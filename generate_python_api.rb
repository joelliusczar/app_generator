require_relative "generate_app_util"

include AppGenUtils

module AppGenPythons
	def self.generate(choices)

		projectName = choices.local_variable_get(:projectName)
		projectNameSnake = choices.local_variable_get(:projectNameSnake)
		fromLibs = "python/libs"
		fromApi = "python/api"
		fromTests = "python/tests"

		srcDtosAndUtilitiesDir = "src/#{fromLibs}/dtos_and_utilities"
		destDtosAndUtilitiesDir = "src/#{projectNameSnake}/dtos_and_utilities"

		copy_tpl(
			"requirements.txt",
			"requirements.txt"
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/type_aliases.py",
			"#{destDtosAndUtilitiesDir}/type_aliases.py"
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/generic_dtos.py",
			"#{destDtosAndUtilitiesDir}/generic_dtos.py",
			choices
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/simple_functions.py",
			"#{destDtosAndUtilitiesDir}/simple_functions.py"
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/user_role_def.py",
			"#{destDtosAndUtilitiesDir}/user_role_def.py"
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/action_rule_dtos.py",
			"#{destDtosAndUtilitiesDir}/action_rule_dtos.py"
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/account_dtos.py",
			"#{destDtosAndUtilitiesDir}/account_dtos.py"
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/validation_functions.py",
			"#{destDtosAndUtilitiesDir}/validation_functions.py"
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/db_helpers.py",
			"#{destDtosAndUtilitiesDir}/db_helpers.py",
			choices
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/errors.py",
			"#{destDtosAndUtilitiesDir}/errors.py",
			choices
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/logging.py",
			"#{destDtosAndUtilitiesDir}/logging.py",
			choices
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/name_strings.py",
			"#{destDtosAndUtilitiesDir}/name_strings.py"
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/file_reference.py",
			"#{destDtosAndUtilitiesDir}/file_reference.py",
			choices
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/__init__.py",
			"#{destDtosAndUtilitiesDir}/__init__.py"
		)

		copy_tpl(
			"src/#{fromLibs}/tables.py",
			"src/#{projectNameSnake}/tables.py"
		)

		srcServicesDir = "src/#{fromLibs}/services"
		destServicesDir = "src/#{projectNameSnake}/services"

		copy_tpl(
			"#{srcServicesDir}/env_manager.py",
			"#{destServicesDir}/env_manager.py",
			choices
		)

		copy_tpl(
			"#{srcServicesDir}/db_setup_service.py",
			"#{destServicesDir}/db_setup_service.py",
			choices
		)

		copy_tpl(
			"#{srcServicesDir}/process_service.py",
			"#{destServicesDir}/process_service.py",
			choices
		)

		copy_tpl(
			"#{srcServicesDir}/template_service.py",
			"#{destServicesDir}/template_service.py",
			choices
		)

		copy_tpl(
			"#{srcServicesDir}/accounts_service.py",
			"#{destServicesDir}/accounts_service.py",
			choices
		)

		copy_tpl(
			"#{srcServicesDir}/user_actions_history_service.py",
			"#{destServicesDir}/user_actions_history_service.py",
			choices
		)

		copy_tpl(
			"#{srcServicesDir}/__init__.py",
			"#{destServicesDir}/__init__.py"
		)

		copy_tpl(
			"src/#{fromLibs}/__init__.py",
			"src/#{projectNameSnake}/__init__.py"
		)


		copy_tpl(
			"src/#{fromApi}/api_error.py",
			"src/api/api_error.py",
			choices
		)

		copy_tpl(
			"src/#{fromApi}/api_dependencies.py",
			"src/api/api_dependencies.py",
			choices
		)

		copy_tpl(
			"src/#{fromApi}/accounts_controller.py",
			"src/api/accounts_controller.py",
			choices
		)

		copy_tpl(
			"src/#{fromApi}/index.py",
			"src/api/index.py",
			choices
		)

		copy_tpl(
			"src/#{fromApi}/accounts_controller.py",
			"src/api/accounts_controller.py",
			choices
		)

		copy_tpl(
			"src/#{fromApi}/api_dependencies.py",
			"src/api/api_dependencies.py",
			choices
		)


		copy_tpl(
			"src/#{fromTests}/mocks/__init__.py",
			"src/tests/mocks/__init__.py"
		)

		copy_tpl(
			"src/#{fromTests}/mocks/constant_values_defs.py",
			"src/tests/mocks/constant_values_defs.py",
			choices
		)

		copy_tpl(
			"src/#{fromTests}/mocks/db_data.py",
			"src/tests/mocks/db_data.py",
			choices
		)

		copy_tpl(
			"src/#{fromTests}/mocks/db_population.py",
			"src/tests/mocks/db_population.py",
			choices
		)

		copy_tpl(
			"src/#{fromTests}/mocks/mock_datetime_provider.py",
			"src/tests/mocks/mock_datetime_provider.py")

		copy_tpl(
			"src/#{fromTests}/mocks/mock_db_constructors.py",
			"src/tests/mocks/mock_db_constructors.py",
			choices
		)

		copy_tpl(
			"src/#{fromTests}/mocks/special_strings_reference.py",
			"src/tests/mocks/special_strings_reference.py"
		)

		copy_tpl(
			"src/#{fromTests}/__init__.py",
			"src/tests/__init__.py"
		)

		copy_tpl(
			"src/#{fromTests}/api_test_dependencies.py",
			"src/tests/api_test_dependencies.py"
		)

		copy_tpl(
			"src/#{fromTests}/common_fixtures.py",
			"src/tests/common_fixtures.py",
			choices
		)

		copy_tpl(
			"src/#{fromTests}/constant_fixtures_for_test.py",
			"src/tests/constant_fixtures_for_test.py",
			choices
		)

		copy_tpl(
			"src/#{fromTests}/helpers.py",
			"src/tests/helpers.py"
		)

		copy_tpl(
			"src/#{fromTests}/test_account_service.py",
			"src/tests/test_account_service.py",
			choices
		)

		copy_tpl(
			"src/#{fromTests}/test_accounts_controller.py",
			"src/tests/test_accounts_controller.py",
			choices
		)

		copy_tpl(
			"src/#{fromTests}/test_dtos.py",
			"src/tests/test_dtos.py",
			choices
		)

		copy_tpl(
			"src/#{fromTests}/test_fast_api.py",
			"src/tests/test_fast_api.py"
		)

		copy_tpl(
			"src/#{fromTests}/test_in_mem_db.py",
			"src/tests/test_in_mem_db.py",
			choices
		)

		copy_tpl(
			"src/#{fromTests}/test_python.py",
			"src/tests/test_python.py"
		)

		copy_tpl(
			"src/#{fromTests}/test_simple_functions.py",
			"src/tests/test_simple_functions.py",
			choices
		)

		copy_tpl(
			"src/#{fromTests}/test_test_env.py",
			"src/tests/test_test_env.py",
			choices
		)

		copy_tpl(
			"src/#{fromTests}/pytest.ini",
			"src/tests/pytest.ini"
		)


	end
end