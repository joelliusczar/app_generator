import os
import re
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from <%= projectName %>_libs.dtos_and_utilities import (
	DbUsers
)


class EnvManager:

	@classmethod
	def app_root(cls) -> str:
		if EnvManager.test_flag():
			return os.environ["<%= ucPrefix %>_TEST_ROOT"]
		return os.environ["<%= ucPrefix %>_APP_ROOT"]
	
	@classmethod
	def relative_content_home(cls) -> str:
		contentHome = os.environ["<%= ucPrefix %>_CONTENT_HOME"]
		return contentHome

	@classmethod
	def absolute_content_home(cls) -> str:
		return f"{EnvManager.app_root()}/{EnvManager.relative_content_home()}"

	@classmethod
	def db_setup_pass(cls) -> str:
		return os.environ.get("__DB_SETUP_PASS__", "")

	@classmethod
	def db_pass_api(cls) -> str:
		return os.environ.get("<%= ucPrefix %>_DB_PASS_API", "")

	@classmethod
	def db_pass_owner(cls) -> str:
		return os.environ.get("<%= ucPrefix %>_DB_PASS_OWNER", "")

	@classmethod
	def templates_dir(cls) -> str:
		templateDir = os.environ["<%= ucPrefix %>_TEMPLATES_DIR_CL"]
		return f"{EnvManager.app_root()}/{templateDir}"


	@classmethod
	def sql_script_dir(cls) -> str:
		moduleDir = os.environ["<%= ucPrefix %>_SQL_SCRIPTS_DIR_CL"]
		return f"{EnvManager.app_root()}/{moduleDir}"

	@classmethod
	def db_name(cls) -> str:
		return os.environ["<%= ucPrefix %>_DATABASE_NAME"]

	@classmethod
	def test_flag(cls) -> bool:
		return os.environ.get("__TEST_FLAG__","false") == "true"

	@classmethod
	def secret_key(cls) -> str:
		return os.environ["<%= ucPrefix %>_AUTH_SECRET_KEY"]

	@classmethod
	def get_configured_api_connection(
		cls,
		dbName: str,
		echo: bool=False
	) -> Connection:
		dbPass = EnvManager.db_pass_api()
		if not dbPass:
			raise RuntimeError("The system is not configured correctly for that.")
		engine = create_engine(
			f"mysql+pymysql://{DbUsers.API_USER()}:{dbPass}@localhost/{dbName}",
			echo=echo,
		)
		conn = engine.connect()
		return conn


	@staticmethod
	def read_config_value(confLocation: str, key: str) -> str:
		passLines: list[str] = []
		with open(confLocation, "r") as configFile:
			for line in configFile:
				if f"<{key}>" in line or passLines:
					passLines.append(line)
				if f"</{key}>" in line:
					break
		segment = "".join(passLines)
		match = re.search(rf"<{key}>([^<]+)</{key}>", segment)
		if match:
			g = match.groups()
			return g[0]
		return ""