import { useMemo } from "react";
import {
	Named,
	NamedIdItem,
	SortCallback,
	SortCallbackFactory,
} from "../Types/generic_types";

export const nameSortFn: SortCallback<Named> = (a: Named,b: Named): number =>
	a.name > b.name ? 1 : a.name < b.name ? -1 : 0;


export const keyedSortFn: SortCallbackFactory =
	<T, K extends keyof T>(key: K) => ((a: T,b: T) =>
		a[key] > b[key] ? 1 : a[key] < b[key] ? -1 : 0);


export const useCombinedContextAndFormItems = <T extends NamedIdItem>(
	contextItems: T[],
	fetchedItems: T[]
): T[] => {
	const combined = useMemo(() => {
		const missing = fetchedItems
			.filter(i => contextItems.every(c => c.id !== i.id) || !contextItems);
		return [...contextItems, ...missing].sort(nameSortFn);
	},[contextItems, fetchedItems]);

	return combined;
};

export const notNullPredicate =
	<T>(value: T | null | undefined): value is T => {
		return value !== null && value !== undefined;
	};

export const prefix_split  = (prefix: string) => {
	const result = prefix
		.split("/")
		.filter(s => !!s)
		.reduce((a, c) => {
			if (a.length) {
				const last = a[a.length - 1];
				a.push(`${last}${c}/`);
				return a;
			}
			else {
				a.push(`${c}/`);
				return a;
			}
		},[] as string[]);
	return result;
};