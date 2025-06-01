require 'fileutils'
require 'erb'

module AppGenUtils

	LOW = :low
	UP = :up


	def build_default_prefix(projectName)
		projectName.split(/([A-Z\-_ ][a-z0-9]*)/)
			.map {|x| x.strip.delete("^a-zA-Z0-9")[0]}
			.join
			.upcase
			
	end

	def to_snake(projectName, casing = nil)
		casing = casing ? casing.to_sym() : nil

		project_name = projectName.split(
				/
					(?<=[A-Z])(?=[A-Z][a-z])
					|(?<=[^A-Z])(?=[A-Z])
					|(?<=[A-Za-z])(?=[^A-Za-z])
				/x
			)
			.map(&:strip)
			.join("_")
			.delete("^a-zA-Z0-9 _-")
			.tr(" -","_")

		if casing == LOW
			project_name.downcase!
		end

		if casing == UP
			project_name.upcase!
		end

		return project_name
	end

	def to_flat(projectName)
		projectName.delete("^a-zA-Z0-9_\-").downcase
	end

	def copy_tpl(srcFile, destFile, replacements = nil)
		destFile = "./output/#{destFile}"
		destDir = File.dirname(destFile)
		FileUtils.mkdir_p(destDir)
		templateContent = File.read("./template/#{srcFile}")
		template = ERB.new(templateContent, trim_mode:"<>")
		if replacements
			content = template.result(replacements)
		else
			content = template.result
		end
		File.write(destFile, content)
	end

	def copy_raw(srcFile, destFile)
		destFile = "./output/#{destFile}"
		destDir = File.dirname(destFile)
		FileUtils.mkdir_p(destDir)

		FileUtils.cp(srcFile, destFile)
	end

end