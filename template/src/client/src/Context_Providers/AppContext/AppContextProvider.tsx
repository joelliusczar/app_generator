import React, {
	useMemo,
	useEffect,
} from "react";
import {
	dataDispatches as dispatches,
	useDataWaitingReducer,
} from "../../Reducers/dataWaitingReducer";
import PropTypes from "prop-types";
import { formatError } from "../../Helpers/error_formatter";
import { useCurrentUser } from "../AuthContext/AuthContext";
import {
	initialItemState,
	AppContext,
} from "./AppContext";



export const AppContextProvider = (props: { children: JSX.Element }) => {
	const { children } = props;
	const { access_token } = useCurrentUser();
	const loggedIn = !!access_token;

	const [itemState, itemDispatch] = useDataWaitingReducer(
		initialItemState
	);


	// useEffect(() => {
	// 	if (!loggedIn) return;
	// 	const requestObj = fetchItemList({});
	// 	const fetch = async () => {
	// 		try {
	// 			itemDispatch(dispatches.started());
	// 			const data = await requestObj.call();
	// 			itemDispatch(dispatches.done(data));
	// 		}
	// 		catch(err) {
	// 			itemDispatch(dispatches.failed(formatError(err)));
	// 		}
	// 	};
	// 	fetch();
	// 	return () => requestObj.abortController.abort();
	// },[itemDispatch, loggedIn]);




	const contextValue = useMemo(() => ({
		itemState,
		itemDispatch,
	}),[
		itemState,
		itemDispatch,
	]);

	return <AppContext.Provider value={contextValue}>
		{children}
	</AppContext.Provider>;
};

AppContextProvider.propTypes = {
	children: PropTypes.oneOfType([
		PropTypes.arrayOf(PropTypes.node),
		PropTypes.node,
	]).isRequired,
};



