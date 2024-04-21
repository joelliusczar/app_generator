from typing import (
	List,
	TypeVar,
	Generic
)
from pydantic import BaseModel as <%= ucPrefix %>BaseClass, ConfigDict


T = TypeVar("T")

class FrozenBaseClass(<%= ucPrefix %>BaseClass):
	model_config = ConfigDict(frozen=True)

class ListData(<%= ucPrefix %>BaseClass, Generic[T]):
	items: List[T]


class TableData(ListData[T]):
	totalrows: int


# class ErrorInfo(BaseModel):
# 	msg: str

class IdItem(FrozenBaseClass):
	id: int