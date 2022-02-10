import json
import pydantic
from formats.UAIFormat import BaseUAIFormat
from formats.SpecificationIdFormat import Frames
from modules.UAItoSpecificationId import convert_data
from modules.ErrorParser import print_errors
from modules.UUIDtoInt import UUID_to_int
import pandas as pd
from os import path, mkdir, listdir
import numpy as np

IDENTIFIER = 'label'
OBJECT_UUID = 'temporalId'
FRAME_ID_COLUMN = 'frameId'


# this is helper function to covert int64 and float64 to int and float because
# json has problems with numpy's int64 and float64
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

    # potential check if there is any invalid data, in that case, program should not continue, discussion

    data = pd.DataFrame([item.dict() for item in valid_data])

    # this is a dict containing unique values of each label, ordered by frame, as requested
    # in specification that numbering should be consecutive and objects which first appear
    # on earlier  frames should have smaller ids
    unique_ids = {
        label: UUID_to_int(
            groupedData.sort_values(FRAME_ID_COLUMN)[OBJECT_UUID].unique(),
            label
        ) for label, groupedData in data.groupby(IDENTIFIER)
    }

    formatted_data = {
        'FRAMES': [{
            'FRAME_ID': label,
            'BICYCLES': convert_data(groupedDataByFrameId, 'BICYCLE', unique_ids),
            'HUMANS': convert_data(groupedDataByFrameId, 'HUMAN', unique_ids),
              } for label, groupedDataByFrameId in data.groupby(FRAME_ID_COLUMN)
        ]
    }

    if not path.exists('output'):
        mkdir('output')

    # validate output data format
    try:
        d = Frames(**formatted_data)
    except pydantic.ValidationError as VE:
        print(VE)

    # improvement: if there is something wrong with data validation, data should not be written to file

    output_file = 'output/{}_SID_format.json'.format(file_name.strip('.json'))

    with open(output_file, 'w') as file_handler:
        json.dump(formatted_data, file_handler, default=np_encoder)
