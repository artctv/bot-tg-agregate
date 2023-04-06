from enum import Enum


class GroupTypeEnum(str, Enum):
    """Available `group_type` values"""
    hour = "hour"
    day = "day"
    month = "month"
