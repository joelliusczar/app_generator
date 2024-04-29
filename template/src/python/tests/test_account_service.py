#pyright: reportMissingTypeStubs=false, reportPrivateUsage=false
import pytest
from sqlalchemy import insert
from sqlalchemy.engine import Connection
from datetime import datetime, timezone
from <%= projectNameSnake %>.tables import station_queue
from <%= projectNameSnake %>.services import AccountsService
from <%= projectNameSnake %>.dtos_and_utilities import (
	AccountInfo,
	UserRoleDef,
	ActionRule
)
from .constant_fixtures_for_test import\
	fixture_primary_user as fixture_primary_user
from .constant_fixtures_for_test import *
from .common_fixtures import\
	fixture_account_service as fixture_account_service
from .common_fixtures import *

@pytest.fixture
def fixture_account_service_mock_current_time(
	fixture_account_service: AccountsService
):
	def _get_test_datetime() -> datetime:
		global currentTestDate
		if not currentTestDate:
			currentTestDate = datetime.now(timezone.utc)
		return currentTestDate
	fixture_account_service.get_datetime = _get_test_datetime
	return fixture_account_service

def test_unique_roles():
	alphaRole = "alphaRole"
	bravoRole = "bravoRole"
	charlieRole = "charlieRole"
	testRoles1 = [ActionRule(name=alphaRole)]
	gen = ActionRule.filter_out_repeat_roles(testRoles1)
	result = next(gen)
	assert result.name == alphaRole
	with pytest.raises(StopIteration):
		next(gen)
	testRoles2 = ActionRule.sorted([
		ActionRule(name=alphaRole, span=5, count=1),
		ActionRule(name=alphaRole, span=15, count=1)
	])
	gen = ActionRule.filter_out_repeat_roles(testRoles2)
	results = list(gen)
	assert len(results) == 1
	assert results[0].name == alphaRole
	assert results[0].span == 15
	testRoles3 = ActionRule.sorted([
		ActionRule(name=alphaRole),
		ActionRule(name=alphaRole, span=15, count=1)
	])
	gen = ActionRule.filter_out_repeat_roles(testRoles3)
	results = list(gen)
	assert len(results) == 1
	assert results[0].name == alphaRole
	assert results[0].span == 15
	testRoles4 = ActionRule.sorted([
		ActionRule(name=alphaRole),
		ActionRule(name=alphaRole, span=15, count=1),
		ActionRule(name=bravoRole, span=60, count=1),
		ActionRule(name=bravoRole, span=15, count=1),
		ActionRule(name=charlieRole)
	])
	gen = ActionRule.filter_out_repeat_roles(testRoles4)
	results = list(gen)
	assert len(results) == 3
	assert results[2].name == charlieRole
	assert results[0].name == bravoRole
	assert results[0].span == 60
	assert results[1].name == alphaRole
	assert results[1].span == 15

