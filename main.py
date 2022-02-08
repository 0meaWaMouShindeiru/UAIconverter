import json
import pydantic
from formats.UAIFormat import BaseUAIFormat


file = 'input/annotations.json'

with open(file, 'r') as file_handler:
    loaded_data = json.load(file_handler)

valid_data = []
invalid_data = []

for item in loaded_data:
    try:
        valid_data.append(BaseUAIFormat(**item))
    except pydantic.ValidationError as VE:
        invalid_data.append((VE, item))
