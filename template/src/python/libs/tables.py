from typing import cast, Optional
from sqlalchemy import (
	BINARY,
	Boolean,
	Column,
	Double,
	Float,
	ForeignKey,
	Index,
	Integer,
	LargeBinary,
	MetaData,
	String,
	Table,
	Text
)
from sqlalchemy.sql.schema import Column


metadata = MetaData()

def get_ddl_scripts(conn: Connection) -> str:
	
	result = ""
	for table in metadata.sorted_tables:
		result += str(CreateTable(table).compile(conn))
		for index in sorted(table.indexes or [], key=lambda i: i.name or ""):
			result += (str(CreateIndex(index).compile(conn)) + "\n")

	return result

users = Table("users", metadata,
	Column("pk", Integer, primary_key=True),
	Column("username", String(50), nullable=False),
	Column("displayname", String(50), nullable=True),
	Column("hashedpw", LargeBinary, nullable=True),
	Column("email", String(254), nullable=True),
	Column("isdisabled", Boolean, nullable=True),
	Column("creationtimestamp", Double[float](), nullable=False),
	Column("viewsecuritylevel", Integer, nullable=True),
)

u = users.c
u_pk = cast(Column[Integer],u.pk)
u_username = cast(Column[String],u.username)
u_displayName = cast(Column[Optional[String]],u.displayname)
u_hashedPW = cast(Column[LargeBinary],u.hashedpw)
u_email = cast(Column[Optional[String]],u.email)
u_disabled = cast(Column[Optional[Integer]],u.isdisabled)
u_creationTimestamp = cast(Column[Double[float]],u.creationtimestamp)

Index("idx_uniqueusername", u_username, unique=True)
Index("idx_uniqueemail", u_email, unique=True)


userRoles = Table("userroles", metadata,
	Column("userfk", Integer, ForeignKey("users.pk"), nullable=False),
	Column("role", String(50)),
	Column("span", Float[float], nullable=False),
	Column("count", Float[float], nullable=False),
	Column("priority", Integer),
	Column("creationtimestamp", Double[float], nullable=False)
)
ur_userFk = cast(Column[Integer], userRoles.c.userfk)
ur_role = cast(Column[String], userRoles.c.role)
ur_span = cast(Column[Float[float]], userRoles.c.span)
ur_count = cast(Column[Float[float]], userRoles.c.count)
ur_priority = cast(Column[Integer], userRoles.c.priority)
Index("idx_userroles", ur_userFk, ur_role, unique=True)

user_agents = Table("useragents",metadata,
	Column("pk", Integer, primary_key=True),
	Column("content", Text, nullable=False),
	Column("hash", BINARY(16), nullable=False),
	Column("length", Integer, nullable=False),
)

uag_pk = cast(Column[Integer], user_agents.c.pk)
uag_content = cast(Column[String], user_agents.c.content)
uag_hash = cast(Column[BINARY], user_agents.c.hash)
uag_length = cast(Column[Integer], user_agents.c.length)

Index("idx_useragenthash", uag_hash)


user_action_history = Table("useractionhistory", metadata,
	Column("pk", Integer, primary_key=True),
	Column("userfk", Integer, ForeignKey("users.pk"), nullable=True),
	Column("action", String(50), nullable=False),
	Column("timestamp", Double[float], nullable=True),
	Column("queuedtimestamp", Double[float], nullable=False),
	Column("ipv4address", String(24), nullable=True),
	Column("ipv6address", String(50), nullable=True),
	Column("useragentsfk", Integer, ForeignKey("useragents.pk"), nullable=True),
)

uah = user_action_history.c
uah_pk = cast(Column[Integer], uah.pk)
uah_userFk = cast(Column[Optional[Integer]],uah.userfk)
uah_action = cast(Column[String], uah.action)
uah_timestamp = cast(Column[Optional[Double[float]]],uah.timestamp)
uah_queuedTimestamp = cast(Column[Double[float]], uah.queuedtimestamp)
uah_requestedTimestamp = cast(Column[Double[float]], uah.requestedtimestamp)



jobs = Table('jobs', metadata,
	Column('pk', Integer, primary_key=True, autoincrement=True),
	Column("jobtype", String(50), nullable=False),
	Column("status", String(50), nullable=True),
	Column("instructions", String(2000), nullable=True),
	Column("queuedtimestamp", Double[float], nullable=False),
	Column('completedtimestamp', Double[float], nullable=True)
)

j = jobs.c
j_pk = cast(Column[Integer], j.pk)
j_type = cast(Column[String], j.jobtype)
j_status = cast(Column[String], j.status)
j_instructions = cast(Column[String], j.instructions)
j_queuedtimestamp = cast(Column[Double[float]], j.queuedtimestamp)
j_completedtimestamp = cast(Column[Double[float]], j.completedtimestamp)