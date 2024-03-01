import React from "react";
import { Route, Routes, NavLink, useNavigate } from "react-router-dom";
import { List, ListItem } from "@mui/material";
import { UserNew } from "../Users/UserNew";
import { UserEdit } from "../Users/UserEdit";
import { LoginForm } from "../Users/UserLoginForm";
import { UserList } from "../Users/UserList";
import { NotFound } from "../Shared/RoutingErrors";
import { DomRoutes, UserRoleDef } from "../../constants";
import { PrivateRoute } from "../Shared/PrivateRoute";
import {
	useCurrentUser,
	useHasAnyRoles,
} from "../../Context_Providers/AuthContext/AuthContext";
import {
	SiteUserRoleAssignmentTable,
} from "../Users/SiteUserRoleAssignmentTable";


export function NavMenu() {

	const currentUser = useCurrentUser();

	const canOpenAccountList = useHasAnyRoles([
		UserRoleDef.USER_EDIT,
		UserRoleDef.USER_LIST,
	]);

	return (
		<List>
			{canOpenAccountList &&
			<ListItem component={NavLink} to={DomRoutes.userList()}>
				User List
			</ListItem>}
		</List>
	);
}

export function AppRoutes() {


	const currentUser = useCurrentUser();


	const navigate = useNavigate();


	return (
		<Routes>
			{!currentUser.username &&<Route
				path={DomRoutes.userNew()}
				element={<UserNew />}
			/>}
			{!currentUser.username && <Route
				path={DomRoutes.userLogin()}
				element={<LoginForm
					afterSubmit={() => navigate("")}
				/>}
			/>}
			{currentUser.username &&
			<Route
				path={DomRoutes.userEdit({
					subjectuserkey: ":subjectuserkey",
				})}
				element={<UserEdit />}
			/>}
			<Route
				path={DomRoutes.userList()}
				element={
					<PrivateRoute
						scopes={[UserRoleDef.USER_LIST, UserRoleDef.USER_EDIT]}
						element={<UserList />}
					/>
				}
			/>
			<Route path="*" element={<NotFound />} />
		</Routes>
	);
}