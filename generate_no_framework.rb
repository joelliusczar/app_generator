require_relative "generate_app_util"

include AppGenUtils

module AppGenNoFramework
	def self.generate(choices)
		fromClient = "no_framework/client"

		copy_tpl(
			"src/#{fromClient}/index.html",
			"src/client/index.html"
		)
	end
end