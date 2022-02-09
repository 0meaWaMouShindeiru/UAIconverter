import json
import pydantic
from formats.UAIFormat import BaseUAIFormat
from modules.OrientationCoverter import convert_Euler_to_quaternion
from modules.PositionConverter import calculate_center_position_from_dimensions
from modules.UUIDtoInt import UUID_to_int
import pandas as pd
from os import path

IDENTIFIER = 'label'
OBJECT_UUID = 'temporalId'
FRAME_ID_COLUMN = 'frameId'

file = 'input/annotations.json'

with open(file, 'r') as file_handler:
    loaded_data = json.load(file_handler)

valid_data = []
invalid_data = []


age_converter = {
    'adult': 0,
    'child': 1
}

bicycle_type_converter = {
    'normal': 0,
    'motorized': 1
}

bicycle_status_converter = {
    'parked': 2,
    'stopped': 1,
    'moving': 0
}


for item in loaded_data:
    try:
        valid_data.append(BaseUAIFormat(**item))
    except pydantic.ValidationError as VE:
        invalid_data.append((VE, item))

data = pd.DataFrame([item.dict() for item in valid_data])

unique_ids = {
    label: UUID_to_int(
        groupedData.sort_values(FRAME_ID_COLUMN)[OBJECT_UUID].unique(),
        label
    ) for label, groupedData in data.groupby(IDENTIFIER)
}
def convert_common_data(row):
    return {
        'POSITION': calculate_center_position_from_dimensions(
            row['x'], row['y'], row['z'], row['height'], row['length'], row['width']
        ),
        'ORIENTATION': convert_Euler_to_quaternion(
            row['yaw'], row['pitch'], row['roll']
        ),
        'SIZE': (row['width'], row['length'], row['height'])
    }


def expand_attributes(data: pd.DataFrame, label: str):
    expanded_data = data[data['label'] == label]
    expanded_data = pd.concat([
        expanded_data,
        expanded_data['attributes'].apply(pd.Series)
    ], axis=1)

    return expanded_data


def convert_data(data: pd.DataFrame, label: str):
    relevant_data = expand_attributes(data, label)

    ridden_bicycles = expand_attributes(data, 'HUMAN')
    # find humans that are driving bicycle and their relation
    ridden_bicycles = ridden_bicycles[~ridden_bicycles['rides_on_bicycle'].isin([''])][[OBJECT_UUID, 'rides_on_bicycle']]
    ridden_bicycles.rename(columns={
            OBJECT_UUID: 'human_id',
            'rides_on_bicycle': 'bicycle_id'
        }, inplace=True)

    if not relevant_data.shape[0]:
        return []

    objects = []

    for _, row in relevant_data.iterrows():
        common_data = convert_common_data(row)
        specific_data = globals()['convert_{}'.format(label.lower())](row, ridden_bicycles)
        objects.append({
            **common_data,
            **specific_data
        })

    return objects


def convert_bicycle(row, ridden_bicycles: pd.DataFrame):
    status = bicycle_status_converter[row['status']]
    bicycle_uuid = row[OBJECT_UUID]

    rider = None

    if bicycle_uuid in ridden_bicycles['bicycle_id'].tolist():
        temp_df = ridden_bicycles.set_index('bicycle_id')
        human_uuid = temp_df.loc[bicycle_uuid]['human_id']
        rider = unique_ids['HUMAN'].loc[human_uuid]

        if status == 2:
            # Assumption that, if bike, which is labeled as parked, has a driver, is actually stopped
            # This should be discussed
            status = 1

    return {
        'BICYCLE_ID': unique_ids['BICYCLE'].loc[bicycle_uuid],
        'TYPE': bicycle_type_converter[row['type']],
        'STATUS': status,
        'RIDER': rider
    }


def convert_human(row, ridden_bicycles):
    human_uuid = row[OBJECT_UUID]
    # ridden_bicycles = ridden_bicycles.set_index('human_id')
    helmet = None
    if human_uuid in ridden_bicycles['human_id'].tolist():
        helmet = 1 if row['wears_helmet'] else 0

    return {
        'HUMAN_ID': unique_ids['HUMAN'].loc[human_uuid],
        'AGE': age_converter[row['age']],
        'WEARS_HELMET': helmet
    }


all_data = {
    'FRAMES': [{
        'FRAME_ID': label,
        'BICYCLES': convert_data(groupedDataByFrameId, 'BICYCLE'),
        'HUMANS': convert_data(groupedDataByFrameId, 'HUMAN'),
          } for label, groupedDataByFrameId in data.groupby(FRAME_ID_COLUMN)
    ]
}

