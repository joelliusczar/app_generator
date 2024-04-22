import os
import platform
import subprocess
import random
from enum import Enum
from itertools import dropwhile, islice
from typing import Optional
from <%= projectName %>_libs.dtos_and_utilities import (
	get_non_simple_chars
)
from .env_manager import EnvManager
import <%= projectName %>_libs.dtos_and_utilities.logging as logging


class PackageManagers(Enum):
	APTGET = "apt-get"
	PACMAN = "pacman"
	HOMEBREW = "homebrew"



class ProcessService:


	@staticmethod
	def noop_mode() -> bool:
		return platform.system() == "Darwin"

	@staticmethod
	def get_pid() -> int:
		if ProcessService.noop_mode():
			return random.randint(0, 1000)
		return os.getpid()

	@staticmethod
	def end_process(procId: int) -> None:
		if ProcessService.noop_mode():
			return
		try:
			os.kill(procId, 15)
		except:
			pass

	@staticmethod
	def get_pkg_mgr() -> Optional[PackageManagers]:
		if platform.system() == "Linux":
			result = subprocess.run(
				["which", PackageManagers.PACMAN.value],
				stdout=subprocess.DEVNULL
			)
			if result.returncode == 0:
				return PackageManagers.PACMAN
			result = subprocess.run(
				["which", PackageManagers.APTGET.value],
				stdout=subprocess.DEVNULL
			)
			if result.returncode == 0:
				return PackageManagers.APTGET
		elif platform.system() == "Darwin":
			return PackageManagers.HOMEBREW
		return None