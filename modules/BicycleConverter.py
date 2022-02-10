import pandas as pd


OBJECT_UUID = 'temporalId'

bicycle_type_converter = {
    'normal': 0,
    'motorized': 1
}

bicycle_status_converter = {
    'parked': 2,
    'stopped': 1,
    'moving': 0
}


def convert_bicycle(row, ridden_bicycles: pd.DataFrame, unique_ids):
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
