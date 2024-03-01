import sys
from typing import (Any, Optional, Iterable, Iterator, Callable)
from .generic_dtos import MCBaseClass
from .user_role_def import UserRoleDomain, RulePriorityLevel
from itertools import groupby, chain
from operator import attrgetter





class ActionRule(MCBaseClass):
	name: str=""
	span: float=0
	count: float=0
	#if priority is not specified, priority should be specific
	# (station, path) > general
	priority: Optional[int]=RulePriorityLevel.NONE.value
	domain: str=UserRoleDomain.Site.value
	# model_config=ConfigDict(revalidate_instances="subclass-instances")

	@staticmethod
	def sorted(rules: Iterable["ActionRule"]) -> list["ActionRule"]:
		s = sorted(rules, key=attrgetter("score"))
		s.sort(key=attrgetter("priority"), reverse=True)
		s.sort(key=attrgetter("name"))
		return s

	@staticmethod
	def aggregate(
		*args: Iterable["ActionRule"],
		filter: Callable[["ActionRule"], bool]=lambda r: True
	) -> list["ActionRule"]:
		return ActionRule.sorted(r for r in chain(
			*args
		) if filter(r))

	@property
	def priorityElse(self) -> int:
		return self.priority or RulePriorityLevel.NONE.value

	@property
	def score(self) -> float:
		if self.noLimit:
			return sys.maxsize
		return abs(self.count / self.span)

	@property
	def noLimit(self) -> bool:
		return not self.span

	@property
	def blocked(self) -> bool:
		#noLimit has higher precedence because I don't want to rewrite
		#my comparison methods again
		return not self.noLimit and not self.count

	def conforms(self, rule: str) -> bool:
		return rule == self.name

	def __gt__(self, other: "ActionRule") -> bool:
		if self.name > other.name:
			return True
		if self.name < other.name:
			return False
		if (self.priorityElse) > (other.priorityElse):
			return True
		if (self.priorityElse) < (other.priorityElse):
			return False
		return self.score > other.score

	def __lt__(self, other: "ActionRule") -> bool:
		if self.name < other.name:
			return True
		if self.name > other.name:
			return False
		if (self.priorityElse) < (other.priorityElse):
			return True
		if (self.priorityElse) > (other.priorityElse):
			return False
		return self.score < other.score

	def __ge__(self, other: "ActionRule") -> bool:
		if self.name > other.name:
			return True
		if self.name < other.name:
			return False
		if (self.priorityElse) > (other.priorityElse):
			return True
		if (self.priorityElse) < (other.priorityElse):
			return False
		return self.score >= other.score

	def __le__(self, other: "ActionRule") -> bool:
		if self.name < other.name:
			return True
		if self.name > other.name:
			return False
		if (self.priorityElse) < (other.priorityElse):
			return True
		if (self.priorityElse) > (other.priorityElse):
			return False
		return self.score <= other.score

	def __eq__(self, other: Any) -> bool:
		if not other:
			return False
		return self.name == other.name and\
			self.span == other.span and self.count == other.count

	def __ne__(self, other: Any) -> bool:
		if not other:
			return True
		return self.name != other.name or\
			self.span != other.span or self.count != other.count

	def __hash__(self) -> int:
		return hash((
			self.name,
			self.span,
			self.count,
			self.priority
		))

	@staticmethod
	def filter_out_repeat_roles(
		rules: Iterable["ActionRule"]
	) -> Iterator["ActionRule"]:
		yield from (next(g[1]) for g in groupby(rules, key=lambda k: k.name))


action_rule_class_map = {
	UserRoleDomain.Site.value: ActionRule
}