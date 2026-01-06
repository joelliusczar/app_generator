#pyright: reportMissingTypeStubs=false
import ipaddress
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
	Path,
	Header
)
from sqlalchemy.engine import Connection
from <%= projectNameSnake %>.services import (
	AccountAccessService,
	AccountManagementService,
	AccountTokenCreator,
	ActionsHistoryManagementService,
	ActionsHistoryQueryService,
	BasicUserProvider,
	CurrentUserProvider,
	CurrentUserTrackingService,
	JobsService,
	ProcessService,
	
)
from <%= projectNameSnake %>.dtos_and_utilities import (
	AccountInfo,
	ActionRule,
	build_error_obj,
	ConfigAcessors,
	get_datetime,
	NotLoggedInError,
	UserRoleDef,
	int_or_str,
	TrackingInfo,
	SimpleQueryParameters,
	UserRoleDomain,
	WrongPermissionsError,
)
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose.exceptions import ExpiredSignatureError
from api_error import (
	build_not_logged_in_error,
	build_not_wrong_credentials_error,
	build_expired_credentials_error,
	build_wrong_permissions_error,
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


def owner_key_path(
	ownerkey: Union[int, str]  = Path()
) -> Union[int, str]:
	return int_or_str(ownerkey)


def owner_key_query(
	ownerkey: Union[int, str, None]  = Query(None)
) -> Union[int, str, None]:
	if ownerkey is None:
		return ownerkey
	return int_or_str(ownerkey)


def datetime_provider() -> Callable[[], datetime]:
	return get_datetime


def get_configured_db_connection(
	envManager: ConfigAcessors=Depends(ConfigAcessors)
) -> Iterator[Connection]:
	if not envManager:
		envManager = ConfigAcessors()
	conn = envManager.get_configured_api_connection("musical_chairs_db")
	try:
		yield conn
	finally:
		conn.close()


def account_access_service(
	conn: Connection=Depends(get_configured_db_connection),
) -> AccountAccessService:
	return AccountAccessService(conn)


def get_user_from_token(
	token: str,
	accountAccessService: AccountAccessService
) -> Tuple[AccountInfo, float]:
	if not token:
		raise build_not_logged_in_error()
	try:
		user, expiration = accountAccessService.get_user_from_token(token)
		if not user:
			raise build_not_wrong_credentials_error()
		return user, expiration
	except ExpiredSignatureError:
		raise build_expired_credentials_error()


def get_current_user_simple(
	request: Request,
	token: str = Depends(oauth2_scheme),
	accountsAccessService: AccountAccessService = Depends(account_access_service)
) -> AccountInfo:
	cookieToken = request.cookies.get("access_token", None)
	user, _ = get_user_from_token(
		token or parse.unquote(cookieToken or ""),
		accountsAccessService
	)
	return user


def get_optional_user_from_token(
	request: Request,
	token: str = Depends(oauth2_scheme),
	accountAccessService: AccountAccessService = Depends(account_access_service),
) -> Optional[AccountInfo]:
	cookieToken = request.cookies.get("access_token", None)
	if not token and not cookieToken:
		return None
	try:
		user, _ = accountAccessService.get_user_from_token(
			token or parse.unquote(cookieToken or "")
		)
		return user
	except ExpiredSignatureError:
		raise build_expired_credentials_error()


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


def current_user_tracking_service(
	trackingInfo: TrackingInfo = Depends(get_tracking_info)
) -> CurrentUserTrackingService:
	return CurrentUserTrackingService(trackingInfo)


def actions_history_query_service(
	conn: Connection=Depends(get_configured_db_connection)
) -> ActionsHistoryQueryService:
	return ActionsHistoryQueryService(conn)


def basic_user_provider(
	user: AccountInfo = Depends(get_optional_user_from_token),
) -> BasicUserProvider:
	return BasicUserProvider(user)




def current_user_provider(
	securityScopes: SecurityScopes,
	basicUserProvider: BasicUserProvider = Depends(basic_user_provider),
	currentUserTrackingService: CurrentUserTrackingService = Depends(
		current_user_tracking_service
	),
	actionsHistoryQueryService: ActionsHistoryQueryService = Depends(
		actions_history_query_service
	),
) -> CurrentUserProvider:
	return CurrentUserProvider(
		basicUserProvider,
		currentUserTrackingService,
		actionsHistoryQueryService,
		set(securityScopes.scopes)
	)


def __check_scope__(
	securityScopes: SecurityScopes,
	currentUser: AccountInfo,
):
	scopeSet = {s for s in securityScopes.scopes}
	hasRole = currentUser.isadmin or\
		any(r.name in scopeSet for r in currentUser.roles)
	if not hasRole:
		raise build_wrong_permissions_error()


def check_scope(
	securityScopes: SecurityScopes,
	currentUser: AccountInfo = Depends(get_current_user_simple),
):
	__check_scope__(securityScopes, currentUser)


def actions_history_management_service(
	conn: Connection=Depends(get_configured_db_connection),
	currentUserTrackingService: CurrentUserTrackingService = Depends(
		current_user_tracking_service
	),
	userProvider: CurrentUserProvider = Depends(
		current_user_provider
	)
) -> ActionsHistoryManagementService:
	return ActionsHistoryManagementService(
		conn,
		currentUserTrackingService,
		userProvider
	)


def account_management_service(
	conn: Connection=Depends(get_configured_db_connection),
	userActionHistoryService: ActionsHistoryManagementService =
		Depends(actions_history_management_service),
	userProvider: CurrentUserProvider = Depends(
		current_user_provider
	),
	accountsAccessService: AccountAccessService = Depends(account_access_service)
) -> AccountManagementService:
	return AccountManagementService(
		conn,
		userProvider,
		accountsAccessService,
		userActionHistoryService,
	)


def account_token_creator(
	conn: Connection=Depends(get_configured_db_connection),
	userActionHistoryService: ActionsHistoryManagementService =
		Depends(actions_history_management_service)
) -> AccountTokenCreator:
	return AccountTokenCreator(conn, userActionHistoryService)



def job_service(
	conn: Connection=Depends(get_configured_db_connection),
	fileService: FileService=Depends(file_service)
) -> JobsService:
	return JobsService(conn, fileService)


def process_service() -> ProcessService:
	return ProcessService()


def get_optional_prefix(
	prefix: Optional[str]=Query(None),
	nodeId: Optional[str]=Query(None)
) -> Optional[str]:
	if prefix is not None:
		return prefix
	if nodeId is not None:
		translated = nodeId
		decoded = urlsafe_b64decode(translated).decode()
		return decoded


def get_prefix(
	prefix: Optional[str]=Query(None),
	nodeId: Optional[str]=Query(None)
) -> str:
	prefix = get_optional_prefix(prefix, nodeId)
	if prefix is not None:
		return prefix
	raise HTTPException(
		status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
		detail=[build_error_obj("prefix and nodeId both missing")
		]
	)


def __open_user_from_request__(
	userkey: Union[int, str, None],
	accountManagementService: AccountManagementService
) -> Optional[AccountInfo]:
	if userkey:
		try:
			userkey = int(userkey)
			owner = accountManagementService.get_account_for_edit(userkey)
		except:
			owner = accountManagementService.get_account_for_edit(userkey)
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
	accountManagementService: AccountManagementService = Depends(
		account_management_service
	)
) -> AccountInfo:
	user = __open_user_from_request__(subjectuserkey, accountManagementService)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=[build_error_obj("subjectuserkey missing")
			]
		)
	return user


