from .actions_history_query_service import ActionsHistoryQueryService
from .basic_user_provider import BasicUserProvider, Impersonation
from <%= projectNameSnake %>.dtos_and_utilities import (
	AccountInfo,
	ActionRule,
	get_datetime,
	NotLoggedInError,
	TooManyRequestsError,
	TrackingInfo,
	WrongPermissionsError,
)
from <%= projectNameSnake %>.protocols import (
	TrackingInfoProvider,
	UserProvider
)
from typing import (Literal, Optional, overload)

class CurrentUserProvider(TrackingInfoProvider, UserProvider):

	def __init__(
		self,
		basicUserProvider: BasicUserProvider,
		trackingInfoProvider: TrackingInfoProvider,
		actionsHistoryQueryService: ActionsHistoryQueryService,
		securityScopes: Optional[set[str]] = None,
	) -> None:
		self.basic_user_provider = basicUserProvider
		self.__path_rule_loaded_user__: Optional[AccountInfo] = None
		self.tracking_info_provider = trackingInfoProvider
		self.actions_history_query_service = actionsHistoryQueryService
		self.get_datetime = get_datetime
		self.security_scopes = securityScopes or set()

	@overload
	def current_user(self) -> AccountInfo:
		...

	@overload
	def current_user(self, optional: Literal[False]) -> AccountInfo:
		...

	@overload
	def current_user(self, optional: Literal[True]) -> Optional[AccountInfo]:
		...

	def current_user(self, optional: bool=False) -> Optional[AccountInfo]:
		return self.basic_user_provider.current_user(optional=optional)
	

	def is_loggedIn(self) -> bool:
		return self.basic_user_provider.is_loggedIn()


	def set_user(self, user: AccountInfo):
		self.basic_user_provider.set_user(user)


	def optional_user_id(self) -> Optional[int]:
		return self.basic_user_provider.optional_user_id()


	def tracking_info(self) -> TrackingInfo:
		return self.tracking_info_provider.tracking_info()


	def get_rate_limited_user(self) -> AccountInfo:
		user = self.current_user()
		if user.isadmin:
			return user
		scopeSet = self.security_scopes
		rules = ActionRule.sorted((r for r in user.roles if r.name in scopeSet))
		if not rules and scopeSet:
			raise WrongPermissionsError()
		timeoutLookup = \
			self.actions_history_query_service\
				.calc_lookup_for_when_user_can_next_do_action(
					user.id,
					rules
				)
		for scope in scopeSet:
			if scope in timeoutLookup:
				whenNext = timeoutLookup[scope]
				if whenNext is None:
					raise WrongPermissionsError()
				if whenNext > 0:
					currentTimestamp = get_datetime().timestamp()
					timeleft = whenNext - currentTimestamp
					raise TooManyRequestsError(int(timeleft))
		return user


	def impersonate(self, user: AccountInfo) -> Impersonation:
		return self.basic_user_provider.impersonate(user)



