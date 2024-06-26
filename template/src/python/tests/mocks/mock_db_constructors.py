import pytest
from typing import (Protocol, Optional)
from datetime import datetime
from sqlalchemy.engine import Connection
from <%= projectNameSnake %>.dtos_and_utilities import AccountInfo
from .db_population import (
	populate_users,
	populate_user_roles,
	populate_user_actions_history
)

class ConnectionConstructor(Protocol):
	def __call__(
		self,
		echo: bool=False,
		inMemory: bool=False
	) -> Connection:
			...

class MockDbPopulateClosure(Protocol):
	def __call__(
		self,
		conn: Connection,
		request: Optional[pytest.FixtureRequest]=None
	) -> None:
		...


def setup_in_mem_tbls(
	conn: Connection,
	request: Optional[pytest.FixtureRequest],
	orderedTestDates: list[datetime],
	primaryUser: AccountInfo,
	testPassword: bytes,
) -> None:
	populate_users(conn, orderedTestDates, primaryUser, testPassword)
	populate_artists(conn)
	populate_albums(conn)
	populate_songs(conn)
	populate_songs_artists(conn)
	populate_stations(conn)
	populate_stations_songs(conn)
	populate_user_roles(conn, orderedTestDates, primaryUser)
	populate_station_permissions(conn, orderedTestDates)
	populate_path_permissions(conn, orderedTestDates)
	populate_user_actions_history(conn, orderedTestDates)
	populate_station_queue(conn)
	conn.commit()
