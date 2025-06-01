import { reactive } from "vue";
import { fetchLookups } from "../api_calls/lookups";
import { CallStatus, type ApiResult } from "../types/requests";
import type { LookupsDto } from "../types/lookups";
import { formatError } from "../helpers/errors"

const fetchResults = reactive<ApiResult<LookupsDto>>({ 
	loading: CallStatus.Inert,
	data: null,
	error: null
});

try {
	const requestObj = fetchLookups();
	fetchResults.data = await requestObj.call();
}
catch (err) {
	fetchResults.error = formatError(err);
}

export const useLookups = () => {

	return fetchResults;
};