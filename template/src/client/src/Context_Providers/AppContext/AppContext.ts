import React, {
	useCallback,
	useContext,
	createContext,
} from "react";
import { RequiredDataStore } from "../../Reducers/reducerStores";
import {
	ListDataShape,
} from "../../Types/reducer_types";
import {
	IdItem,
	SingleOrList,
	NamedIdItem,
} from "../../Types/generic_types";
import { nameSortFn } from "../../Helpers/array_helpers";
import {
	DataActionPayload as ActionPayload,
	dataDispatches as dispatches,
} from "../../Reducers/dataWaitingReducer";


type AppContextType = {
	albumsState: RequiredDataStore<ListDataShape<NamedIdItem>>,
	albumsDispatch: React.Dispatch<
		ActionPayload<ListDataShape<NamedIdItem>>
	>
};

export const initialItemState =
	new RequiredDataStore<ListDataShape<NamedIdItem>>({ items: []});


export const AppContext = createContext<AppContextType>({
	albumsState: initialItemState,
	albumsDispatch: ({ }) => {},
});

const addItemToState = <T extends NamedIdItem>(
	state: RequiredDataStore<ListDataShape<T>>,
	item: T
) => {
	const items = [...state.data.items, item]
		.sort(nameSortFn);
	return {
		...state,
		data: {
			items: items,
		},
	};
};

const updateItemInState = <T extends NamedIdItem>(
	state: RequiredDataStore<ListDataShape<T>>,
	item: T
) => {
	const items = [...state.data.items];
	const idx = items.findIndex(i => i.id === item.id);
	if (idx > -1) {
		items[idx] = item;
		return {
			...state,
			data: {
				items: items,
			},
		};
	}
	console.error("Item was not found in local store.");
	return state;
};

export const useItemData = () => {
	const {
		albumsState: { data: { items }, error, callStatus },
		albumsDispatch: dispatch,
	} = useContext(AppContext);

	const add = useCallback(
		(item: NamedIdItem) => 
			dispatch(dispatches.update(state => {
				return addItemToState(state, item);
			})),
		[dispatch]
	);

	const update = useCallback((item: NamedIdItem) => 
		dispatch(dispatches.update((state) => {
			return updateItemInState(state, item);
		})),
	[dispatch]
	);

	return {
		items,
		error,
		callStatus,
		add,
		update,
	};
};



export const useIdMapper = <T extends IdItem>(items: T[]) => {
	const idMapper =
		<InT extends T | T[] | null,>(value: InT): SingleOrList<T, InT> => {
			if(!value) return null as SingleOrList<T, InT>;
			if(Array.isArray(value)) {
				return value.map((item) =>
					items.find(x => x.id === item.id)
				).filter(x => !!x) as SingleOrList<T, InT>;
			}
			if (typeof(value) === "object") {
				const matches = items.find(x => x.id === value.id) || null;
				if (matches) {
					return matches as SingleOrList<T, InT>;
				}
			}
			return null as SingleOrList<T, InT>;
		};
	return idMapper;
};