from datetime import datetime
from typing import List, Any
from sqlalchemy.engine import Connection
from <%= projectName %>_libs.dtos_and_utilities import AccountInfo
from <%= projectName %>_libs.tables import (
	users,
	userRoles,
	user_action_history,
)
from sqlalchemy import insert
from .db_data import *
from .constant_values_defs import (
	mock_ordered_date_list,
	primary_user,
	mock_password
)


fooDirOwnerId = 11
jazzDirOwnerId = 11
blitzDirOwnerId = 11



def populate_users(
	conn: Connection,
	orderedTestDates: List[datetime],
	primaryUser: AccountInfo,
	testPassword: bytes
):
	userParams = get_user_params(orderedTestDates, primaryUser, testPassword)
	stmt = insert(users)
	conn.execute(stmt, userParams)

def populate_user_roles(
	conn: Connection,
	orderedTestDates: List[datetime],
	primaryUser: AccountInfo,
):
	userRoleParams = get_user_role_params(orderedTestDates, primaryUser)
	stmt = insert(userRoles)
	conn.execute(stmt, userRoleParams) #pyright: ignore [reportUnknownMemberType]

#don't remember why I am using using funcs to return these global variables
def get_initial_users() -> list[dict[Any, Any]]:
	userParams = get_user_params(
		mock_ordered_date_list,
		primary_user(),
		mock_password()
	)
	return userParams

def populate_user_actions_history(
	conn: Connection,
	orderedTestDates: List[datetime]
):
	actionsHistoryParams = get_actions_history(orderedTestDates)
	stmt = insert(user_action_history)
	conn.execute(stmt, actionsHistoryParams) #pyright: ignore [reportUnknownMemberType]

