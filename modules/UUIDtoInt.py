import pandas as pd


def UUID_to_int(unique_ids_array, label):
    # this function maps uuid as index and int as values of series
    id_with_uuid = pd.Series(unique_ids_array)
    uuid_with_id = pd.Series(id_with_uuid.index, id_with_uuid.values, name=label)

    return uuid_with_id
