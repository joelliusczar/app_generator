import { SubjectUserParams } from "./Types/user_types";
import { StringObject } from "./Types/generic_types";


//these vars need to be prefixed VITE
export const baseAddress = import.meta.env.VITE_BASE_ADDRESS;
export const apiVersion = import.meta.env.VITE_API_VERSION;
export const apiAddress = import.meta.env.DEV ?
	baseAddress : `${baseAddress}/api/${apiVersion}`;




export const CallStatus = {
	loading: "loading",
	done: "done",
	failed: "failed",
	idle: "idle",
};

export const DomRoutes = {
	userNew: () => "/accounts/new",
	userEdit: ({ subjectuserkey }: SubjectUserParams) =>
		`/accounts/edit/${subjectuserkey}`,
	userLogin: () => "/accounts/login",
	userRoles: ({ subjectuserkey }: SubjectUserParams) =>
		`/users/roles/${subjectuserkey}`,
	userList: () => "/accounts/list",
	notFound: () => "/not-found",
};

export const UserRoleDomain: StringObject = {
	SITE: "site",
};

export const UserRoleDef: StringObject = {
	ADMIN: "admin",
	SITE_USER_ASSIGN: `${UserRoleDomain.SITE}:userassign`,
	SITE_USER_LIST: `${UserRoleDomain.SITE}:userlist`,
	SITE_PLACEHOLDER: `${UserRoleDomain.SITE}:placeholder`,
	USER_LIST: "user:list",
	USER_EDIT: "user:edit",
	USER_IMPERSONATE: "user:impersonate",
};

export const MinItemSecurityLevel = {
	PUBLIC: 0,
	// SITE permissions should be able to overpower ANY_USER level restrictions
	ANY_USER: 9,
	// ANY_STATION should be able to overpower RULED_USER
	RULED_USER: 19,
	FRIEND_USER: 29, // not used
	// STATION_PATH should be able to overpower INVITED_USER
	INVITED_USER: 39,
	OWENER_USER: 49,
	//only admins should be able to see these items
	LOCKED: 59,
};