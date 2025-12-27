#pyright: reportMissingTypeStubs=false
from typing import (
	Iterator,
	Tuple,
	Optional,
	Union,
	Callable
)
from urllib import parse
from fastapi import (
	Depends,
	HTTPException,
	status,
	Query,
	Request,
	Path
)
from sqlalchemy.engine import Connection
from <%= projectNameSnake %>.services import (
	AccountsService,
	CurrentUserProvider,
	ProcessService,
	UserActionsHistoryService
)
from <%= projectNameSnake %>.dtos_and_utilities import (
	AccountInfo,
	ConfigAcessors,
	build_error_obj,
	UserRoleDomain,
	ActionRule,
	get_datetime,
	UserRoleDef,
	int_or_str
)
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose.exceptions import ExpiredSignatureError
from api_error import (
	build_not_logged_in_error,
	build_not_wrong_credentials_error,
	build_expired_credentials_error,
	build_wrong_permissions_error,
	build_too_many_requests_error
)
from datetime import datetime


oauth2_scheme = OAuth2PasswordBearer(
	tokenUrl="accounts/open",
	auto_error=False
)


def subject_user_key_path(
	subjectuserkey: Union[int, str]  = Path()
) -> Union[int, str]:
	return int_or_str(subjectuserkey)

def subject_user_key_query(
	subjectuserkey: Union[int, str]  = Query()
) -> Union[int, str]:
	return int_or_str(subjectuserkey)

def datetime_provider() -> Callable[[], datetime]:
	return get_datetime

def get_configured_db_connection(
	configAcessors: ConfigAcessors=Depends(ConfigAcessors)
) -> Iterator[Connection]:
	if not configAcessors:
		configAcessors = ConfigAcessors()
	conn = configAcessors.get_configured_api_connection("<%= projectNameSnake %>_db")
	try:
		yield conn
	finally:
		conn.close()

def current_user_provider(
	user: AccountInfo = Depends(get_current_user_simple)
) -> CurrentUserProvider:
	return CurrentUserProvider(user.id)



def accounts_service(
	conn: Connection=Depends(get_configured_db_connection),
	currentUserProvider : CurrentUserProvider = Depends(current_user_provider)
) -> AccountsService:
	return AccountsService(conn, currentUserProvider)

def process_service() -> ProcessService:
	return ProcessService()

def user_actions_history_service(
	conn: Connection=Depends(get_configured_db_connection)
) -> UserActionsHistoryService:
	return UserActionsHistoryService(conn)

def get_user_from_token(
	token: str,
	accountsService: AccountsService
) -> Tuple[AccountInfo, float]:
	if not token:
		raise build_not_logged_in_error()
	try:
		user, expiration = accountsService.get_user_from_token(token)
		if not user:
			raise build_not_wrong_credentials_error()
		return user, expiration
	except ExpiredSignatureError:
		raise build_expired_credentials_error()

def get_current_user_simple(
	request: Request,
	token: str = Depends(oauth2_scheme),
	accountsService: AccountsService = Depends(accounts_service)
) -> AccountInfo:
	cookieToken = request.cookies.get("access_token", None)
	user, _ = get_user_from_token(
		token or parse.unquote(cookieToken or ""),
		accountsService
	)
	return user

def get_optional_user_from_token(
	request: Request,
	token: str = Depends(oauth2_scheme),
	accountsService: AccountsService = Depends(accounts_service),
) -> Optional[AccountInfo]:
	cookieToken = request.cookies.get("access_token", None)
	if not token and not cookieToken:
		return None
	try:
		user, _ = accountsService.get_user_from_token(
			token or parse.unquote(cookieToken or "")
		)
		return user
	except ExpiredSignatureError:
		raise build_expired_credentials_error()

def __open_user_from_request__(
	userkey: Union[int, str, None],
	accountsService: AccountsService
) -> Optional[AccountInfo]:
	if userkey:
		try:
			userkey = int(userkey)
			owner = accountsService.get_account_for_edit(userkey)
		except:
			owner = accountsService.get_account_for_edit(userkey)
		if owner:
			return owner
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=[build_error_obj(f"User with key {userkey} not found")
			]
		)
	return None

def get_from_path_subject_user(
	subjectuserkey: Union[int, str] = Depends(subject_user_key_path),
	accountsService: AccountsService = Depends(accounts_service)
) -> AccountInfo:
	user = __open_user_from_request__(subjectuserkey, accountsService)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=[build_error_obj("subjectuserkey missing")
			]
		)
	return user


def get_from_query_subject_user(
	subjectuserkey: Union[int, str] = Depends(subject_user_key_query),
	accountsService: AccountsService = Depends(accounts_service)
) -> AccountInfo:
	user = __open_user_from_request__(subjectuserkey, accountsService)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=[build_error_obj("subjectuserkey missing")
			]
		)
	return user


