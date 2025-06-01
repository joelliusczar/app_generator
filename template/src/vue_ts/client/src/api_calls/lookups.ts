import type { LookupsDto } from "../types/lookups";

export const fetchLookups = () => {
	const abortController = new AbortController();
	return {
		abortController: abortController,
		call: async () => {
			const response = await fetch(
				"/api/lookups",
				{ signal: abortController.signal }
			);
			return await response.json() as LookupsDto;
		},
	};
};