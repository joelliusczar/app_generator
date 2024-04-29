from typing import (
	Optional,
	Iterator,
	cast,
	Iterable,
	Union,
	overload,
	Collection
)
from sqlalchemy.engine import Connection
from <%= projectNameSnake %>.dtos_and_utilities import (
	get_datetime,
	UserHistoryActionItem,
	ActionRule
)
from sqlalchemy import (
	select,
	insert,
	func
)
from <%= projectNameSnake %>.tables import (
	user_action_history, uah_userFk, uah_action, uah_pk,
	uah_requestedTimestamp,
	station_queue, q_stationFk, q_userActionHistoryFk
)
from itertools import groupby

def __when_next_can_do__(
	rule: ActionRule,
	timestamps: list[float],
	currentTimestamp: float
) -> Optional[float]:
	if rule.noLimit:
		return 0
	if rule.blocked:
		return None
	fromTimestamp = currentTimestamp - rule.span
	#the main query can be overly permissive if
	#there is a mismatch of strictness
	timestamps = [t for t in timestamps if t >= fromTimestamp]
	if not timestamps:
		return 0

	if len(timestamps) == rule.count:
		return timestamps[0] + rule.span
	return 0


class UserActionsHistoryService:

	def __init__(self,
		conn: Optional[Connection]=None
	) -> None:
		if not conn:
			raise RuntimeError("No connection provided")
		self.conn = conn
		self.get_datetime = get_datetime

	@overload
	def get_user_action_history(
		self,
		userId: int,
		fromTimestamp: float,
		actions: Iterable[str]=[],
		limit: Optional[int]=None
	) -> Iterator[UserHistoryActionItem]:
		...


	def get_user_action_history(
		self,
		userId: int,
		fromTimestamp: float,
		actions: Iterable[str]=[],
		limit: Optional[int]=None,
		stationIds: Optional[Iterable[int]]=None
	) -> Iterator[UserHistoryActionItem]:
		query = select(
			uah_action,
			uah_requestedTimestamp,
			func.row_number().over( #pyright: ignore [reportUnknownMemberType]
				partition_by=uah_action,
				order_by=uah_requestedTimestamp
			).label("rownum")
		)\
		.select_from(user_action_history)\
		.where(uah_requestedTimestamp >= fromTimestamp)\
		.where(uah_userFk == userId)
		if actions:
			query = query.where(uah_action.in_(actions))
		query = query.order_by(uah_action, uah_requestedTimestamp)
		subquery = query.subquery()
		query = select(*subquery.c)
		if limit is not None:
			query = query.where(subquery.c.rownum < limit)

		records = self.conn.execute(query).mappings().fetchall()
		yield from (
			UserHistoryActionItem(
				userid=userId,
				action=cast(str,row[uah_action]),
				timestamp=cast(float,row[uah_requestedTimestamp])
			)
			for row in records
		)

	def add_user_action_history_item(self, userId: int, action: str):
		stmt = insert(user_action_history).values(
			userFk = userId,
			action = action,
			timestamp = self.get_datetime().timestamp(),
		)
		res = self.conn.execute(stmt) #pyright: ignore reportUnknownMemberType

	def calc_lookup_for_when_user_can_next_do_action(
		self,
		userid: int,
		rules: Collection[ActionRule],
	) -> dict[str, Optional[float]]:
		if not rules:
			return {}
		maxLimit = max(int(r.count) for r in rules)
		maxSpan = max(r.span for r in rules)
		currentTimestamp = self.get_datetime().timestamp()
		fromTimestamp = currentTimestamp - maxSpan
		actionGen = self.get_user_action_history(
			userid,
			fromTimestamp,
			(r.name for r in rules),
			maxLimit
		)
		presorted = {g[0]:[i.timestamp for i in g[1]] for g in groupby(
			actionGen,
			key=lambda k: k.action
		)}
		result = {
			r.name:__when_next_can_do__(
				r,
				presorted.get(r.name,[]),
				currentTimestamp
			) for r in ActionRule.filter_out_repeat_roles(rules)
		}
		return result
