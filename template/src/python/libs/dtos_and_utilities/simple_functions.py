#pyright: reportMissingTypeStubs=false
import re
import bcrypt
import email_validator #pyright: ignore reportUnknownMemberType
from datetime import datetime, timezone
from typing import (
	Any,
	Hashable,
	Iterable,
	Iterator,
	Optional,
	Tuple,
	overload,
	TypeVar,
	Union
)
from email_validator import ValidatedEmail
from collections import Counter
from .type_aliases import (s2sDict)

T = TypeVar("T")

guidRegx = \
	r"[a-zA-Z\d]{8}-?[a-zA-Z\d]{4}-?[a-zA-Z\d]{4}-?[a-zA-Z\d]{4}-?[a-zA-Z\d]{12}"

def get_datetime() -> datetime:
	return datetime.now(timezone.utc)

def build_error_obj(msg: str, field: Optional[str]=None) -> dict[str, Any]:
	obj: dict[str, Any] = { "msg": msg, "field": field  }
	return obj

def hashpw(pw: bytes) -> bytes:
	return bcrypt.hashpw(pw, bcrypt.gensalt(12))

def checkpw(guess: bytes, hash: bytes) -> bool:
	return bcrypt.checkpw(guess, hash)

def validate_email(email: str) -> ValidatedEmail:
	return email_validator.validate_email(email) #pyright: ignore reportUnknownMemberType

def seconds_to_tuple(seconds: int) -> Tuple[int, int, int, int]:
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	d, h = divmod(h, 24)
	return (d, h, m, s)

def build_timespan_msg(timeleft: Tuple[int, int, int, int]) -> str:
	days = f"{timeleft[0]} days, " if any(timeleft[1:]) \
		else f"{timeleft[0]} days" if timeleft[0] else ""
	hours = f"{timeleft[1]} hours, " if any(timeleft[2:]) \
		else f"{timeleft[1]} hours" if timeleft[1] else ""
	minutes = f"{timeleft[2]} mins, " if timeleft[3] \
		else f"{timeleft[2]} mins" if timeleft[2] else ""
	seconds = f"and {timeleft[3]} seconds" \
		if any(timeleft[:-1]) else f"{timeleft[3]} seconds" if timeleft[3] else ""
	return f"{days}{hours}{minutes}{seconds}"

def get_duplicates(
	items: Iterable[Hashable]
) -> Iterator[Tuple[Hashable, int]]:
	counter = Counter(items)
	mostCommon = counter.most_common(1)
	return (pair for pair in mostCommon if pair[1] > 1)


def get_non_simple_chars(name: str) -> Optional[str]:
		m = re.search(r"[^a-zA-Z0-9_]", name)
		if m:
			return m.group(0)
		return None

def is_name_safe(name: str, maxLen: int=50) -> bool:
	if len(name) > maxLen:
		return False
	if get_non_simple_chars(name):
		return False
	return True

def _kvpSplit(kvp: str) -> Tuple[str, str]:
	eqSplit = kvp.split("=")
	if len(eqSplit) < 2:
		return "name", kvp
	return eqSplit[0], eqSplit[1]

def role_dict(role: str) -> s2sDict:
		return {p[0]:p[1] for p in (_kvpSplit(k) for k in role.split(";"))}

def squash_sequential_duplicates(
	compressura: Iterable[T],
	pattern: T
) -> Iterator[T]:
	cIter = iter(compressura)
	previous = next(cIter)
	yield previous
	for element in cIter:
		if element == previous and element == pattern:
			continue
		previous = element
		yield element

def squash_sequential_duplicate_chars(
	compressura: str,
	pattern: str
) -> str:
	return "".join(squash_sequential_duplicates(compressura, pattern))

def format_newlines_for_stream(input: str) -> str:
	cleaned = input.replace("\n", " ")
	output = f"{cleaned}\n"
	return output

def int_or_str(s: Union[int, str]) -> Union[int, str]:
	#fastapi/pydantic stopped auto comnverting my string ints
	#to ints
	try:
		i = int(s)
		return i
	except:
		return s

def clean_search_term_for_like(searchTerm: str) -> str:
	return searchTerm.replace("_","\\_").replace("%","\\%")