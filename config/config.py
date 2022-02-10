from enum import Enum


class UAIFormat(Enum):
    ANNOTATION_ID = 'annotationId'
    FRAME_ID = 'frameId'
    OBJECT_ID = 'temporalId'
    LABEL = 'label'
    ATTRIBUTES = 'attributes'
    X = 'x'
    Y = 'y'
    Z = 'z'
    ROLL = 'roll'
    YAW = 'yaw'
    PITCH = 'pitch'
    LENGTH = 'length'
    HEIGHT = 'height'
    WIDTH = 'width'
    STATUS = 'status'
    TYPE = 'type'
    AGE = 'age'
    WEARS_HELMET = 'wears_helmet'
    RIDES_ON_BICYCLE = 'rides_on_bicycle'

