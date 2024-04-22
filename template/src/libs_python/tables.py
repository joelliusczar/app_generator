from typing import cast, Optional
from sqlalchemy import (
	Table,
	MetaData,
	Column,
	Float,
	Double,
	Boolean,
	LargeBinary,
	Integer,
	String,
	ForeignKey,
	Index,
	Text
)
from sqlalchemy.sql.schema import Column



metadata = MetaData()


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

user_action_history = Table("useractionhistory", metadata,
	Column("pk", Integer, primary_key=True),
	Column("userfk", Integer, ForeignKey("users.pk"), nullable=True),
	Column("action", String(50), nullable=False),
	Column("timestamp", Double[float], nullable=True),
	Column("queuedtimestamp", Double[float], nullable=False),
	Column("requestedtimestamp", Double[float], nullable=True)
)

uah = user_action_history.c
uah_pk = cast(Column[Integer], uah.pk)
uah_userFk = cast(Column[Optional[Integer]],uah.userfk)
uah_action = cast(Column[String], uah.action)
uah_timestamp = cast(Column[Optional[Double[float]]],uah.timestamp)
uah_queuedTimestamp = cast(Column[Double[float]], uah.queuedtimestamp)
uah_requestedTimestamp = cast(Column[Double[float]], uah.requestedtimestamp)




