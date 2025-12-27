require 'fileutils'
require_relative "generate_app_util"

include AppGenUtils

module AppGenJava
	def self.generate(choices)

		projectName = choices.local_variable_get(:projectName)
		projectNameSnake = choices.local_variable_get(:projectNameSnake)

		fromTop = "java"

		copy_tpl(
			"src/java/gitattributes",
			"src/.gitattributes"
		)

		copy_tpl(
			"src/java/gradlew",
			"src/gradlew"
		)

		copy_tpl(
			"src/java/settings.gradle",
			"src/settings.gradle",
			choices
		)

		appDirSrc = "src/java/app"
		appDirDest = "src/app"

		copy_tpl(
			"#{appDirSrc}/build.gradle",
			"#{appDirDest}/build.gradle",
			choices
		)

		appDirMainSrc = "#{appDirSrc}/src/main "
		appDirMainDest = "#{appDirDest}/src/main"

		copy_tpl(
			"#{appDirMainSrc}/resources/application.yml",
			"#{appDirMainDest}/resources/application.yml"
		)

		appCodeSrc = "#{appDirMainSrc}/java/generated_app/app"
		appCodeDest = "#{appDirMainDest}/java/#{projectNameSnake.downcase}/app"

		copy_tpl(
			"#{appCodeSrc}/App.java",
			"#{appCodeDest}/App.java",
			choices
		)

		copy_tpl(
			"#{appCodeSrc}/AppDependencies.java",
			"#{appCodeDest}/AppDependencies.java",
			choices
		)

		copy_tpl(
			"#{appCodeSrc}/controllers/LookupsController.java",
			"#{appCodeDest}/controllers/LookupsController.java",
			choices
		)

		buildSrcDirSrc = "src/java/buildSrc"
		buildSrcDirDest = "src/buildSrc"

		copy_tpl(
			"#{buildSrcDirSrc}/build.gradle",
			"#{buildSrcDirDest}/build.gradle",
			choices
		)

		copy_tpl(
			"#{buildSrcDirSrc}/settings.gradle",
			"#{buildSrcDirDest}/settings.gradle"
		)

		buildSrcDslDirSrc = "#{buildSrcDirSrc}/src/main/groovy"
		buildSrcDslDirDest = "#{buildSrcDirDest}/src/main/groovy"

		copy_tpl(
			"#{buildSrcDslDirSrc}/buildlogic.java-application-conventions.gradle",
			"#{buildSrcDslDirDest}/buildlogic.java-application-conventions.gradle"
		)

		copy_tpl(
			"#{buildSrcDslDirSrc}/buildlogic.java-common-conventions.gradle",
			"#{buildSrcDslDirDest}/buildlogic.java-common-conventions.gradle"
		)

		copy_tpl(
			"#{buildSrcDslDirSrc}/buildlogic.java-library-conventions.gradle",
			"#{buildSrcDslDirDest}/buildlogic.java-library-conventions.gradle"
		)

		engineDirSrc = "src/java/engine"
		engineDirDest = "src/engine"

		copy_tpl(
			"#{engineDirSrc}/build.gradle",
			"#{engineDirDest}/build.gradle",
			choices
		)

		engineSrcTopDirSrc = "#{engineDirSrc}/src/main/java/generated_lib/engine"
		engineSrcTopDirDest = "#{engineDirDest}/src/main/java/#{projectNameSnake.downcase}/engine"

		mkdir("#{engineSrcTopDirDest}/constants")
		
		engineDtosDirSrc = "#{engineSrcTopDirSrc}/dtos"
		engineDtosDirDest = "#{engineSrcTopDirDest}/dtos"
		copy_tpl(
			"#{engineDtosDirSrc}/Lookups.java",
			"#{engineDtosDirDest}/Lookups.java",
			choices
		)

		copy_tpl(
			"#{engineDtosDirSrc}/NamedId.java",
			"#{engineDtosDirDest}/NamedId.java",
			choices
		)

		engineInterfacesDirSrc = "#{engineSrcTopDirSrc}/interfaces"
		engineInterfacesDirDest = "#{engineSrcTopDirDest}/interfaces"
		copy_tpl(
			"#{engineInterfacesDirSrc}/FriendlyNameable.java",
			"#{engineInterfacesDirDest}/FriendlyNameable.java",
			choices
		)

		engineServicesDirSrc = "#{engineSrcTopDirSrc}/services"
		engineServicesDirDest = "#{engineSrcTopDirDest}/services"
		copy_tpl(
			"#{engineServicesDirSrc}/LookupsService.java",
			"#{engineServicesDirDest}/LookupsService.java",
			choices
		)

		engineUtilitiesDirSrc = "#{engineSrcTopDirSrc}/utilities"
		engineUtilitiesDirDest = "#{engineSrcTopDirDest}/utilities"
		copy_tpl(
			"#{engineUtilitiesDirSrc}/EnumUtils.java",
			"#{engineUtilitiesDirDest}/EnumUtils.java",
			choices
		)

		gradleDirSrc = "src/java/gradle"
		gradleDirDest = "src/gradle"

		copy_tpl(
			"#{gradleDirSrc}/libs.versions.toml",
			"#{gradleDirDest}/libs.versions.toml"
		)

		gradleWrapperDirSrc = "#{gradleDirSrc}/wrapper"
		gradleWrapperDirDest = "#{gradleDirDest}/wrapper"
		copy_tpl(
			"#{gradleWrapperDirSrc}/gradle-wrapper.properties",
			"#{gradleWrapperDirDest}/gradle-wrapper.properties",
			choices
		)

		copy_raw(
			"#{gradleWrapperDirSrc}/gradle-wrapper.jar",
			"#{gradleWrapperDirDest}/gradle-wrapper.jar"
		)

	end
end