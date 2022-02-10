import pandas as pd

from modules.OrientationCoverter import convert_Euler_to_quaternion
from modules.PositionConverter import calculate_center_position_from_dimensions
from modules.BicycleConverter import convert_bicycle
from modules.HumanConverter import convert_human

OBJECT_UUID = 'temporalId'


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


def convert_data(data: pd.DataFrame, label: str, unique_ids):
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
        specific_data = globals()['convert_{}'.format(label.lower())](row, ridden_bicycles, unique_ids)
        objects.append({
            **common_data,
            **specific_data
        })

    return objects





