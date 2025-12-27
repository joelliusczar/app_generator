from typing import Optional, cast, Iterable, Iterator, Tuple
from enum import Enum
from sqlalchemy.sql.expression import Select, false, CompoundSelect
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.sql.schema import Column
from sqlalchemy.engine.row import RowMapping
from sqlalchemy import (
	select,
	union_all,
	literal as dbLiteral,
	case,
	or_
)
from sqlalchemy import Integer, String
from <%= projectNameSnake %>.tables import (
	ur_userFk, ur_role, ur_count, ur_span, ur_priority,
	u_username, u_pk, u_displayName, u_email, u_dirRoot,
)
from .user_role_def import (
	UserRoleDef,
	UserRoleDomain,
	RulePriorityLevel,
)
from .action_rule_dtos import (
	ActionRule,
	action_rule_class_map,
)
from .account_dtos import (
	AccountInfo
)




def __build_placeholder_select__(
	domain:UserRoleDomain
) -> Select[Tuple[int, String, float, float, int, str]]:
	ruleNameCol = cast(Column[String], dbLiteral(UserRoleDef.STATION_VIEW.value) \
		if domain == UserRoleDomain.Station \
			else dbLiteral(UserRoleDef.PATH_VIEW.value))
	query = select(
		dbLiteral(0).label("rule_userfk"),
		ruleNameCol.label("rule_name"),
		cast(Column[float],dbLiteral(0)).label("rule_count"),
		cast(Column[float],dbLiteral(0)).label("rule_span"),
		dbLiteral(0).label("rule_priority"),
		dbLiteral("shim").label("rule_domain"),
	)

	return query

#int, String, int, int, int, str]]:

def build_site_rules_query(
	userId: Optional[int]=None
) -> Select[Tuple[Integer, String, Float[float], Float[float], Integer, str]]:

	user_rules_query = select(
		ur_userFk.label("rule_userfk"),
		ur_role.label("rule_name"),
		ur_count.label("rule_count"),
		ur_span.label("rule_span"),
		coalesce[Integer](
			ur_priority,
			case(
				(ur_role == UserRoleDef.ADMIN.value, RulePriorityLevel.SUPER.value),
				else_=RulePriorityLevel.SITE.value
			)
		).label("rule_priority"),
		dbLiteral(UserRoleDomain.Site.value).label("rule_domain"),
	)

	if userId is not None:
		user_rules_query = user_rules_query.where(ur_userFk == userId)

	return user_rules_query


def row_to_user(row: RowMapping) -> AccountInfo:
	return AccountInfo(
		id=row[u_pk],
		username=row[u_username],
		displayname=row[u_displayName],
		email=row[u_email],
		dirroot=row[u_dirRoot],
	)

def row_to_action_rule(row: RowMapping) -> ActionRule:
	clsConstructor = action_rule_class_map.get(
		row["rule_domain"],
		ActionRule
	)

	return clsConstructor(
		name=row["rule_name"],
		span=row["rule_span"],
		count=row["rule_count"],
		priority=cast(int,row["rule_priority"]) if row["rule_priority"] \
			else RulePriorityLevel.NONE
	)

def generate_user_and_rules_from_rows(
	rows: Iterable[RowMapping]
) -> Iterator[AccountInfo]:
	currentUser = None
	for row in rows:
		if not currentUser or currentUser.id != cast(int,row[u_pk]):
			if currentUser:
				yield currentUser
			currentUser = row_to_user(row)
			if row["rule_domain"] != "shim":
				currentUser.roles.append(row_to_action_rule(row))
		elif row["rule_domain"] != "shim":
			currentUser.roles.append(row_to_action_rule(row))
	if currentUser:
		yield currentUser