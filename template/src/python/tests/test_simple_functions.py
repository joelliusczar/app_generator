from typing import Any
from <%= projectNameSnake %>.dtos_and_utilities import (
	seconds_to_tuple,
	squash_sequential_duplicate_chars
)
from sqlalchemy.engine import Connection
from sqlalchemy import\
	select
from sqlalchemy.sql import ColumnCollection
from .common_fixtures import *

def test_seconds_to_tuple():
	result = seconds_to_tuple(59)
	assert result[0] == 0
	assert result[1] == 0
	assert result[2] == 0
	assert result[3] == 59

	result = seconds_to_tuple(60)
	assert result[0] == 0
	assert result[1] == 0
	assert result[2] == 1
	assert result[3] == 0

	result = seconds_to_tuple(61)
	assert result[0] == 0
	assert result[1] == 0
	assert result[2] == 1
	assert result[3] == 1

	result = seconds_to_tuple(119)
	assert result[0] == 0
	assert result[1] == 0
	assert result[2] == 1
	assert result[3] == 59

	result = seconds_to_tuple(120)
	assert result[0] == 0
	assert result[1] == 0
	assert result[2] == 2
	assert result[3] == 0

	result = seconds_to_tuple(3599)
	assert result[0] == 0
	assert result[1] == 0
	assert result[2] == 59
	assert result[3] == 59

	result = seconds_to_tuple(3600)
	assert result[0] == 0
	assert result[1] == 1
	assert result[2] == 0
	assert result[3] == 0

	result = seconds_to_tuple(3601)
	assert result[0] == 0
	assert result[1] == 1
	assert result[2] == 0
	assert result[3] == 1

	result = seconds_to_tuple(86399)
	assert result[0] == 0
	assert result[1] == 23
	assert result[2] == 59
	assert result[3] == 59

	result = seconds_to_tuple(86400)
	assert result[0] == 1
	assert result[1] == 0
	assert result[2] == 0
	assert result[3] == 0

	result = seconds_to_tuple(86401)
	assert result[0] == 1
	assert result[1] == 0
	assert result[2] == 0
	assert result[3] == 1

	result = seconds_to_tuple(2678400)
	assert result[0] == 31
	assert result[1] == 0
	assert result[2] == 0
	assert result[3] == 0


def test_squash_sequential_duplicates():
	result = squash_sequential_duplicate_chars("/alpha//bravo","/")
	assert result == "/alpha/bravo"

	result = squash_sequential_duplicate_chars("alpha//bravo","/")
	assert result == "alpha/bravo"


	result = squash_sequential_duplicate_chars("//////alpha//bravo","/")
	assert result == "/alpha/bravo"

	result = squash_sequential_duplicate_chars("//////","/")
	assert result == "/"

	result = squash_sequential_duplicate_chars("//////alpha//bravo////","/")
	assert result == "/alpha/bravo/"