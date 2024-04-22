require_relative "generate_app_util"

include AppGenUtils

module AppGenReactTs
	def generate_react_ts(choices)

		fromClient = "client_react_ts"
		copy_tpl(
			"src/#{fromClient}/eslintrc.js",
			"src/client/.eslintrc.js"
		)
		
		copy_tpl(
			"src/#{fromClient}/index.html",
			"src/client/index.html"
		)
		
		copy_tpl(
			"src/#{fromClient}/package.json",
			"src/client/package.json",
			choices
		)
		
		copy_tpl(
			"src/#{fromClient}/tsconfig.json",
			"src/client/tsconfig.json"
		)
		
		copy_tpl(
			"src/#{fromClient}/vite-env.d.ts",
			"src/client/vite-env.d.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/vite.config.ts",
			"src/client/vite.config.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Types/generic_types.ts",
			"src/client/src/Types/generic_types.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Types/pageable_types.ts",
			"src/client/src/Types/pageable_types.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Types/user_types.ts",
			"src/client/src/Types/user_types.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Types/browser_types.ts",
			"src/client/src/Types/browser_types.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Types/reducer_types.ts",
			"src/client/src/Types/reducer_types.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/App.css",
			"src/client/src/App.css"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/constants.ts",
			"src/client/src/constants.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/index.css",
			"src/client/src/index.css"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/style_config.ts",
			"src/client/src/style_config"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/AppRoot.tsx",
			"src/client/src/AppRoot.tsx",
			choices
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Navigation/NavRoutes.tsx",
			"src/client/src/Components/Navigation/NavRoutes.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Shared/ErrorBoundary.tsx",
			"src/client/src/Components/Shared/ErrorBoundary.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Shared/FormFileUpload.tsx",
			"src/client/src/Components/Shared/FormFileUpload.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Shared/FormSelect.tsx",
			"src/client/src/Components/Shared/FormSelect.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Shared/FormTextField.tsx",
			"src/client/src/Components/Shared/FormTextField.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Shared/Loader.tsx",
			"src/client/src/Components/Shared/Loader.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Shared/OptionsButton.tsx",
			"src/client/src/Components/Shared/OptionsButton.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Shared/PrivateRoute.tsx",
			"src/client/src/Components/Shared/PrivateRoute.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Shared/RoutingErrors.tsx",
			"src/client/src/Components/Shared/RoutingErrors.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Shared/SubmitButton.tsx",
			"src/client/src/Components/Shared/SubmitButton.tsx"
		)
		
		copy_tpl(
			"src/client/2src/Components/Shared/UrlPagination.tsx",
			"src/client/src/Components/Shared/UrlPagination.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Shared/YesNoControl.tsx",
			"src/client/src/Components/Shared/YesNoControl.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Users/UserEdit.tsx",
			"src/client/src/Components/Users/UserEdit.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Users/UserList.tsx", 
			"src/client/src/Components/Users/UserList.tsx",
			choices
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Users/UserLoginModal.tsx",
			"src/client/src/Components/Users/UserLoginModal.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Users/UserLoginForm.tsx",
			"src/client/src/Components/Users/UserLoginForm.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Users/UserNew.tsx",
			"src/client/src/Components/Users/UserNew.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Users/UserMenu.tsx",
			"src/client/src/Components/Users/UserMenu.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Users/UserSearch.tsx",
			"src/client/src/Components/Users/UserSearch.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Users/RoleView.tsx",
			"src/client/src/Components/Users/RoleView.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Users/RoleEntry.tsx",
			"src/client/src/Components/Users/RoleEntry.tsx"
		)
			
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Users/SiteUserRoleAssignmentTable.tsx",
			"src/client/src/Components/Users/SiteUserRoleAssignmentTable.tsx",
			choices
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Components/Users/UserRoleAssignmentTable.tsx",
			"src/client/src/Components/Users/UserRoleAssignmentTable.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/API_Calls/api.ts",
			"src/client/src/API_Calls/api.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/API_Calls/userCalls.ts",
			"src/client/src/API_Calls/userCalls.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Context_Providers/AppContext/AppContext.ts",
			"src/client/src/Context_Providers/AppContext/AppContext.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Context_Providers/AppContext/AppContextProvider.tsx",
			"src/client/src/Context_Providers/AppContext/AppContextProvider.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Context_Providers/AuthContext/AuthContext.ts",
			"src/client/src/Context_Providers/AuthContext/AuthContext.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Context_Providers/AuthContext/AuthContextProvider.tsx",
			"src/client/src/Context_Providers/AuthContext/AuthContextProvider.tsx"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Helpers/array_helpers.ts",
			"src/client/src/Helpers/array_helpers.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Helpers/string_helpers.ts",
			"src/client/src/Helpers/string_helpers.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Helpers/browser_helpers.ts",
			"src/client/src/Helpers/browser_helpers.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Helpers/compare_helpers.ts",
			"src/client/src/Helpers/compare_helpers.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Helpers/error_formatter.ts",
			"src/client/src/Helpers/error_formatter.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Helpers/pageable_helpers.ts",
			"src/client/src/Helpers/pageable_helpers.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Helpers/request_helpers.ts",
			"src/client/src/Helpers/request_helpers.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Helpers/rule_helpers.ts",
			"src/client/src/Helpers/rule_helpers.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Helpers/time_helper.ts",
			"src/client/src/Helpers/time_helper.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Helpers/validation_helpers.ts",
			"src/client/src/Helpers/validation_helpers.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Reducers/dataWaitingReducer.ts",
			"src/client/src/Reducers/dataWaitingReducer.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Reducers/reducerStores.ts",
			"src/client/src/Reducers/reducerStores.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Reducers/keyedDataWaitingReducer.ts",
			"src/client/src/Reducers/keyedDataWaitingReducer.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Reducers/keyedVoidWaitingReducer.ts",
			"src/client/src/Reducers/keyedVoidWaitingReducer.ts"
		)
		
		copy_tpl(
			"src/#{fromClient}/src/Reducers/voidWaitingReducer.ts",
			"src/client/src/Reducers/voidWaitingReducer.ts"
		)
	end
end