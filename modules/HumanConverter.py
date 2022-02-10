import pandas as pd


OBJECT_UUID = 'temporalId'

age_converter = {
    'adult': 0,
    'child': 1
}


def convert_human(row, ridden_bicycles: pd.DataFrame, unique_ids):
    human_uuid = row[OBJECT_UUID]

    helmet = None
    if human_uuid in ridden_bicycles['human_id'].tolist():
        helmet = 1 if row['wears_helmet'] else 0

    return {
        'HUMAN_ID': unique_ids['HUMAN'].loc[human_uuid],
        'AGE': age_converter[row['age']],
        'WEARS_HELMET': helmet
    }



