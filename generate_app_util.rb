require 'fileutils'
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
		if replacements
			replacements.each do |key, value|
				templateContent.gsub!("<%= #{key} %>", value)
		end
		File.write(destFile, templateContent)
	end
end