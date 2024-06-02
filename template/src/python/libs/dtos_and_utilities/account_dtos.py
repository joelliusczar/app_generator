from typing import (
	Any,
	List,
	Optional,
	Iterator,
	Union,
	Collection
)
from pydantic import (
	field_validator,
	field_serializer,
	SerializationInfo,
	SerializeAsAny,
	Field
)

from .user_role_def import UserRoleDef, RulePriorityLevel, UserRoleDomain
from .validation_functions import min_length_validator_factory
from .simple_functions import (
	get_duplicates,
	validate_email,
)
from .generic_dtos import FrozenIdItem, FrozenBaseClass
from .action_rule_dtos import (
	ActionRule
)


class AccountInfoBase(FrozenBaseClass):
	username: str
	email: str
	displayname: Optional[str]=""

class AccountInfoSecurity(AccountInfoBase):
	roles: List[ActionRule]=Field(default_factory=list)
	dirroot: Optional[str]=None

	@property
	def preferredName(self) -> str:
		return self.displayname or self.username

	@property
	def isadmin(self) -> bool:
		return any(
			UserRoleDef.ADMIN.conforms(r.name) \
				for r in self.roles
		)


	def has_roles(self, *roles: UserRoleDef) -> bool:
		if self.isadmin:
			return True
		for role in roles:
			if all(r.name != role.value or (r.name == role.value and r.blocked) \
				for r in self.roles
			):
				return False
		return True
	
	@field_serializer(
		"roles",
		return_type=SerializeAsAny[List[ActionRule]]
	)
	def serialize_roles(
		self,
		value: List[ActionRule],
		_info: SerializationInfo
	):
		return value

class AccountInfo(AccountInfoSecurity, FrozenIdItem):
	...


class AuthenticatedAccount(AccountInfoSecurity):
	'''
	This AccountInfo is only returned after successful authentication.
	'''
	access_token: str=""
	token_type: str=""
	lifetime: float=0
	login_timestamp: float=0


class AccountCreationInfo(AccountInfoSecurity):
	'''
	This AccountInfo is only to the server to create an account.
	Password is clear text here because it hasn't been hashed yet.
	No id property because no id has been assigned yet.
	This class also has validation on several of its properties.
	'''
	password: str=""

	def scrubed_dict(self) -> dict[str, Any]:
		return {
			"username": self.username,
			"email": self.email,
			"displayname": self.displayname,
			"roles": self.roles
		}

	@field_validator("email")
	def check_email(cls, v: str) -> str:
		valid = validate_email(v)
		if not valid or not valid.email:
			raise ValueError("Email is null")
		return valid.email #pyright: ignore [reportGeneralTypeIssues]

	_pass_len = field_validator( #pyright: ignore [reportUnknownVariableType]
		"password"
	)(min_length_validator_factory(6, "Password"))


	@field_validator("roles")
	def are_all_roles_allowed(cls, v: List[str]) -> List[str]:
		roleSet = UserRoleDef.as_set()
		duplicate = next(get_duplicates(
			UserRoleDef.role_dict(r)["name"] for r in v
		), None)
		if duplicate:
			raise ValueError(
				f"{duplicate[0]} has been added {duplicate[1]} times "
				"but it is only legal to add it once."
			)
		for role in v:
			extracted = UserRoleDef.role_dict(role)["name"]
			if extracted not in roleSet:
				raise ValueError(f"{role} is an illegal role")
		return v

class PasswordInfo(FrozenBaseClass):
	oldpassword: str
	newpassword: str

class UserHistoryActionItem(FrozenBaseClass):
	userid: int
	action: str
	timestamp: float

