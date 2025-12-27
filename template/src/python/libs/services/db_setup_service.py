from typing import Any
from .template_service import TemplateService
from sqlalchemy import create_engine, NullPool
from sqlalchemy.engine import Connection
from <%= projectNameSnake %>.dtos_and_utilities import (
	ConfigAcessors,
	DbUsers,
	is_name_safe,
	SqlScripts
)
from <%= projectNameSnake %>.tables import metadata
#https://github.com/PyMySQL/PyMySQL/issues/590
from pymysql.constants import CLIENT

def is_db_name_safe(dbName: str) -> bool:
	return is_name_safe(dbName, maxLen=100)

def get_schema_hash() -> str:
	with DbRootConnectionService() as rootConnService:
		content = get_ddl_scripts(rootConnService.conn)
		for scriptEnum in sorted(SqlScripts, key=lambda e: e.value[0]):
			content += (scriptEnum.value[1] + "\n")

		hashStr = hashlib.sha256(content.encode("utf-8")).hexdigest()
		return hashStr

"""
This class will mostly exist for the sake of unit tests
"""
class DbRootConnectionService:

	def __init__(self) -> None:
		self.conn = self.conn = self.get_root_connection()

	def get_root_connection(self) -> Connection:
		dbPass = ConfigAcessors.db_setup_pass()
		if not dbPass:
			raise RuntimeError("The system is not configured correctly for that.")
		engineAsRoot = create_engine(
			f"mysql+pymysql://root:{dbPass}@localhost",
			#not fully sure why this was needed, but mariadb/sqlalchemy/somebody
			#was holding onto connections and this was fucking up unit tests
			poolclass=NullPool
		)
		return engineAsRoot.connect()

	def __enter__(self) -> "DbRootConnectionService":
		return self

	def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any):
		self.conn.close()

	def create_db(self, dbName: str):
		if not is_db_name_safe(dbName):
			raise RuntimeError("Invalid name was used")
		self.conn.exec_driver_sql(f"CREATE DATABASE IF NOT EXISTS {dbName}")

	def create_db_user(self, username: str, host: str, userPass: str):
		if not is_name_safe(username):
			raise RuntimeError("Invalid username was used")
		if not is_name_safe(host):
			raise RuntimeError("Invalid host was used")
		self.conn.exec_driver_sql(
			f"CREATE USER IF NOT EXISTS '{username}'@'{host}' "
			f"IDENTIFIED BY %(userPass)s",
			{ "userPass": userPass}
		)

	def create_app_users(self):
		dbPass = ConfigAcessors.db_pass_api()
		if not dbPass:
			raise RuntimeError("The system is not configured correctly for that.")
		self.create_db_user(
			DbUsers.API_USER.value,
			"localhost",
			dbPass
		)

		dbPass = ConfigAcessors.db_pass_janitor()
		if not dbPass:
			raise RuntimeError("The system is not configured correctly for that.")
		self.create_db_user(
			DbUsers.JANITOR_USER.value,
			"localhost",
			dbPass
		)



	def create_owner(self):
		dbPass = ConfigAcessors.db_pass_owner()
		if not dbPass:
			raise RuntimeError("The system is not configured correctly for that.")
		self.create_db_user(
			DbUsers.OWNER_USER.value,
			"localhost",
			dbPass
		)

	def grant_owner_roles(self, dbName: str):
		if not is_db_name_safe(dbName):
			raise RuntimeError("Invalid name was used")
		user = DbUsers.OWNER_USER(host="localhost")
		self.conn.exec_driver_sql(
			f"GRANT ALL PRIVILEGES ON {dbName}.* to "
			f"{user} WITH GRANT OPTION"
		)
		self.conn.exec_driver_sql(
			f"GRANT RELOAD ON *.* to "
			f"{user}"
		)
		self.conn.exec_driver_sql("FLUSH PRIVILEGES")

	#this method can only be used on test databases
	def drop_database(self, dbName: str):
		if not dbName.startswith("test_"):
			raise RuntimeError("only test databases can be removed")
		if not is_db_name_safe(dbName):
			raise RuntimeError("Invalid name was used:")
		self.conn.exec_driver_sql(f"DROP DATABASE IF EXISTS {dbName}")

	def revoke_all_roles(self):
		self.conn.exec_driver_sql(
			f"REVOKE ALL PRIVILEGES, GRANT OPTION "
			f"FROM {DbUsers.API_USER.format_user()}, "
			f"{DbUsers.JANITOR_USER.format_user()}, "
			f"{DbUsers.OWNER_USER.format_user()}"
		)

	def drop_user(self, user: DbUsers):
		self.conn.exec_driver_sql(f"DROP USER IF EXISTS {user.format_user()}")

	def drop_all_users(self):
		for user in DbUsers:
			self.drop_user(user)

class DbOwnerConnectionService:

	def __init__(self, dbName: str, echo: bool=False) -> None:
		self.dbName = dbName
		self.echo = echo
		self.conn = self.get_owner_connection()

	def get_owner_connection(self) -> Connection:
		dbPass = ConfigAcessors.db_pass_owner()
		if not dbPass:
			raise RuntimeError("The system is not configured correctly for that.")
		if not is_db_name_safe(self.dbName):
			raise RuntimeError("Invalid name was used")
		owner = DbUsers.OWNER_USER.value
		engine = create_engine(
			f"mysql+pymysql://{owner}:{dbPass}@localhost/{self.dbName}",
			echo=self.echo,
			connect_args={
				"client_flag": CLIENT.MULTI_STATEMENTS | CLIENT.MULTI_RESULTS
			},
			poolclass=NullPool
		)
		return engine.connect()

	def __enter__(self) -> "DbOwnerConnectionService":
		return self

	def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any):
		self.conn.close()

	def flush_privileges(self):
		self.conn.exec_driver_sql("FLUSH PRIVILEGES")

	def create_tables(self):
		metadata.create_all(self.conn.engine)

	def load_script_contents(self, scriptId: SqlScripts) -> str:
		if not is_db_name_safe(self.dbName):
			raise RuntimeError("Invalid name was used")
		templateNoComments = re.sub(
			r"^[ \t]*--.*\n",
			"",
			TemplateService.load_sql_script_content(
				scriptId
			),
			flags=re.MULTILINE
		)
		return templateNoComments.replace("<dbName>", self.dbName)
	
	def run_defined_api_user_script(self, scriptId: SqlScripts):
		script = self.load_script_contents(scriptId)\
			.replace("<apiUser>", DbUsers.API_USER("localhost"))
		self.conn.exec_driver_sql(script)

	def run_defined_janitor_user_script(self, scriptId: SqlScripts):
		script = self.load_script_contents(scriptId)\
			.replace("<janitorUser>", DbUsers.JANITOR_USER("localhost"))
		self.conn.exec_driver_sql(script)

	def run_defined_script(self, scriptId: SqlScripts):
		script = self.load_script_contents(scriptId)\
			.replace("|","")\
			.replace("DELIMITER","")

		self.conn.exec_driver_sql(script)



def setup_database(dbName: str):
	with DbRootConnectionService() as rootConnService:
		rootConnService.create_db(dbName)
		rootConnService.create_owner()
		rootConnService.create_app_users()
		rootConnService.grant_owner_roles(dbName)

	with DbOwnerConnectionService(dbName, echo=False) as ownerConnService:
		ownerConnService.create_tables()

