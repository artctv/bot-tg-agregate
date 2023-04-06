from dataclasses import dataclass
from datetime import datetime
from typing import Any
from enums import GroupTypeEnum


@dataclass
class AgregateResultDTO:
    """Data Transfer Object according required format"""
    dataset: list[str]
    labels: list[str]


class AgregateBuilder:
    """
    Class which accumulate logick over building mongodb aggregating pipline
    """
    dt_from: datetime
    dt_upto: datetime
    group_type: GroupTypeEnum
    pipline: list[dict]

    def __init__(self, dt_from: datetime, dt_upto: datetime, group_type: GroupTypeEnum):
        self.dt_from = dt_from
        self.dt_upto = dt_upto
        self.group_type = group_type
        self.pipline = list()

    def _get_time_window(self) -> dict[str, datetime]:
        """Return time window over `dt_from` and `dt_upto`"""
        return {"$gte": self.dt_from, "$lte": self.dt_upto}

    def _get_time_format(self) -> str:
        """Return the time format depending on the selected `group_type`"""
        _map = {
            GroupTypeEnum.hour: "%Y-%m-%dT%H:00:00",
            GroupTypeEnum.day: "%Y-%m-%dT00:00:00",
            GroupTypeEnum.month: "%Y-%m-01T00:00:00"
        }
        return _map.get(self.group_type)

    def _build_match(self, date_variable: str) -> None:
        """Builds a match field for the specified time period to sample data"""
        self.pipline.append(
           {"$match": {date_variable: self._get_time_window()}}
        )

    def _build_group(self, date_variable: str, value_variable: str) -> None:
        """
        Builds a grouping of data:
            - Depending on the selected `group_type`, the time cutoff point for grouping data will change
            For example: if we want to group data by days, we need to cut off hours, minutes and seconds
            (according to the ISO format), and if we want group by months, then we must also discard the day
            (in this case, instead of discarding, the day set to `01`)
            - Field `data` it is just a sum of `value_variable` over groupping period
        """
        self.pipline.append(
            {
                "$group": {
                    "_id": {
                        "label": {"$dateToString": {"format": self._get_time_format(), "date": f"${date_variable}"}}
                    },
                    "data": {"$sum": f"${value_variable}"}
                }
            }
        )

    def _build_sort(self, sort_value: int) -> None:
        """Build a sort order:
            1 - from oldest to newest
            -1 - from newest to oldest
        """
        self.pipline.append(
            {"$sort": {"_id": sort_value}}
        )

    def build_pipiline(self, date_variable: str, value_variable: str, sort_value: int) -> list[dict]:
        """Build all part of pipeline for mongodb aggregate"""
        self._build_match(date_variable)
        self._build_group(date_variable, value_variable)
        self._build_sort(sort_value)
        return self.pipline


async def get_agregated(
    collection: Any,
    dt_from: datetime,
    dt_upto: datetime,
    group_type: GroupTypeEnum
) -> AgregateResultDTO:
    builder = AgregateBuilder(dt_from, dt_upto, group_type)
    pipeline = builder.build_pipiline(date_variable="dt", value_variable="value", sort_value=1)
    dataset, labels = [], []
    async for document in collection.aggregate(pipeline):
        label, data = document["_id"]["label"], document["data"]
        labels.append(label)
        dataset.append(data)
    return AgregateResultDTO(dataset=dataset, labels=labels)
