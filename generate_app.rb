require 'fileutils'
require_relative "generate_app_util"
require_relative "generate_python_api"
require_relative "generate_react_ts"
require_relative "generate_no_framework"
require_relative "generate_java_app"
require_relative "generate_vue_ts"


include AppGenUtils

LangChoice = Struct.new("LangChoice",:key,:name, :display, :classTag)


module API_CHOICE_KEYS
	NONE = 1
	PYTHON = 2
	JAVA = 3
end

module CLIENT_CHOICE_KEYS
	NONE = 1
	REACT_TYPESCRIPT = 2
	VUE_TYPESCRIPT = 3
end

module DB_CHOICE_KEYS
	NONE = 1
	MY_SQL = 2
	POSTGRESQL = 3
end

apiLangMap = {
	API_CHOICE_KEYS::NONE => 
		LangChoice.new(
			API_CHOICE_KEYS::NONE,
			"",
			"Nothing",
			""
		),
	API_CHOICE_KEYS::PYTHON => 
		LangChoice.new(
			API_CHOICE_KEYS::PYTHON,
			"python",
			"Python 3",
			""
		),
	API_CHOICE_KEYS::JAVA => 
		LangChoice.new(
			API_CHOICE_KEYS::JAVA,
			"java",
			"Java",
			""
		)
}

feLangMap = {
	CLIENT_CHOICE_KEYS::NONE => 
		LangChoice.new(
			CLIENT_CHOICE_KEYS::NONE,
			"",
			"Nothing",
			""
		),
	CLIENT_CHOICE_KEYS::REACT_TYPESCRIPT =>
		LangChoice.new(
			CLIENT_CHOICE_KEYS::REACT_TYPESCRIPT,
			"react-ts",
			"react/typescript",
			""
		),
	CLIENT_CHOICE_KEYS::VUE_TYPESCRIPT =>
		LangChoice.new(
			CLIENT_CHOICE_KEYS::VUE_TYPESCRIPT,
			"vue-ts",
			"vue/typescript",
			""
		)
}

dbMap = {
	DB_CHOICE_KEYS::NONE => LangChoice.new(
		DB_CHOICE_KEYS::NONE,
		"",
		"Nothing"
	),
	DB_CHOICE_KEYS::MY_SQL => 
		LangChoice.new(
			DB_CHOICE_KEYS::MY_SQL,
			"mysql",
			"MySql"
		),
	DB_CHOICE_KEYS::POSTGRESQL => 
		LangChoice.new(
			DB_CHOICE_KEYS::POSTGRESQL,
			"postgresql",
			"PostgreSql"
		)
}

api_class_map = {
	API_CHOICE_KEYS::NONE => "SaladPrep::StaticAPILauncher",
	API_CHOICE_KEYS::PYTHON => "SaladPrep::PyAPILauncher",
	API_CHOICE_KEYS::JAVA => "SaladPrep::JavaAPILauncher",
}

db_class_map = {
	DB_CHOICE_KEYS::NONE => "SaladPrep::NoopAss",
	DB_CHOICE_KEYS::MY_SQL => "SaladPrep::MyAss",
	DB_CHOICE_KEYS::POSTGRESQL => "SaladPrep::PostGrass"
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
	puts "Api Language? Default: "\
		"#{API_CHOICE_KEYS::PYTHON}) #{apiLangMap[API_CHOICE_KEYS::PYTHON].display}"
	apiLangMap.keys.sort.each {|e| puts "#{e}) #{apiLangMap[e].display}"}
	apiLangInput = gets.chomp
	if apiLangInput.strip.empty?
		apiLangChoice = API_CHOICE_KEYS::PYTHON
	else
		apiLangChoice = apiLangInput.to_i
	end
	break if apiLangMap.has_key?(apiLangChoice)
	puts "#{apiLangInput} is invalid. Try again."
end


feLangChoice = -1
loop do
	puts "Select front end Language? Default: "\
		"#{CLIENT_CHOICE_KEYS::REACT_TYPESCRIPT})"\
		" #{feLangMap[CLIENT_CHOICE_KEYS::REACT_TYPESCRIPT].display}"
	feLangMap.keys.sort.each {|e| puts "#{e}) #{feLangMap[e].display}"}
	feLangInput = gets.chomp
	if feLangInput.strip.empty?
		feLangChoice = CLIENT_CHOICE_KEYS::REACT_TYPESCRIPT
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
projectNameLc = projectName.downcase
projectNameSnake = to_snake(projectName)
projectNameFlat = to_flat(projectName)

if apiLangChoice == API_CHOICE_KEYS::PYTHON
	dbChoice = dbMap[DB_CHOICE_KEYS::MY_SQL]
elsif if apiLangChoice == API_CHOICE_KEYS::JAVA
	dbChoice = dbMap[DB_CHOICE_KEYS::POSTGRESQL]
else
	dbChoice = dbMap[DB_CHOICE_KEYS::NONE]
end

ruby_version = "3.3.5"
projectName = projectName
projectNameLc = projectNameLc
projectNameSnake = projectNameSnake
projectNameFlat = projectNameFlat
ucPrefix = ucPrefix
lcPrefix = lcPrefix
title = projectName
apiLang = apiLangMap[apiLangChoice]
feLang = feLangMap[feLangChoice]
db = dbChoice


if File.exist?("./output")
	FileUtils.remove_dir("./output")
end

choices = binding

copy_tpl(
	"gitignore",
	".gitignore",
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
	"dev_ops/tool-versions",
	"dev_ops/.tool-versions"
)

copy_tpl(
	"dev_ops/dev_ops.rb",
	"dev_ops/dev_ops.rb",
	choices
)

copy_tpl(
	"dev_ops/Gemfile",
	"dev_ops/Gemfile"
)

copy_tpl(
	"dev_ops/ruby_dependency_install.sh",
	"dev_ops/ruby_dependency_install.sh",
	choices
)


copy_tpl(
	"readme.md",
	"README.md",
	choices
)


if apiLang.key == API_CHOICE_KEYS::PYTHON
	AppGenPythons::generate(choices)
elsif apiLang.key == API_CHOICE_KEYS::JAVA
	AppGenJava::generate(choices)
end

if feLang.key == CLIENT_CHOICE_KEYS::REACT_TYPESCRIPT
	AppGenReactTs::generate(choices)
elsif feLang.key == CLIENT_CHOICE_KEYS::VUE_TYPESCRIPT
	AppGenVueTs::generate(choices)
else
	AppGenNoFramework::generate(choices)
end


