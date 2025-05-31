####### This file is generated. #######
from enum import Enum

class SqlScripts(Enum):

	@property
	def file_name(self) -> str:
		return self.value[0]

	@property
	def checksum(self) -> str:
		return self.value[1]
