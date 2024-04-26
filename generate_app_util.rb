require 'fileutils'
require 'erb'

module AppGenUtils

	def build_default_prefix(projectName)
		projectName.split(/([A-Z\-_ ][a-z0-9]*)/)
			.select {|x| x != "" && x != "-" && x != "_" && x != " "}
			.map {|x| x[0]}
			.join
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