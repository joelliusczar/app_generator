#pyright: reportUnknownMemberType=false, reportGeneralTypeIssues=false
#pyright: reportMissingTypeStubs=false
import pytest
import sqlite3
from typing import Callable
from sqlalchemy import select
from .constant_fixtures_for_test import *
from .common_fixtures import (
	fixture_setup_db as fixture_setup_db,
	fixture_db_conn_in_mem as fixture_db_conn_in_mem,
	fixture_db_queryer as fixture_db_queryer
)
from <%= projectNameSnake %>.services import DbOwnerConnectionService
from sqlalchemy.engine import Connection
from .mocks.db_data import *
from .mocks import db_population
from .constant_fixtures_for_test import (
	fixture_mock_password as fixture_mock_password,\
	fixture_primary_user as fixture_primary_user,\
	fixture_mock_ordered_date_list as fixture_mock_ordered_date_list
)

@pytest.fixture
def fixture_db_populate_factory(
	request: pytest.FixtureRequest,
	fixture_setup_db: str,
	fixture_mock_ordered_date_list: List[datetime],
	fixture_primary_user: AccountInfo,
	fixture_mock_password: bytes
) -> Callable[[], None]:
	def populate_fn():
		dbName = fixture_setup_db
		with DbOwnerConnectionService(dbName) as ownerConnService:
			conn = ownerConnService.conn
			db_population.populate_users(
				conn,
				fixture_mock_ordered_date_list,
				fixture_primary_user,
				fixture_mock_password
			)
			# db_population.populate_table(conn)
			conn.commit()
	return populate_fn

@pytest.mark.populateFnName("fixture_db_populate_factory")
@pytest.mark.echo(False)
def test_in_mem_db(fixture_db_conn_in_mem: Connection) -> None:
	pass
	# query = select(table).order_by(a.name)
	# res = fixture_db_conn_in_mem.execute(query).fetchall()


def test_data_view(
	fixture_mock_ordered_date_list: List[datetime],
	fixture_primary_user: AccountInfo,
	fixture_mock_password: bytes
):
	# this test exists as a convience to run queires on
	# the test data
	noop: Callable[[Any], Any] = lambda x: None
	#noop(params)
	users = get_user_params(
		fixture_mock_ordered_date_list,
		fixture_primary_user,
		fixture_mock_password
	)
	noop(users)
	userRoles = get_user_role_params(
		fixture_mock_ordered_date_list,
		fixture_primary_user
	)
	noop(userRoles)

	pass

def test_data_in_db(
	fixture_db_conn_in_mem: Connection,
	fixture_db_queryer: Callable[[str], None]):
	# this test exists as a convience to run sql queires on
	# the test data
	# print(query.compile(compile_kwargs={"literal_binds": True}))
	pass
