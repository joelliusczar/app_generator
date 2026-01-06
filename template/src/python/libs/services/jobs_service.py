from typing import (
	Iterator,
	Optional,
	Any,
	Iterable
)
from <%= projectNameSnake %>.dtos_and_utilities import (
	get_datetime,
	JobInfo
)
from <%= projectNameSnake %>.dtos_and_utilities.logging import (
	scheduledServiceLogger
)
from <%= projectNameSnake %>.dtos_and_utilities.constants import (
	JobTypes,
	JobStatusTypes,
)

from sqlalchemy import (
	select,
	insert,
	update
)
from sqlalchemy.engine import Connection
from musical_ch<%= projectNameSnake %>airs_libs.tables import (
	jobs as jobs_tbl, j_pk, j_instructions, j_type, j_status, j_queuedtimestamp,
	j_completedtimestamp
)


class JobsService:

	def __init__(
		self,
		conn: Connection,
	) -> None:
		if not conn:
			raise RuntimeError("No connection provided")
		self.conn = conn
		self.get_datetime = get_datetime

	def __set_status__(self, id: int, status: str):
		if status == JobStatusTypes.COMPLETED.value:
			completedTimestamp = get_datetime().timestamp()
			stmt = update(jobs_tbl).values(
				status = status,
				completedtimestamp = completedTimestamp
			)\
			.where(j_pk == id)
		else:
			stmt = update(jobs_tbl).values(status = status).where(j_pk == id)
		self.conn.execute(stmt)
		self.conn.commit()

	def get_all(
		self,
		ids: Optional[Iterable[int]]=None,
		jobType: Optional[str]=None,
		status: Optional[str]=""
	) -> Iterator[JobInfo]:
		
		query = select(
			j_pk.label("id"),
			j_type, 
			j_status, 
			j_instructions, 
			j_queuedtimestamp,
			j_completedtimestamp
		)
		if ids:
			query = query.where(j_pk.in_(ids))
		else:

			if jobType:
				query = query.where(j_type == jobType)
			
			if status is None:
				query = query.where(j_status.is_(None))
			elif status:
				query = query.where(j_status == status)
		
		rows = self.conn.execute(query).mappings()
		yield from (JobInfo(**row) for row in rows)
		


	def add(self, internalPaths: Iterable[str]):
		params: list[dict[str, Any]] = [
			{
				"jobtype": JobTypes.SONG_DELETE.value,
				"instructions": path,
				"queuedtimestamp": self.get_datetime().timestamp()
			} for path in internalPaths
		]
		stmt = insert(jobs_tbl)
		self.conn.execute(stmt, params)