def get_current_user(
	user: AccountInfo = Depends(get_current_user_simple)
) -> AccountInfo:
	return user

def get_user_with_simple_scopes(
	securityScopes: SecurityScopes,
	user: AccountInfo = Depends(get_current_user_simple)
) -> AccountInfo:
	if user.isadmin:
		return user
	for scope in securityScopes.scopes:
		if not any(r for r in user.roles if r.name == scope):
			raise build_wrong_permissions_error()
	return user

def get_user_with_rate_limited_scope(
	securityScopes: SecurityScopes,
	user: AccountInfo = Depends(get_current_user_simple),
	userActionHistoryService: UserActionsHistoryService =
		Depends(user_actions_history_service)
) -> AccountInfo:
	if user.isadmin:
		return user
	scopeSet = set(securityScopes.scopes)
	rules = ActionRule.sorted((r for r in user.roles if r.name in scopeSet))
	if not rules:
		raise build_wrong_permissions_error()
	timeoutLookup = \
		userActionHistoryService.calc_lookup_for_when_user_can_next_do_action(
			user.id,
			rules
		)
	for scope in scopeSet:
		if scope in timeoutLookup:
			whenNext = timeoutLookup[scope]
			if whenNext is None:
				raise build_wrong_permissions_error()
			if whenNext > 0:
				currentTimestamp = get_datetime().timestamp()
				timeleft = whenNext - currentTimestamp
				raise build_too_many_requests_error(int(timeleft))
	return user

def impersonated_user_id(
	impersonateduserid: Optional[int],
	user: AccountInfo = Depends(get_current_user_simple)
) -> Optional[int]:
	if user.isadmin or any(r.conforms(UserRoleDef.USER_IMPERSONATE.value) \
			for r in user.roles):
		return impersonateduserid
	return None


def get_account_if_has_scope(
	securityScopes: SecurityScopes,
	subjectuserkey: Union[int, str] = Depends(subject_user_key_path),
	currentUser: AccountInfo = Depends(get_current_user_simple),
	accountsService: AccountsService = Depends(accounts_service)
) -> AccountInfo:
	isCurrentUser = subjectuserkey == currentUser.id or\
		subjectuserkey == currentUser.username
	scopeSet = {s for s in securityScopes.scopes}
	hasEditRole = currentUser.isadmin or\
		any(r.name in scopeSet for r in currentUser.roles)
	if not isCurrentUser and not hasEditRole:
		raise build_wrong_permissions_error()
	prev = accountsService.get_account_for_edit(subjectuserkey) \
		if subjectuserkey else None
	if not prev:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=[build_error_obj("Account not found")],
		)
	return prev

def get_account_if_has_scope(
	securityScopes: SecurityScopes,
	subjectuserkey: Union[int, str] = Depends(subject_user_key_path),
	currentUser: AccountInfo = Depends(get_current_user_simple),
	accountsService: AccountsService = Depends(accounts_service)
) -> AccountInfo:
	isCurrentUser = subjectuserkey == currentUser.id or\
		subjectuserkey == currentUser.username
	scopeSet = {s for s in securityScopes.scopes}
	hasEditRole = currentUser.isadmin or\
		any(r.name in scopeSet for r in currentUser.roles)
	if not isCurrentUser and not hasEditRole:
		raise build_wrong_permissions_error()
	prev = accountsService.get_account_for_edit(subjectuserkey) \
		if subjectuserkey else None
	if not prev:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=[build_error_obj("Account not found")],
		)
	return prev

def get_page(
	page: int = 1,
) -> int:
	if page > 0:
		page -= 1
	return page

def extract_ip_address(request: Request) -> Tuple[str, str]:
	candidate = request.headers.get("x-real-ip", "")
	if not candidate and request.client:
		candidate = request.client.host
	try:
		address = ipaddress.ip_address(candidate)
		if isinstance(address, ipaddress.IPv4Address):
			return (candidate, "")
		else:
			return ("", candidate)
	except:
		return ("","")


def get_tracking_info(request: Request):
	userAgent = request.headers["user-agent"]
	ipaddresses = extract_ip_address(request)
	
	return TrackingInfo(
		userAgent,
		ipv4Address=ipaddresses[0],
		ipv6Address=ipaddresses[1]
	)

def check_back_key(
	x_back_key: str = Header(),
	envManager: ConfigAcessors=Depends(ConfigAcessors)
):
	if not envManager:
		envManager = ConfigAcessors()
	if envManager.back_key() != x_back_key:
		raise build_wrong_permissions_error()