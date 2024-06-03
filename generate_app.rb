require 'fileutils'
require_relative "generate_app_util"
require_relative "generate_python_api"
require_relative "generate_react_ts"
require_relative "generate_no_framework"


include AppGenUtils




pythonChoice = 2
reactTsChoice = 2

apiLangMap = {
	1 => { name: "", display: "Nothing" },
	2 => { name: "python", display: "Python 3" }
}

feLangMap = {
	1 => { name: "", display: "Nothing" },
	2 => { name: "react-ts", display: "react/typescript" }
}

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

apiLangChoice = -1
loop do
	puts "Api Language? Default: 2) #{apiLangMap[pythonChoice][:display]}"
	apiLangMap.keys.sort.each {|e| puts "#{e}) #{apiLangMap[e][:display]}"}
	apiLangInput = gets.chomp
	if apiLangInput.strip.empty?
		apiLangChoice = pythonChoice
	else
		apiLangChoice = apiLangInput.to_i
	end
	break if apiLangMap.has_key?(apiLangChoice)
	puts "#{apiLangInput} is invalid. Try again."
end


feLangChoice = -1
loop do
	puts "Select front end Language? Default: "\
		"#{reactTsChoice}) #{feLangMap[reactTsChoice][:display]}"
	feLangMap.keys.sort.each {|e| puts "#{e}) #{feLangMap[e][:display]}"}
	feLangInput = gets.chomp
	if feLangInput.strip.empty?
		feLangChoice = reactTsChoice
	else
		feLangChoice = feLangInput.to_i
	end
	break if feLangMap.has_key?(feLangChoice)
	puts "#{feLangInput} is invalid. Try again."
end


if prefix.strip.empty?
	prefix = defaultPrefix
end


lcPrefix = prefix.downcase
ucPrefix = prefix.upcase
devOpsFile = "#{lcPrefix}_dev_ops"
projectNameLc = projectName.downcase
projectNameSnake = to_snake(projectName)
projectNameFlat = to_flat(projectName)

if apiLangChoice == pythonChoice
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
	apiLang: apiLangMap[apiLangChoice][:name],
	feLang: feLangMap[feLangChoice][:name],
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

if apiLangChoice == pythonChoice
	AppGenPythons::generate(choices)
end

if feLangChoice == reactTsChoice
	AppGenReactTs::generate(choices)
else
	AppGenNoFramework::generate(choices)
end


