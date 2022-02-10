from pydantic import BaseModel
from typing import Union, List, Tuple


class Bicycle(BaseModel):
    BICYCLE_ID: int
    POSITION: Tuple[float, float, float]
    ORIENTATION: Tuple[float, float, float, float]
    SIZE: Tuple[float, float, float]
    STATUS: int
    RIDER: Union[int, None]
    TYPE: int


class Human(BaseModel):
    HUMAN_ID: int
    POSITION: Tuple[float, float, float]
    ORIENTATION: Tuple[float, float, float, float]
    SIZE: Tuple[float, float, float]
    WEARS_HELMET: Union[int, None]
    AGE: int


class Frame(BaseModel):
    FRAME_ID: int
    BICYCLES: List[Bicycle]
    HUMANS: List[Human]


class Frames(BaseModel):
    FRAMES: List[Frame]
