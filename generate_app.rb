require 'fileutils'
require_relative "generate_app_util"
require_relative "generate_python_api"
require_relative "generate_react_ts"


include AppGenUtils
include AppGenPythons
include AppGenReactTs



pythonConst = "python"
reactTsConst = "react-ts"

puts "Project Name?"
appName = gets.chomp

puts "Project Prefix?"
prefix = gets.chomp

puts "Api Language? Default: #{pythonConst}"
apiLang = gets.chomp

puts "Front end Language? Default: #{reactTsConst}"
feLang = gets.chomp


if prefix.strip.empty?
	prefix = build_default_prefix(appName)
end

if apiLang.strip.empty?
	apiLang = pythonConst
end

if feLang.strip.empty?
	feLang = reactTsConst
end

apiLang = apiLang.strip.downcase
feLang = feLang.strip.downcase


lcPrefix = prefix.downcase
ucPrefix = prefix.upcase
devOpsUtilitiesFile = "#{lcPrefix}_dev_ops_utilities"
lcAppName = appName.downcase

choices = {
	devOpsUtilitiesFile: devOpsUtilitiesFile,
	projectName: appName,
	lcProjectName: lcAppName,
	ucPrefix: ucPrefix,
	lcPrefix: lcPrefix,
}

if File.exists?("./output")
	FileUtils.remove_dir("./output")
end

copy_tpl(
	"gitignore", 
	".gitignore", 
	{ projectName: appName }
)

copy_tpl(
	"dev_ops_utilities.sh", 
	"#{devOpsUtilitiesFile}.sh", 
	{
		projectName: appName,
		lcProjectName: lcAppName,
		ucPrefix: ucPrefix,
		lcPrefix: lcPrefix,
	}
)



copy_tpl(
	"deploy_to_server.sh",
	"deploy_to_server.sh",
	{
		devOpsUtilitiesFile: devOpsUtilitiesFile,
		projectName: appName,
		ucPrefix: ucPrefix,
		lcPrefix: lcPrefix
	}
)

copy_tpl(
	".vscode/launch.json",
	".vscode/launch.json",
	{
		projectName: appName,
		ucPrefix: ucPrefix,
		lcPrefix: lcPrefix
	}
)

copy_tpl(
	".vscode/settings.json",
	".vscode/settings.json",
	{
		projectName: appName,
		ucPrefix: ucPrefix,
		lcPrefix: lcPrefix
	}
)

copy_tpl(
	".vscode/tasks.json",
	".vscode/tasks.json",
	{
		devOpsUtilitiesFile: devOpsUtilitiesFile
	}
)

copy_tpl(
	"install_script.sh",
	"install_script.sh",
	{
		devOpsUtilitiesFile: devOpsUtilitiesFile,
		ucPrefix: ucPrefix,
		lcPrefix: lcPrefix
	}
)

if apiLang == pythonConst
	generate_python_api(appName, ucPrefix, lcPrefix, devOpsUtilitiesFile)
end

if feLang == reactTsConst
	generate_react_ts(appName, ucPrefix, lcPrefix, devOpsUtilitiesFile)
end

copy_tpl(
	"templates/env_api",
	"templates/.env_api",
	{
		ucPrefix: ucPrefix
	}
)

copy_tpl(
	"templates/nginx_evil.conf",
	"templates/nginx_evil.conf"
)

copy_tpl(
	"templates/nginx_template.conf",
	"templates/nginx_template.conf",
	{
		ucPrefix: ucPrefix
	}
)

copy_tpl(
	"templates/nginx_template.conf",
	"templates/nginx_template.conf",
	{
		ucPrefix: ucPrefix
	}
)


