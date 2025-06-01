
import get from "just-safe-get";

export const formatError = (err: unknown): string => {
	if (!err) return "Missing error";
	if(!get(err, "response.data")) {
		return "Unable to hit api.";
	}
	const msg = get(err, "response.data.detail[0].msg");
	if (msg) return msg;
	console.error(err);
	return "undocumented error has occured";
};