def get_from_query_subject_user(
	subjectuserkey: Union[int, str] = Depends(subject_user_key_query),
	accountManagementService: AccountManagementService = Depends(
		account_management_service
	)
) -> AccountInfo:
	user = __open_user_from_request__(subjectuserkey, accountManagementService)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=[build_error_obj("subjectuserkey missing")
			]
		)
	return user


def check_subjectuser(
	securityScopes: SecurityScopes,
	subjectuserkey: Union[int, str] = Depends(subject_user_key_path),
	currentUser: AccountInfo = Depends(get_current_user_simple),
):
	isCurrentUser = subjectuserkey == currentUser.id or\
		subjectuserkey == currentUser.username
	scopeSet = {s for s in securityScopes.scopes}
	hasEditRole = currentUser.isadmin or\
		any(r.name in scopeSet for r in currentUser.roles)
	if not isCurrentUser and not hasEditRole:
		raise build_wrong_permissions_error()


def get_page_num(
	page: int = 1,
) -> int:
	if page > 0:
		page -= 1
	return page


def check_back_key(
	x_back_key: str = Header(),
	envManager: ConfigAcessors=Depends(ConfigAcessors)
):
	if not envManager:
		envManager = ConfigAcessors()
	if envManager.back_key() != x_back_key:
		raise build_wrong_permissions_error()


def get_query_params(
	limit: int = 50,
	page: int = Depends(get_page_num),
	orderby: Optional[str]=None,
	sortdir: Optional[str]=None,
) -> SimpleQueryParameters:
		return SimpleQueryParameters(
			page=page,
			limit=limit,
			orderby=orderby,
			sortdir=sortdir
		)

def get_secured_query_params(
	queryParams: SimpleQueryParameters=Depends(get_query_params),
	currentUserProvider : CurrentUserProvider = Depends(current_user_provider)
) -> SimpleQueryParameters:
	currentUserProvider.get_rate_limited_user()
	return queryParams


def check_rate_limit(
		currentUserProvider : CurrentUserProvider = Depends(current_user_provider)
):
	currentUserProvider.get_rate_limited_user()