require 'fileutils'
require 'erb'

module AppGenUtils

	def build_default_prefix(projectName)
		projectName.split(/([A-Z\-_ ][a-z0-9]*)/)
			.select {|x| x != "" && x != "-" && x != "_" && x != " "}
			.map {|x| x.strip[0]}
			.join
	end

	def to_snake(projectName, casing = nil)
		if not casing
			casing = "low"
		end
		projectName = projectName
			.delete("^a-zA-Z0-9 _-")
			.tr(" -","_")

		if casing == "low"
			projectName.downcase!
		end

		if casing == "up"
			projectName.upcase!
		end

		return projectName
	end

	def to_flat(projectName)
		projectName.delete("^a-zA-Z0-9")
	end

	def copy_tpl(srcFile, destFile, replacements = nil)
		destFile = "./output/#{destFile}"
		destDir = File.dirname(destFile)
		FileUtils.mkdir_p(destDir)
		templateContent = File.read("./template/#{srcFile}")
		template = ERB.new(templateContent, trim_mode:"<>")
		if replacements
			content = template.result_with_hash(replacements)
		else
			content = template.result
		end
		File.write(destFile, content)
	end
end