@pytest.mark.echo(False)
def test_save_roles(
	fixture_account_service_mock_current_time: AccountsService
):
	alphaRole = "alphaRole"
	bravoRole = "bravoRole"
	charlieRole = "charlieRole"
	deltaRole = "deltaRole"
	accountService = fixture_account_service_mock_current_time
	accountInfo = accountService.get_account_for_edit(6)
	assert accountInfo and len(accountInfo.roles) == 3
	assert accountInfo and accountInfo.roles[0] == ActionRule(
		name=alphaRole,span=120
	)
	assert accountInfo and accountInfo.roles[1] == ActionRule(
		name=bravoRole
	)
	assert accountInfo and accountInfo.roles[2] == ActionRule(
		name=charlieRole, span=15
	)


	result = sorted(accountService.save_roles(6, accountInfo.roles))
	assert len(result) == 3
	assert result[0] == ActionRule(
		name=alphaRole,span=120
	)
	assert accountInfo and accountInfo.roles[1] == ActionRule(
		name=bravoRole
	)
	assert result[2] == ActionRule(
		name=charlieRole, span=15
	)
	fetched = sorted(accountService.__get_roles__(6))
	assert len(fetched) == 3
	assert fetched[0] == ActionRule(
		name=alphaRole,span=120
	)
	assert fetched[1] == ActionRule(
		name=bravoRole
	)
	assert fetched[2] == ActionRule(
		name=charlieRole, span=15
	)


	nextSet = [*result, ActionRule(name=deltaRole)]
	result = list(sorted(accountService.save_roles(6, nextSet)))
	assert len(result) == 4
	assert result[0] == ActionRule(
		name=alphaRole,span=120
	)
	assert fetched[1] == ActionRule(
		name=bravoRole
	)
	assert result[2] == ActionRule(
		name=charlieRole, span=15
	)
	assert result[3] == ActionRule(name=deltaRole)
	fetched = sorted(accountService.__get_roles__(6))
	assert len(fetched) == 4
	assert result[0] == ActionRule(
		name=alphaRole,span=120
	)
	assert fetched[1] == ActionRule(
		name=bravoRole
	)
	assert result[2] == ActionRule(
		name=charlieRole, span=15
	)
	assert result[3] == ActionRule(name=deltaRole)


	nextSet = [*result, ActionRule(name=deltaRole)]
	result = sorted(accountService.save_roles(6, nextSet))
	assert len(result) == 4
	assert result[0] == ActionRule(
		name=alphaRole,span=120
	)
	assert fetched[1] == ActionRule(
		name=bravoRole
	)
	assert result[2] == ActionRule(
		name=charlieRole, span=15
	)
	assert result[3] == ActionRule(name=deltaRole)
	fetched = sorted(accountService.__get_roles__(6))
	assert len(fetched) == 4
	assert result[0] == ActionRule(
		name=alphaRole,span=120
	)
	assert fetched[1] == ActionRule(
		name=bravoRole
	)
	assert result[2] == ActionRule(
		name=charlieRole, span=15
	)
	assert result[3] == ActionRule(name=deltaRole)


	nextSet = [
		ActionRule(name=charlieRole, span=15),
		ActionRule(name=deltaRole)
	]
	result = sorted(accountService.save_roles(6, nextSet))
	assert len(result) == 2
	assert result[0] == ActionRule(
		name=charlieRole, span=15
	)
	assert result[1] == ActionRule(name=deltaRole)
	fetched = sorted(accountService.__get_roles__(6))
	assert len(fetched) == 2
	assert fetched[0] == ActionRule(
		name=charlieRole, span=15
	)
	assert fetched[1] == ActionRule(name=deltaRole)


	nextSet = [
		ActionRule(name=deltaRole),
		ActionRule(name=alphaRole,span=120)
	]
	result = sorted(accountService.save_roles(6, nextSet))
	assert len(result) == 2
	assert result[0] == ActionRule(
		name=alphaRole,span=120
	)
	assert result[1] == ActionRule(name=deltaRole)
	fetched = sorted(accountService.__get_roles__(6))
	assert len(fetched) == 2
	assert fetched[0] == ActionRule(
		name=alphaRole,span=120
	)
	assert fetched[1] == ActionRule(name=deltaRole)

def test_user_search(
	fixture_account_service_mock_current_time: AccountsService
):
	accountService = fixture_account_service_mock_current_time
	res = sorted(
		accountService.get_account_list("a"),
		key=lambda a: a.id
	)
	assert len(res) == 1
	assert res[0].displayname == "Alice is my name"
	res = sorted(
		accountService.get_account_list("f"),
		key=lambda a: a.id
	)
	assert len(res) == 3#4
	#assert res[0].displayname == "\uFB00 ozotroz"
	assert res[0].displayname == "Felix the man"
	assert res[1].displayname == None
	assert res[2].displayname == "Foxtrain chu"

	res = sorted(
		accountService.get_account_list("fo"),
		key=lambda a: a.id
	)
	assert len(res) == 2
	assert res[0].displayname == None
	assert res[1].displayname == "Foxtrain chu"

	res = sorted(
		accountService.get_account_list("fox"),
		key=lambda a: a.id
	)
	assert len(res) == 2
	assert res[0].displayname == None
	assert res[1].displayname == "Foxtrain chu"

	res = sorted(
		accountService.get_account_list("foxt"),
		key=lambda a: a.id
	)
	assert len(res) == 1
	assert res[0].displayname == "Foxtrain chu"

	res = sorted(
		accountService.get_account_list("n"),
		key=lambda a: a.id
	)
	assert len(res) == 3
	assert res[0].displayname == "\u006E\u0303ovoper"
	assert res[1].displayname == "Ned Land of the Spear"
	assert res[2].displayname == "Narloni"
