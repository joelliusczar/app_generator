"use strict";
const Generator = require("yeoman-generator");

module.exports = class extends Generator {
  prompting() {
    const buildDefaultPrefix = projectName => {
      const split = projectName
        .split(/([A-Z\-_ ][a-z0-9]*)/)
        .filter(x => x !== "" && x !== "-" && x !== "_" && x !== " ");
      const firstLetters = split.map(x => x[0]);
      return firstLetters.join("");
    };

    const prompts = [
      {
        type: "input",
        name: "name",
        message: "Project Name?",
        default: this.appname
      },
      {
        type: "input",
        name: "prefix",
        message: "Project Prefix?",
        default: buildDefaultPrefix(this.appname)
      }
    ];

    return this.prompt(prompts).then(props => {
      // To access props later use this.props.someAnswer;
      this.props = props;
    });
  }

  writing() {
    const lcPrefix = this.props.prefix.toLowerCase();
    const ucPrefix = this.props.prefix.toUpperCase();
    const devOpsUtilitiesFile = `${lcPrefix}_dev_ops_utilities`;

    this.fs.copyTpl(
      this.templatePath("gitignore"),
      this.destinationPath(".gitignore"),
      { projectName: this.props.name }
    );

    this.fs.copyTpl(
      this.templatePath("dev_ops_utilities.sh"),
      this.destinationPath(`${lcPrefix}_dev_ops_utilities.sh`),
      {
        projectName: this.props.name,
        ucPrefix: ucPrefix,
        lcPrefix: lcPrefix
      }
    );

    this.fs.copy(
      this.templatePath("requirements.txt"),
      this.destinationPath("requirements.txt")
    );

    this.fs.copyTpl(
      this.templatePath("deploy_to_server.sh"),
      this.destinationPath("deploy_to_server.sh"),
      {
        devOpsUtilitiesFile: devOpsUtilitiesFile,
        projectName: this.props.name,
        ucPrefix: ucPrefix,
        lcPrefix: lcPrefix
      }
    );

    this.fs.copyTpl(
      this.templatePath(".vscode/launch.json"),
      this.destinationPath(".vscode/launch.json"),
      {
        projectName: this.props.name,
        ucPrefix: ucPrefix,
        lcPrefix: lcPrefix
      }
    );

    this.fs.copyTpl(
      this.templatePath(".vscode/settings.json"),
      this.destinationPath(".vscode/settings.json"),
      {
        projectName: this.props.name,
        ucPrefix: ucPrefix,
        lcPrefix: lcPrefix
      }
    );

    this.fs.copyTpl(
      this.templatePath(".vscode/tasks.json"),
      this.destinationPath(".vscode/tasks.json"),
      {
        devOpsUtilitiesFile: devOpsUtilitiesFile
      }
    );

    this.fs.copyTpl(
      this.templatePath("install_script.sh"),
      this.destinationPath("install_script.sh"),
      {
        devOpsUtilitiesFile: devOpsUtilitiesFile,
        ucPrefix: ucPrefix,
        lcPrefix: lcPrefix
      }
    );

    const srcDtosAndUtilitiesDir = `src/libs/dtos_and_utilities`;
    const destDtosAndUtilitiesDir = `src/${this.props.name}_libs/dtos_and_utilities`;
    this.fs.copy(
      this.templatePath(`${srcDtosAndUtilitiesDir}/type_aliases.py`),
      this.destinationPath(`${destDtosAndUtilitiesDir}/type_aliases.py`)
    );

    this.fs.copy(
      this.templatePath(`${srcDtosAndUtilitiesDir}/generic_dtos.py`),
      this.destinationPath(`${destDtosAndUtilitiesDir}/generic_dtos.py`)
    );

    this.fs.copy(
      this.templatePath(`${srcDtosAndUtilitiesDir}/simple_functions.py`),
      this.destinationPath(`${destDtosAndUtilitiesDir}/simple_functions.py`)
    );

    this.fs.copy(
      this.templatePath(`${srcDtosAndUtilitiesDir}/user_role_def.py`),
      this.destinationPath(`${destDtosAndUtilitiesDir}/user_role_def.py`)
    );

    this.fs.copy(
      this.templatePath(`${srcDtosAndUtilitiesDir}/action_rule_dtos.py`),
      this.destinationPath(`${destDtosAndUtilitiesDir}/action_rule_dtos.py`)
    );

    this.fs.copy(
      this.templatePath(`${srcDtosAndUtilitiesDir}/account_dtos.py`),
      this.destinationPath(`${destDtosAndUtilitiesDir}/account_dtos.py`)
    );

    this.fs.copy(
      this.templatePath(`${srcDtosAndUtilitiesDir}/validation_functions.py`),
      this.destinationPath(`${destDtosAndUtilitiesDir}/validation_functions.py`)
    );

    this.fs.copyTpl(
      this.templatePath(`${srcDtosAndUtilitiesDir}/db_helpers.py`),
      this.destinationPath(`${destDtosAndUtilitiesDir}/db_helpers.py`),
      {
        projectName: this.props.name,
        lcPrefix: lcPrefix
      }
    );

    this.fs.copy(
      this.templatePath(`${srcDtosAndUtilitiesDir}/errors.py`),
      this.destinationPath(`${destDtosAndUtilitiesDir}/errors.py`)
    );

    this.fs.copyTpl(
      this.templatePath(`${srcDtosAndUtilitiesDir}/logging.py`),
      this.destinationPath(`${destDtosAndUtilitiesDir}/logging.py`),
      {
        projectName: this.props.name,
        lcPrefix: lcPrefix
      }
    );

    this.fs.copy(
      this.templatePath(`${srcDtosAndUtilitiesDir}/name_strings.py`),
      this.destinationPath(`${destDtosAndUtilitiesDir}/name_strings.py`)
    );

    this.fs.copyTpl(
      this.templatePath(`${srcDtosAndUtilitiesDir}/file_reference.py`),
      this.destinationPath(`${destDtosAndUtilitiesDir}/file_reference.py`),
      {
        devOpsUtilitiesFile: devOpsUtilitiesFile
      }
    );

    this.fs.copy(
      this.templatePath(`${srcDtosAndUtilitiesDir}/__init__.py`),
      this.destinationPath(`${destDtosAndUtilitiesDir}/__init__.py`)
    );

    this.fs.copy(
      this.templatePath("src/libs/dev/ssl/installed_certs/__main__.py"),
      this.destinationPath(
        `src/${this.props.name}_libs/dev/ssl/installed_certs/__main__.py`
      )
    );

    this.fs.copy(
      this.templatePath("src/libs/tables.py"),
      this.destinationPath(`src/${this.props.name}_libs/tables.py`)
    );

    const srcServicesDir = `src/libs/services`;
    const destServicesDir = `src/${this.props.name}_libs/services`;

    this.fs.copyTpl(
      this.templatePath(`${srcServicesDir}/env_manager.py`),
      this.destinationPath(`${destServicesDir}/env_manager.py`),
      {
        projectName: this.props.name,
        ucPrefix: ucPrefix
      }
    );

    this.fs.copyTpl(
      this.templatePath(`${srcServicesDir}/db_setup_service.py`),
      this.destinationPath(`${destServicesDir}/db_setup_service.py`),
      {
        projectName: this.props.name
      }
    );

    this.fs.copyTpl(
      this.templatePath(`${srcServicesDir}/process_service.py`),
      this.destinationPath(`${destServicesDir}/process_service.py`),
      {
        projectName: this.props.name
      }
    );

    this.fs.copyTpl(
      this.templatePath(`${srcServicesDir}/template_service.py`),
      this.destinationPath(`${destServicesDir}/template_service.py`),
      {
        projectName: this.props.name
      }
    );

    this.fs.copyTpl(
      this.templatePath(`${srcServicesDir}/accounts_service.py`),
      this.destinationPath(`${destServicesDir}/accounts_service.py`),
      {
        projectName: this.props.name
      }
    );

    this.fs.copyTpl(
      this.templatePath(`${srcServicesDir}/user_actions_history_service.py`),
      this.destinationPath(
        `${destServicesDir}/user_actions_history_service.py`
      ),
      {
        projectName: this.props.name
      }
    );

    this.fs.copy(
      this.templatePath(`${srcServicesDir}/__init__.py`),
      this.destinationPath(`${destServicesDir}/__init__.py`)
    );

    this.fs.copy(
      this.templatePath("src/libs/__init__.py"),
      this.destinationPath(`src/${this.props.name}_libs/__init__.py`)
    );

    this.fs.copyTpl(
      this.templatePath("src/api/api_error.py"),
      this.destinationPath("src/api/api_error.py"),
      {
        projectName: this.props.name
      }
    );

    this.fs.copyTpl(
      this.templatePath("src/api/api_dependencies.py"),
      this.destinationPath("src/api/api_dependencies.py"),
      {
        projectName: this.props.name
      }
    );

    this.fs.copyTpl(
      this.templatePath("src/api/accounts_controller.py"),
      this.destinationPath("src/api/accounts_controller.py"),
      {
        projectName: this.props.name
      }
    );

    this.fs.copyTpl(
      this.templatePath("src/api/index.py"),
      this.destinationPath("src/api/index.py"),
      {
        projectName: this.props.name
      }
    );

    this.fs.copyTpl(
      this.templatePath("src/api/accounts_controller.py"),
      this.destinationPath("src/api/accounts_controller.py"),
      {
        projectName: this.props.name
      }
    );

    this.fs.copyTpl(
      this.templatePath("src/api/api_dependencies.py"),
      this.destinationPath("src/api/api_dependencies.py"),
      {
        projectName: this.props.name
      }
    );

    this.fs.copyTpl(
      this.templatePath("templates/env_api"),
      this.destinationPath("templates/.env_api"),
      {
        ucPrefix: ucPrefix
      }
    );

    this.fs.copyTpl(
      this.templatePath("templates/env_api"),
      this.destinationPath("templates/.env_api"),
      {
        ucPrefix: ucPrefix
      }
    );

    this.fs.copy(
      this.templatePath("templates/nginx_evil.conf"),
      this.destinationPath("templates/nginx_evil.conf")
    );

    this.fs.copyTpl(
      this.templatePath("templates/nginx_template.conf"),
      this.destinationPath("templates/nginx_template.conf"),
      {
        ucPrefix: ucPrefix
      }
    );

    this.fs.copyTpl(
      this.templatePath("templates/nginx_template.conf"),
      this.destinationPath("templates/nginx_template.conf"),
      {
        ucPrefix: ucPrefix
      }
    );

    this.fs.copy(
      this.templatePath("src/client/eslintrc.js"),
      this.destinationPath("src/client/.eslintrc.js")
    );

    this.fs.copy(
      this.templatePath("src/client/index.html"),
      this.destinationPath("src/client/index.html")
    );

    this.fs.copyTpl(
      this.templatePath("src/client/package.json"),
      this.destinationPath("src/client/package.json"),
      {
        projectName: this.props.name,
        devOpsUtilitiesFile: devOpsUtilitiesFile
      }
    );

    this.fs.copy(
      this.templatePath("src/client/tsconfig.json"),
      this.destinationPath("src/client/tsconfig.json")
    );

    this.fs.copy(
      this.templatePath("src/client/vite-env.d.ts"),
      this.destinationPath("src/client/vite-env.d.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/vite.config.ts"),
      this.destinationPath("src/client/vite.config.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Types/generic_types.ts"),
      this.destinationPath("src/client/src/Types/generic_types.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Types/pageable_types.ts"),
      this.destinationPath("src/client/src/Types/pageable_types.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Types/user_types.ts"),
      this.destinationPath("src/client/src/Types/user_types.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Types/browser_types.ts"),
      this.destinationPath("src/client/src/Types/browser_types.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Types/reducer_types.ts"),
      this.destinationPath("src/client/src/Types/reducer_types.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/App.css"),
      this.destinationPath("src/client/src/App.css")
    );

    this.fs.copy(
      this.templatePath("src/client/src/constants.ts"),
      this.destinationPath("src/client/src/constants.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/index.css"),
      this.destinationPath("src/client/src/index.css")
    );

    this.fs.copy(
      this.templatePath("src/client/src/style_config.ts"),
      this.destinationPath("src/client/src/style_config")
    );

    this.fs.copyTpl(
      this.templatePath("src/client/src/AppRoot.tsx"),
      this.destinationPath("src/client/src/AppRoot.tsx"),
      {
        title: this.props.name
      }
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Navigation/NavRoutes.tsx"),
      this.destinationPath("src/client/src/Components/Navigation/NavRoutes.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Shared/ErrorBoundary.tsx"),
      this.destinationPath("src/client/src/Components/Shared/ErrorBoundary.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Shared/FormFileUpload.tsx"),
      this.destinationPath(
        "src/client/src/Components/Shared/FormFileUpload.tsx"
      )
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Shared/FormSelect.tsx"),
      this.destinationPath("src/client/src/Components/Shared/FormSelect.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Shared/FormTextField.tsx"),
      this.destinationPath("src/client/src/Components/Shared/FormTextField.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Shared/Loader.tsx"),
      this.destinationPath("src/client/src/Components/Shared/Loader.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Shared/OptionsButton.tsx"),
      this.destinationPath("src/client/src/Components/Shared/OptionsButton.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Shared/PrivateRoute.tsx"),
      this.destinationPath("src/client/src/Components/Shared/PrivateRoute.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Shared/RoutingErrors.tsx"),
      this.destinationPath("src/client/src/Components/Shared/RoutingErrors.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Shared/SubmitButton.tsx"),
      this.destinationPath("src/client/src/Components/Shared/SubmitButton.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Shared/UrlPagination.tsx"),
      this.destinationPath("src/client/src/Components/Shared/UrlPagination.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Shared/YesNoControl.tsx"),
      this.destinationPath("src/client/src/Components/Shared/YesNoControl.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Users/UserEdit.tsx"),
      this.destinationPath("src/client/src/Components/Users/UserEdit.tsx")
    );

    this.fs.copyTpl(
      this.templatePath("src/client/src/Components/Users/UserList.tsx"),
      this.destinationPath("src/client/src/Components/Users/UserList.tsx"),
      {
        title: this.props.name
      }
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Users/UserLoginModal.tsx"),
      this.destinationPath("src/client/src/Components/Users/UserLoginModal.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Users/UserLoginForm.tsx"),
      this.destinationPath("src/client/src/Components/Users/UserLoginForm.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Users/UserNew.tsx"),
      this.destinationPath("src/client/src/Components/Users/UserNew.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Users/UserMenu.tsx"),
      this.destinationPath("src/client/src/Components/Users/UserMenu.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Users/UserSearch.tsx"),
      this.destinationPath("src/client/src/Components/Users/UserSearch.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Users/RoleView.tsx"),
      this.destinationPath("src/client/src/Components/Users/RoleView.tsx")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Components/Users/RoleEntry.tsx"),
      this.destinationPath("src/client/src/Components/Users/RoleEntry.tsx")
    );

    this.fs.copy(
      this.templatePath(
        "src/client/src/Components/Users/SiteUserRoleAssignmentTable.tsx"
      ),
      this.destinationPath(
        "src/client/src/Components/Users/SiteUserRoleAssignmentTable.tsx"
      ),
      {
        title: this.props.name
      }
    );

    this.fs.copy(
      this.templatePath(
        "src/client/src/Components/Users/UserRoleAssignmentTable.tsx"
      ),
      this.destinationPath(
        "src/client/src/Components/Users/UserRoleAssignmentTable.tsx"
      )
    );

    this.fs.copy(
      this.templatePath("src/client/src/API_Calls/api.ts"),
      this.destinationPath("src/client/src/API_Calls/api.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/API_Calls/userCalls.ts"),
      this.destinationPath("src/client/src/API_Calls/userCalls.ts")
    );

    this.fs.copy(
      this.templatePath(
        "src/client/src/Context_Providers/AppContext/AppContext.ts"
      ),
      this.destinationPath(
        "src/client/src/Context_Providers/AppContext/AppContext.ts"
      )
    );

    this.fs.copy(
      this.templatePath(
        "src/client/src/Context_Providers/AppContext/AppContextProvider.tsx"
      ),
      this.destinationPath(
        "src/client/src/Context_Providers/AppContext/AppContextProvider.tsx"
      )
    );

    this.fs.copy(
      this.templatePath(
        "src/client/src/Context_Providers/AuthContext/AuthContext.ts"
      ),
      this.destinationPath(
        "src/client/src/Context_Providers/AuthContext/AuthContext.ts"
      )
    );

    this.fs.copy(
      this.templatePath(
        "src/client/src/Context_Providers/AuthContext/AuthContextProvider.tsx"
      ),
      this.destinationPath(
        "src/client/src/Context_Providers/AuthContext/AuthContextProvider.tsx"
      )
    );

    this.fs.copy(
      this.templatePath("src/client/src/Helpers/array_helpers.ts"),
      this.destinationPath("src/client/src/Helpers/array_helpers.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Helpers/browser_helpers.ts"),
      this.destinationPath("src/client/src/Helpers/browser_helpers.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Helpers/compare_helpers.ts"),
      this.destinationPath("src/client/src/Helpers/compare_helpers.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Helpers/error_formatter.ts"),
      this.destinationPath("src/client/src/Helpers/error_formatter.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Helpers/pageable_helpers.ts"),
      this.destinationPath("src/client/src/Helpers/pageable_helpers.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Helpers/request_helpers.ts"),
      this.destinationPath("src/client/src/Helpers/request_helpers.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Helpers/rule_helpers.ts"),
      this.destinationPath("src/client/src/Helpers/rule_helpers.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Helpers/time_helper.ts"),
      this.destinationPath("src/client/src/Helpers/time_helper.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Helpers/validation_helpers.ts"),
      this.destinationPath("src/client/src/Helpers/validation_helpers.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Reducers/dataWaitingReducer.ts"),
      this.destinationPath("src/client/src/Reducers/dataWaitingReducer.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Reducers/reducerStores.ts"),
      this.destinationPath("src/client/src/Reducers/reducerStores.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Reducers/keyedDataWaitingReducer.ts"),
      this.destinationPath("src/client/src/Reducers/keyedDataWaitingReducer.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Reducers/keyedVoidWaitingReducer.ts"),
      this.destinationPath("src/client/src/Reducers/keyedVoidWaitingReducer.ts")
    );

    this.fs.copy(
      this.templatePath("src/client/src/Reducers/voidWaitingReducer.ts"),
      this.destinationPath("src/client/src/Reducers/voidWaitingReducer.ts")
    );

    this.fs.copy(
      this.templatePath("src/tests/mocks/__init__.py"),
      this.destinationPath("src/tests/mocks/__init__.py")
    );

    this.fs.copyTpl(
      this.templatePath("src/tests/mocks/constant_values_defs.py"),
      this.destinationPath("src/tests/mocks/constant_values_defs.py"),
      { projectName: this.props.name }
    );

    this.fs.copyTpl(
      this.templatePath("src/tests/mocks/db_data.py"),
      this.destinationPath("src/tests/mocks/db_data.py"),
      { projectName: this.props.name }
    );

    this.fs.copyTpl(
      this.templatePath("src/tests/mocks/db_population.py"),
      this.destinationPath("src/tests/mocks/db_population.py"),
      { projectName: this.props.name }
    );

    this.fs.copy(
      this.templatePath("src/tests/mocks/mock_datetime_provider.py"),
      this.destinationPath("src/tests/mocks/mock_datetime_provider.py")
    );

    this.fs.copyTpl(
      this.templatePath("src/tests/mocks/mock_db_constructors.py"),
      this.destinationPath("src/tests/mocks/mock_db_constructors.py"),
      { projectName: this.props.name }
    );

    this.fs.copy(
      this.templatePath("src/tests/mocks/special_strings_reference.py"),
      this.destinationPath("src/tests/mocks/special_strings_reference.py")
    );

    this.fs.copy(
      this.templatePath("src/tests/__init__.py"),
      this.destinationPath("src/tests/__init__.py")
    );

    this.fs.copy(
      this.templatePath("src/tests/api_test_dependencies.py"),
      this.destinationPath("src/tests/api_test_dependencies.py")
    );

    this.fs.copyTpl(
      this.templatePath("src/tests/common_fixtures.py"),
      this.destinationPath("src/tests/common_fixtures.py"),
      { projectName: this.props.name }
    );

    this.fs.copyTpl(
      this.templatePath("src/tests/constant_fixtures_for_test.py"),
      this.destinationPath("src/tests/constant_fixtures_for_test.py"),
      { projectName: this.props.name }
    );

    this.fs.copy(
      this.templatePath("src/tests/helpers.py"),
      this.destinationPath("src/tests/helpers.py")
    );

    this.fs.copyTpl(
      this.templatePath("src/tests/test_account_service.py"),
      this.destinationPath("src/tests/test_account_service.py"),
      { projectName: this.props.name }
    );

    this.fs.copyTpl(
      this.templatePath("src/tests/test_accounts_controller.py"),
      this.destinationPath("src/tests/test_accounts_controller.py"),
      { projectName: this.props.name }
    );

    this.fs.copyTpl(
      this.templatePath("src/tests/test_dtos.py"),
      this.destinationPath("src/tests/test_dtos.py"),
      { projectName: this.props.name }
    );

    this.fs.copy(
      this.templatePath("src/tests/test_fast_api.py"),
      this.destinationPath("src/tests/test_fast_api.py")
    );

    this.fs.copyTpl(
      this.templatePath("src/tests/test_in_mem_db.py"),
      this.destinationPath("src/tests/test_in_mem_db.py"),
      { projectName: this.props.name }
    );

    this.fs.copy(
      this.templatePath("src/tests/test_python.py"),
      this.destinationPath("src/tests/test_python.py")
    );

    this.fs.copyTpl(
      this.templatePath("src/tests/test_simple_functions.py"),
      this.destinationPath("src/tests/test_simple_functions.py"),
      { projectName: this.props.name }
    );

    this.fs.copyTpl(
      this.templatePath("src/tests/test_test_env.py"),
      this.destinationPath("src/tests/test_test_env.py"),
      { projectName: this.props.name }
    );

    this.fs.copy(
      this.templatePath("src/tests/pytest.ini"),
      this.destinationPath("src/tests/pytest.ini")
    );
  }

  install() {
    this.installDependencies();
  }
};
