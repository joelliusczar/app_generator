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

while not projectName =~ /^[A-Za-z][A-Za-z0-9 _-]*$/
	puts "\"#{projectName}\" is invalid. Try again"
	projectName = gets.chomp
end

defaultPrefix = build_default_prefix(projectName)

puts "Project Prefix? #{defaultPrefix}"
prefix = gets.chomp

if prefix.strip.empty?
	prefix = defaultPrefix
end

while not prefix =~ /^[A-Za-z][A-Za-z0-9]*$/
	puts "#{prefix} is invalid. Try again"
	prefix = gets.chomp
end

puts "Api Language? Default: #{pythonConst}"
apiLang = gets.chomp

puts "Front end Language? Default: #{reactTsConst}"
feLang = gets.chomp


if prefix.strip.empty?
	prefix = defaultPrefix
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
projectNameLc = projectName.downcase
projectNameSnake = to_snake(projectName)
projectNameFlat = to_flat(projectName)

if apiLang == pythonConst
	db = "mysql"
else
	db = ""
end

choices = {
	devOpsFile: devOpsFile,
	projectName: projectName,
	projectNameLc: projectNameLc,
	projectNameSnake: projectNameSnake,
	projectNameFlat: projectNameFlat,
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
	"deploy.sh",
	"deploy.sh",
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
	"install.sh",
	"install.sh",
	choices
)

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

copy_tpl(
	"dev_ops_libs/python/installed_certs/__main__.py",
	"#{projectNameSnake}_dev_ops/installed_certs/__main__.py"
)

copy_tpl(
	"requirements.txt",
	"requirements.txt"
)

if apiLang == pythonConst
	AppGenPythons::generate(choices)
end

if feLang == reactTsConst
	AppGenReactTs::generate(choices)
else
	AppGenNoFramework::generate(choices)
end


