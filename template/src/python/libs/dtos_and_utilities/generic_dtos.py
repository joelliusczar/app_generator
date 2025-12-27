from .action_rule_dtos import ActionRule
from pydantic import BaseModel as <%= ucPrefix %>BaseClass, ConfigDict, Field
from typing import (
	List,
	TypeVar,
	Generic
)


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

class RuledEntity(<%= ucPrefix %>BaseClass):
	rules: list[ActionRule]=cast(list[ActionRule], Field(
		default_factory=list, frozen=False
	))
	viewsecuritylevel: Optional[int]=Field(default=0, frozen=False)