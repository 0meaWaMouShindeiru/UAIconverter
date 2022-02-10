import pandas as pd
from config.config import UAIFormat
from modules.OrientationCoverter import convert_Euler_to_quaternion
from modules.PositionConverter import calculate_center_position_from_dimensions
from modules.BicycleConverter import convert_bicycle
from modules.HumanConverter import convert_human

OBJECT_UUID = UAIFormat.OBJECT_ID.value
X = UAIFormat.X.value
Y = UAIFormat.Y.value
Z = UAIFormat.Z.value
HEIGHT = UAIFormat.HEIGHT.value
LENGTH = UAIFormat.LENGTH.value
WIDTH = UAIFormat.WIDTH.value
LABEL = UAIFormat.LABEL.value
RIDES_ON_BICYCLE = UAIFormat.RIDES_ON_BICYCLE.value
YAW = UAIFormat.YAW.value
PITCH = UAIFormat.PITCH.value
ROLL = UAIFormat.ROLL.value
ATTRIBUTES = UAIFormat.ATTRIBUTES.value


def convert_common_data(row):
    return {
        'POSITION': calculate_center_position_from_dimensions(
            row[X], row[Y], row[Z], row[HEIGHT], row[LENGTH], row[WIDTH]
        ),
        'ORIENTATION': convert_Euler_to_quaternion(
            row[YAW], row[PITCH], row[ROLL]
        ),
        'SIZE': (row[WIDTH], row[LENGTH], row[HEIGHT])
    }


def expand_attributes(data: pd.DataFrame, label: str):
    expanded_data = data[data[LABEL] == label]
    expanded_data = pd.concat([
        expanded_data,
        expanded_data[ATTRIBUTES].apply(pd.Series)
    ], axis=1)

    return expanded_data


def convert_data(data: pd.DataFrame, label: str, unique_ids):
    relevant_data = expand_attributes(data, label)

    ridden_bicycles = expand_attributes(data, 'HUMAN')
    # find humans that are driving bicycle and their relation
    ridden_bicycles = ridden_bicycles[~ridden_bicycles[RIDES_ON_BICYCLE].isin([''])][[OBJECT_UUID, RIDES_ON_BICYCLE]]
    ridden_bicycles.rename(columns={
            OBJECT_UUID: 'human_id',
            RIDES_ON_BICYCLE: 'bicycle_id'
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





