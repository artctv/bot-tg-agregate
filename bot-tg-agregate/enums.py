from typing import Any
from enum import Enum


class GroupTypeEnum(str, Enum):
    """Available `group_type` values"""
    hour = "hour"
    day = "day"
    month = "month"

    @classmethod
    def contain(cls, item: Any):
        return item in cls.__members__.keys()

