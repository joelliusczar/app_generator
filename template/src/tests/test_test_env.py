import sys
import os
import pytest

@pytest.mark.skip()
def test_show_path():
	print(os.environ['PYTHONPATH'])
	print(sys.path)


def test_show_db_setup_pass():
	from <%= projectName %>_libs.services import EnvManager
	dbSetupPass = EnvManager.db_setup_pass()
	dbOwnerPass = EnvManager.db_pass_owner()
	dbApiPass = EnvManager.db_pass_api()
	assert dbSetupPass
	assert dbOwnerPass
	assert dbApiPass