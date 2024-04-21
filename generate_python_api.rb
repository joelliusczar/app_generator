require_relative "generate_app_util"

include AppGenUtils

module AppGenPythons
	def generate_python_api(appName, ucPrefix, lcPrefix, devOpsUtilitiesFile)

		srcDtosAndUtilitiesDir = 'src/libs/dtos_and_utilities'
		destDtosAndUtilitiesDir = "src/#{appName}_libs/dtos_and_utilities"

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/type_aliases.py", 
			"#{destDtosAndUtilitiesDir}/type_aliases.py"
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/generic_dtos.py",
			"#{destDtosAndUtilitiesDir}/generic_dtos.py",
			{
				ucPrefix: ucPrefix
			}
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
			{
				projectName: appName,
				lcPrefix: lcPrefix
			}
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/errors.py",
			"#{destDtosAndUtilitiesDir}/errors.py",
			{
				ucPrefix: ucPrefix
			}
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/logging.py",
			"#{destDtosAndUtilitiesDir}/logging.py",
			{
				projectName: appName,
				lcPrefix: lcPrefix
			}
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/name_strings.py",
			"#{destDtosAndUtilitiesDir}/name_strings.py"
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/file_reference.py",
			"#{destDtosAndUtilitiesDir}/file_reference.py",
			{
				devOpsUtilitiesFile: devOpsUtilitiesFile
			}
		)

		copy_tpl(
			"#{srcDtosAndUtilitiesDir}/__init__.py",
			"#{destDtosAndUtilitiesDir}/__init__.py"
		)

		copy_tpl(
			"src/libs/dev/ssl/installed_certs/__main__.py",
			"src/#{appName}_libs/dev/ssl/installed_certs/__main__.py"
		)

		copy_tpl(
			"src/libs/tables.py",
			"src/#{appName}_libs/tables.py"
		)

		srcServicesDir = "src/libs/services"
		destServicesDir = "src/#{appName}_libs/services"

		copy_tpl(
			"#{srcServicesDir}/env_manager.py",
			"#{destServicesDir}/env_manager.py",
			{
				projectName: appName,
				ucPrefix: ucPrefix
			}
		)

		copy_tpl(
			"#{srcServicesDir}/db_setup_service.py",
			"#{destServicesDir}/db_setup_service.py",
			{
				projectName: appName
			}
		)

		copy_tpl(
			"#{srcServicesDir}/process_service.py",
			"#{destServicesDir}/process_service.py",
			{
				projectName: appName
			}
		)

		copy_tpl(
			"#{srcServicesDir}/template_service.py",
			"#{destServicesDir}/template_service.py",
			{
				projectName: appName
			}
		)

		copy_tpl(
			"#{srcServicesDir}/accounts_service.py",
			"#{destServicesDir}/accounts_service.py",
			{
				projectName: appName
			}
		)

		copy_tpl(
			"#{srcServicesDir}/user_actions_history_service.py",
			"#{destServicesDir}/user_actions_history_service.py",
			{
				projectName: appName
			}
		)

		copy_tpl(
			"#{srcServicesDir}/__init__.py",
			"#{destServicesDir}/__init__.py"
		)

		copy_tpl(
			"src/libs/__init__.py",
			"src/#{appName}_libs/__init__.py")

		copy_tpl(
			"src/api/api_error.py", 
			"src/api/api_error.py",
			{
				projectName: appName
			}
		)

		copy_tpl(
			"src/api/api_dependencies.py", 
			"src/api/api_dependencies.py",
			{
				projectName: appName
			}
		)

		copy_tpl(
			"src/api/accounts_controller.py", 
			"src/api/accounts_controller.py",
			{
				projectName: appName
			}
		)

		copy_tpl(
			"src/api/index.py", 
			"src/api/index.py",
			{
				projectName: appName
			}
		)

		copy_tpl(
			"src/api/accounts_controller.py", 
			"src/api/accounts_controller.py",
			{
				projectName: appName
			}
		)

		copy_tpl(
			"src/api/api_dependencies.py", 
			"src/api/api_dependencies.py",
			{
				projectName: appName
			}
		)


		copy_tpl(
			"src/tests/mocks/__init__.py",
			"src/tests/mocks/__init__.py"
		)
		
		copy_tpl(
			"src/tests/mocks/constant_values_defs.py", 
			"src/tests/mocks/constant_values_defs.py",
			{ projectName: appName }
		)
		
		copy_tpl(
			"src/tests/mocks/db_data.py", 
			"src/tests/mocks/db_data.py",
			{ projectName: appName }
		)
		
		copy_tpl(
			"src/tests/mocks/db_population.py", 
			"src/tests/mocks/db_population.py",
			{ projectName: appName }
		)
		
		copy_tpl(
			"src/tests/mocks/mock_datetime_provider.py",
			"src/tests/mocks/mock_datetime_provider.py")
		
		copy_tpl(
			"src/tests/mocks/mock_db_constructors.py", 
			"src/tests/mocks/mock_db_constructors.py",
			{ projectName: appName }
		)
		
		copy_tpl(
			"src/tests/mocks/special_strings_reference.py",
			"src/tests/mocks/special_strings_reference.py"
		)
		
		copy_tpl(
			"src/tests/__init__.py",
			"src/tests/__init__.py"
		)
		
		copy_tpl(
			"src/tests/api_test_dependencies.py",
			"src/tests/api_test_dependencies.py"
		)
		
		copy_tpl(
			"src/tests/common_fixtures.py",
			"src/tests/common_fixtures.py",
			{ projectName: appName }
		)
		
		copy_tpl(
			"src/tests/constant_fixtures_for_test.py",
			"src/tests/constant_fixtures_for_test.py",
			{ projectName: appName }
		)
		
		copy_tpl(
			"src/tests/helpers.py",
			"src/tests/helpers.py"
		)
		
		copy_tpl(
			"src/tests/test_account_service.py", 
			"src/tests/test_account_service.py",
			{ projectName: appName }
		)
		
		copy_tpl(
			"src/tests/test_accounts_controller.py", 
			"src/tests/test_accounts_controller.py",
			{ projectName: appName }
		)
		
		copy_tpl(
			"src/tests/test_dtos.py",
			"src/tests/test_dtos.py",
			{ projectName: appName }
		)
		
		copy_tpl(
			"src/tests/test_fast_api.py",
			"src/tests/test_fast_api.py"
		)
		
		copy_tpl("src/tests/test_in_mem_db.py", "src/tests/test_in_mem_db.py",
			{ projectName: appName }
		)
		
		copy_tpl(
			"src/tests/test_python.py",
			"src/tests/test_python.py"
		)
		
		copy_tpl("src/tests/test_simple_functions.py", "src/tests/test_simple_functions.py",
			{ projectName: appName }
		)
		
		copy_tpl("src/tests/test_test_env.py", "src/tests/test_test_env.py",
			{ projectName: appName }
		)
		
		copy_tpl(
			"src/tests/pytest.ini",
			"src/tests/pytest.ini"
		)

		copy_tpl(
			"requirements.txt",
			"requirements.txt"
		)
		

	end
end