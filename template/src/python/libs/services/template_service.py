import hashlib
from pathlib import Path
from .process_service import ProcessService
from <%= projectNameSnake %>.dtos_and_utilities import (
	ConfigAcessors,
	SqlScripts
)


class TemplateService:

	def __init__(self) -> None:
		pass


	@staticmethod
	def load_sql_script_content(script: SqlScripts) -> str:
		sqlScriptsDir = ConfigAcessors.sql_script_dir()
		txt = Path(f"{sqlScriptsDir}/{script.file_name}").read_text()
		checksum = hashlib.md5(txt.encode("utf-8")).hexdigest()
		if checksum != script.checksum:
			raise RuntimeError(f"{script.file_name} is missing")
		return txt