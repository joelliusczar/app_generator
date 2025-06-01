import { onMounted, onUnmounted } from "vue"

export const useFormSubmit = (
	id: string,
	sendAction: (params: HTMLFormElement) => void
) => {

	const submit = (e: Event) => {
		e.preventDefault();
		sendAction(e.target as HTMLFormElement);
	};


	onMounted(() => {
		document.querySelector(`form#${id}`)?.addEventListener("submit", submit);
	});

	onUnmounted(() => {
		document.querySelector(`form#${id}`)?.removeEventListener("submit", submit)
	});
};