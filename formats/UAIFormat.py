from pydantic import BaseModel, validator
from typing import Union, Literal


class BicycleAttributes(BaseModel):
    status: Literal['parked', 'stopped', 'moving']
    type: Literal['normal', 'motorized']

    # assumption that 'driving' and 'moving' are synonyms
    @validator('status', pre=True)
    def convert_driving_to_moving(cls, value):
        if value == 'driving':
            return 'moving'


class HumanAttributes(BaseModel):
    wears_helmet: bool
    age: Literal['adult', 'child']
    rides_on_bicycle: str


class BaseUAIFormat(BaseModel):
    annotationId: str
    frameId: int
    temporalId: str
    label: Literal['BICYCLE', 'HUMAN']
    attributes: Union[BicycleAttributes, HumanAttributes]
    x: float
    y: float
    z: float
    roll: float
    yaw: float
    pitch: float
    length: float
    height: float
    width: float

    @validator('length', 'height', 'width')
    def must_be_greater_than_zero(cls, value):
        if value > 0:
            return value
        raise ValueError('Object dimensions should be greater than zero')


