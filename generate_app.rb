require 'fileutils'
require_relative "generate_app_util"
require_relative "generate_python_api"
require_relative "generate_react_ts"
require_relative "generate_no_framework"


include AppGenUtils




pythonConst = "python"
reactTsConst = "react-ts"

puts "Project Name?"
projectName = gets.chomp

puts "Project Prefix?"
prefix = gets.chomp

puts "Api Language? Default: #{pythonConst}"
apiLang = gets.chomp

puts "Front end Language? Default: #{reactTsConst}"
feLang = gets.chomp


if prefix.strip.empty?
	prefix = build_default_prefix(projectName)
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
devOpsFile = "#{lcPrefix}_dev_ops"
lcProjectName = projectName.downcase

if apiLang == pythonConst
	db = "mysql"
else
	db = ""
end

choices = {
	devOpsFile: devOpsFile,
	projectName: projectName,
	lcProjectName: lcProjectName,
	ucPrefix: ucPrefix,
	lcPrefix: lcPrefix,
	title: projectName,
	apiLang: apiLang,
	feLang: feLang,
	db: db
}

if File.exists?("./output")
	FileUtils.remove_dir("./output")
end

copy_tpl(
	"gitignore", 
	".gitignore", 
	choices
)

copy_tpl(
	"dev_ops.sh", 
	"#{devOpsFile}.sh", 
	choices
)


copy_tpl(
	"deploy_to_server.sh",
	"deploy_to_server.sh",
	choices
)

copy_tpl(
	".vscode/launch.json",
	".vscode/launch.json",
	choices
)

copy_tpl(
	".vscode/settings.json",
	".vscode/settings.json",
	choices
)

copy_tpl(
	".vscode/tasks.json",
	".vscode/tasks.json",
	choices
)

copy_tpl(
	"install_script.sh",
	"install_script.sh",
	choices
)

if apiLang == pythonConst
	AppGenPythons::generate(choices)
end

if feLang == reactTsConst
	AppGenReactTs::generate(choices)
else
	AppGenNoFramework::generate(choices)
end

copy_tpl(
	"templates/env_api",
	"templates/.env_api",
	choices
)

copy_tpl(
	"templates/nginx_evil.conf",
	"templates/nginx_evil.conf"
)

copy_tpl(
	"templates/nginx_template.conf",
	"templates/nginx_template.conf",
	choices
)

copy_tpl(
	"templates/nginx_template.conf",
	"templates/nginx_template.conf",
	choices
)


