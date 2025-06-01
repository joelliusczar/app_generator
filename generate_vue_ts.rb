require 'fileutils'
require_relative "generate_app_util"

include AppGenUtils

module AppGenVueTs
	def self.generate(choices)
		clientSrc = "src/vue_ts/client"
		clientDest = "src/client"


		copy_tpl(
			"#{clientSrc}/eslintrc.cjs",
			"#{clientDest}/.eslintrc.cjs"
		)

		copy_tpl(
			"#{clientSrc}/env.d.ts",
			"#{clientDest}/env.d.ts"
		)

		copy_tpl(
			"#{clientSrc}/index.html",
			"#{clientDest}/index.html"
		)

		copy_tpl(
			"#{clientSrc}/package.json",
			"#{clientDest}/package.json"
		)

		copy_tpl(
			"#{clientSrc}/prettierrc.json",
			"#{clientDest}/.prettierrc.json"
		)

		copy_tpl(
			"#{clientSrc}/tsconfig.app.json",
			"#{clientDest}/tsconfig.app.json"
		)

		copy_tpl(
			"#{clientSrc}/tsconfig.json",
			"#{clientDest}/tsconfig.json"
		)

		copy_tpl(
			"#{clientSrc}/tsconfig.node.json",
			"#{clientDest}/tsconfig.node.json"
		)

		copy_tpl(
			"#{clientSrc}/vite.config.ts",
			"#{clientDest}/vite.config.ts"
		)

		viteSrc = "#{clientSrc}/vite/deps"
		viteDest = "#{clientDest}/.vite/deps"

		copy_tpl(
			"#{viteSrc}/_metadata.json",
			"#{viteDest}/_metadata.json"
		)

		copy_tpl(
			"#{viteSrc}/package.json",
			"#{viteDest}/package.json"
		)

		copy_tpl(
			"#{viteSrc}/vue.js",
			"#{viteDest}/vue.js"
		)

		copy_tpl(
			"#{viteSrc}/vue.js.map",
			"#{viteDest}/vue.js.map"
		)

		vscodeSrc = "#{clientSrc}/vscode"
		vscodeDest = "#{clientDest}/.vscode"

		copy_tpl(
			"#{vscodeSrc}/extension.json",
			"#{vscodeDest}/extension.json"
		)

		copy_tpl(
			"#{vscodeSrc}/settings.json",
			"#{vscodeDest}/settings.json"
		)

		copy_raw(
			"#{clientSrc}/public/favicon.ico",
			"#{clientDest}/public/favicon.ico"
		)

		codeSrc = "#{clientSrc}/src"
		codeDest = "#{clientDest}/src"

		copy_tpl(
			"#{codeSrc}/App.vue",
			"#{codeDest}/App.vue"
		)

		copy_tpl(
			"#{codeSrc}/main.ts",
			"#{codeDest}/main.ts"
		)

		apiCallsSrc = "#{codeSrc}/api_calls"
		apiCallsDest = "#{codeDest}/api_calls"

		copy_tpl(
			"#{vscodeSrc}/lookups.ts",
			"#{vscodeDest}/lookups.ts"
		)

		assetsSrc = "#{codeSrc}/assets"
		assetsDest = "#{codeDest}/assets"

		copy_tpl(
			"#{vscodeSrc}/main.css",
			"#{vscodeDest}/main.css"
		)

		FileUtils.mkdir_p("#{codeDest}/components")

		composablesSrc = "#{codeSrc}/composables"
		composablesDest = "#{codeDest}/composables"

		copy_tpl(
			"#{composablesSrc}/useFormSubmit.ts",
			"#{composablesDest}/useFormSubmit.ts"
		)

		copy_tpl(
			"#{composablesSrc}/useLookups.ts",
			"#{composablesDest}/useLookups.ts"
		)

		helpersSrc = "#{codeSrc}/helpers"
		helpersDest = "#{codeDest}/helpers"

		copy_tpl(
			"#{helpersSrc}/errors.ts",
			"#{helpersDest}/errors.ts"
		)

		copy_tpl(
			"#{helpersSrc}/numbers.ts",
			"#{helpersDest}/numbers.ts"
		)

		typesSrc = "#{codeSrc}/types"
		typesDest = "#{codeDest}/types"

		copy_tpl(
			"#{typesSrc}/generics.ts",
			"#{typesDest}/generics.ts"
		)

		copy_tpl(
			"#{typesSrc}/lookups.ts",
			"#{typesDest}/lookups.ts"
		)

		copy_tpl(
			"#{typesSrc}/requests.ts",
			"#{typesDest}/requests.ts"
		)


	end
end