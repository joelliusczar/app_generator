from enum import Enum
from typing import (
	Union,
	Set,
	Tuple,
	Optional
)
from .type_aliases import (
	s2sDict,
	simpleDict
)
from .simple_functions import role_dict

class MinItemSecurityLevel(Enum):
	#these values should align with RulePriorityLevel
	PUBLIC = 0
	# SITE permissions should be able to overpower ANY_USER level restrictions
	ANY_USER = 9
	# ANY_STATION should be able to overpower RULED_USER
	RULED_USER = 19
	FRIEND_USER = 29 # not used
	# STATION_PATH should be able to overpower INVITED_USER
	INVITED_USER = 39
	OWENER_USER = 49
	#only admins should be able to see these items
	LOCKED = 59

class RulePriorityLevel(Enum):
	NONE = 0
	USER = 10
	SITE = 20
	SUPER = 30

class UserRoleDomain(Enum):
	Site = "site"

	def conforms(self, candidate: str) -> bool:
		return candidate.startswith(self.value)


class UserRoleDef(Enum):
	ADMIN = "admin"
	SITE_USER_ASSIGN = f"{UserRoleDomain.Site.value}:userassign"
	SITE_USER_LIST = f"{UserRoleDomain.Site.value}:userlist"
	SITE_PLACEHOLDER = f"{UserRoleDomain.Site.value}:placeholder"
	USER_EDIT = f"{UserRoleDomain.Site.value}:useredit"
	USER_LIST = "user:list"
	USER_IMPERSONATE = "user:impersonate"

	def __call__(self, **kwargs: Union[str, int]) -> str:
		return self.modded_value(**kwargs)

	def conforms(self, candidate: str) -> bool:
		return candidate.startswith(self.value)

	@property
	def nameValue(self):
		return self.value

	@staticmethod
	def as_set(domain: Optional[str]=None) -> Set[str]:
		return {r.value for r in UserRoleDef \
			if not domain or r.value.startswith(domain)}

	@staticmethod
	def role_dict(role: str) -> s2sDict:
		return role_dict(role)

	@staticmethod
	def role_str(roleDict: simpleDict) -> str:
		return ";".join(sorted(f"{k}={v}" for k,v in roleDict.items() if v != ""))

	@staticmethod
	def extract_role_segments(role: str) -> Tuple[str, int]:
		roleDict = UserRoleDef.role_dict(role)
		if "name" in roleDict:
			nameValue = roleDict["name"]
			mod = int(roleDict["mod"]) if "mod" in roleDict else -1
			return (nameValue, mod)
		return ("", 0)

	def modded_value(
		self,
		**kwargs: Optional[Union[str, int]]
	) -> str:
		if "name" in kwargs and kwargs["name"] != self.value:
			raise RuntimeError("Name should not be provided.")
		kwargs["name"] = self.value
		return UserRoleDef.role_str(kwargs)