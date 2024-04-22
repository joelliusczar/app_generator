####### This file is generated. #######
# edit regen_file_reference_file #
# in <%= devOpsUtilitiesFile %>.sh and rerun
from enum import Enum

class SqlScripts(Enum):

	@property
	def file_name(self) -> str:
		return self.value[0]

	@property
	def checksum(self) -> str:
		return self.value[1]
