from enum import Enum

class Status(Enum):
    success = (0, 32)        # green
    fail    = (1, 31)        # red
    skip    = (2, 33)        # yellow
    error   = (3, 31)        # red

    def __new__(cls, code, color):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.color = color
        obj.code = code
        return obj

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            return cls[value.lower()]
        raise
