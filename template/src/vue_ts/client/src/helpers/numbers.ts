export const formatOrdinal = (n: number) => {
	const h = n % 100;
	if (h > 10 && n < 20) {
		return `${n}th`
	}
	else
	{
		const t = n % 10;
		if ([0, 4, 5, 6, 7, 8, 9].some(d => d === t)) {
			return `${n}th`
		}
		if (t === 1) {
			return `${n}st`
		}
		if (t === 2) {
			return `${n}nd`
		}
		if (t === 3) {
			return `${n}rd`
		}
	}
	return "shit";
};