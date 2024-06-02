from typing import (
	List,
	TypeVar,
	Generic
)
from pydantic import BaseModel as <%= ucPrefix %>BaseClass, ConfigDict, Field


T = TypeVar("T")

class FrozenBaseClass(<%= ucPrefix %>BaseClass):
	model_config = ConfigDict(frozen=True)

class ListData(<%= ucPrefix %>BaseClass, Generic[T]):
	items: List[T]


class TableData(ListData[T]):
	totalrows: int


# class ErrorInfo(BaseModel):
# 	msg: str

class FrozenIdItem(FrozenBaseClass):
	id: int

class FrozenNamed(FrozenBaseClass):
	name: str

class FrozenNamedIdItem(FrozenIdItem, FrozenNamed):
	...


class IdItem(<%= ucPrefix %>BaseClass):
	id: int=Field(frozen=True)

class Named(<%= ucPrefix %>BaseClass):
	name: str=Field(frozen=True)

class NamedIdItem(IdItem, Named):
	...