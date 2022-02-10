import json
import pydantic
from formats.UAIFormat import BaseUAIFormat
from modules.UAItoSpecificationId import convert_data
from modules.ErrorParser import print_errors
from modules.UUIDtoInt import UUID_to_int
import pandas as pd
from os import path, mkdir, listdir
import numpy as np

IDENTIFIER = 'label'
OBJECT_UUID = 'temporalId'
FRAME_ID_COLUMN = 'frameId'


def np_encoder(obj):
    if isinstance(obj, np.generic):
        return obj.item()


input_folder = 'input'
files = [file for file in listdir(input_folder) if file.endswith('.json')]

for file_name in files:
    file_path = path.join(input_folder, file_name)

    with open(file_path, 'r') as file_handler:
        loaded_data = json.load(file_handler)

    valid_data = []
    invalid_data = []

    for item in loaded_data:
        try:
            valid_data.append(BaseUAIFormat(**item))
        except pydantic.ValidationError as VE:
            invalid_data.append((VE, item))

    print_errors(invalid_data)

    data = pd.DataFrame([item.dict() for item in valid_data])

    unique_ids = {
        label: UUID_to_int(
            groupedData.sort_values(FRAME_ID_COLUMN)[OBJECT_UUID].unique(),
            label
        ) for label, groupedData in data.groupby(IDENTIFIER)
    }

    all_data = {
        'FRAMES': [{
            'FRAME_ID': label,
            'BICYCLES': convert_data(groupedDataByFrameId, 'BICYCLE', unique_ids),
            'HUMANS': convert_data(groupedDataByFrameId, 'HUMAN', unique_ids),
              } for label, groupedDataByFrameId in data.groupby(FRAME_ID_COLUMN)
        ]
    }

    if not path.exists('output'):
        mkdir('output')

    output_file = 'output/{}_SID_format.json'.format(file_name)

    with open(output_file, 'w') as file_handler:
        json.dump(all_data, file_handler, default=np_encoder)
