export const CallStatus = {
	Inert: "",
	Dim: "dim",
	Hide: "hide"
};

type CallStatusT = typeof CallStatus[keyof typeof CallStatus];

export type ApiResult<T> = {
	data: T | null,
	error: string | null,
	loading: CallStatusT
};