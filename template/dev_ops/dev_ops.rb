require "fileutils"
require "salad_prep"

module Provincial
	using SaladPrep::StringEx

	Resorcerer = SaladPrep::Resorcerer
	PackageManagers = SaladPrep::Enums::PackageManagers
	SetupLvls = SaladPrep::Enums::SetupLvls
	NODE_VERSION = "22.13.1"

	module SetupLvls

	end
	
	class <%=ucPrefix%>Egg < SaladPrep::Egg
	
		def app_lvl_definitions_script_path
			__FILE__
		end
		
	end


	class <%=ucPrefix%>Installion < SaladPrep::Installion

		def initialize(
			egg:,
<% if apiLang.key == API_CHOICE_KEYS::PYTHON %>
			monty:,
			w_spoon:
<% end %>
		)
			super(egg)
<% if apiLang.key == API_CHOICE_KEYS::PYTHON %>
			@monty = monty
			@w_spoon = w_spoon
<% end %>
		end

		def install_dependencies
			self.class.curl
<% if apiLang.key == API_CHOICE_KEYS::PYTHON %>
			self.class.python_full(@egg, @monty)
<% end %>
<% if feLang.key == CLIENT_CHOICE_KEYS::REACT_TYPESCRIPT %>
			self.class.nodejs(NODE_VERSION)
<% end %>
			self.class.mariadb(@egg.db_setup_key(prefer_keys_file: false))
			self.class.openssl
			self.class.ca_certificates
			self.class.nginx_and_setup(@egg, @w_spoon)
		end


		def install_local_dependencies
			super
<% if feLang.key == CLIENT_CHOICE_KEYS::REACT_TYPESCRIPT %>
			self.class.nodejs(NODE_VERSION)
<% end %>
		end

		
	end



	class <%=ucPrefix%>DbAss < <%=db_class_map[dbChoice.key] %>

<% if apiLang.key == API_CHOICE_KEYS::PYTHON %>
		def initialize(egg, monty)
			super(egg)
			@monty = monty
		end
<% end %>

		def backup_db(backup_lvl: Enums::BackupLvl::ALL)
			super(backup_lvl:, has_bin: true)
		end


		def setup_db
			raise "setup_db"
		end


		def teardown_db(force: false)
			raise "setteardown_dbup_db"
		end


		def backup_tables_list
			[]
		end

	end



	Resorcerer.class_eval do
		def self.nginx_template
			conf = <<~CONF
				server {
					listen [::]:80;
					server_name <SERVER_NAME>;

					return 301 https://$host$request_uri;
				}

				server {
					listen <listen>;
					#should be the public key
					ssl_certificate <ssl_public_key>;
					#should be the private key
					ssl_certificate_key <ssl_private_key>;
					#should be the intermediate key if relevant
					#apparently this isn't needed anymore with porkbun?
					#ssl_trusted_certificate <ssl_intermediate>;
					proxy_set_header X-Real-IP $remote_addr;

					location /api/<API_VERSION>/ {
						proxy_pass http://127.0.0.1:<API_PORT>/;
					}

					location /docs {
						proxy_pass http://127.0.0.1:<API_PORT>/docs;
					}

					location /openapi.json {
						proxy_pass http://127.0.0.1:<API_PORT>;
					}

					location / {
						root <CLIENT_DEST>;
						try_files $uri /index.html =404;
					}
					server_name <SERVER_NAME>;
				}
			CONF
		end
	end
	
	@egg = <%=ucPrefix%>Egg.new(
		project_name_0: "<%=projectName%>",
		local_repo_path: ENV["<%=ucPrefix%>_LOCAL_REPO_DIR"],
		repo_url: ENV["<%=ucPrefix%>_REPO_URL"],
		env_prefix: "<%=ucPrefix%>",
		url_base: "<%=projectNameFlat%>",
		tld: nil,
		db_owner_name: "<%=lcPrefix%>_owner"
	)
	@box_box = <%=ucPrefix%>BoxBox.new(@egg)

<% if apiLang.key == API_CHOICE_KEYS::PYTHON %>
	generated_file_dir = File.join(@egg.lib_src, "dtos_and_utilities")
	
	
	@monty = SaladPrep::Monty.new(
		@egg, 
		generated_file_dir: generated_file_dir
	)
	@dbass = <%=ucPrefix%>DbAss.new(@egg, @monty)
<% else %>
	@dbass = <%=ucPrefix%>DbAss.new(@egg)
<% end %>
	@browser_trust_introducer = SaladPrep::FirefoxTrustIntroducer.new
	@cert_retriever = SaladPrep::PorkbunCertRetriever.new(@egg)
	@spoon_handle = SaladPrep::WSpoon.spoon_handle(@egg)
	@local_spoon = SaladPrep::LocalSpoon.new(
		@egg,
		@browser_trust_introducer,
		@spoon_handle
	)
	@remote_spoon = SaladPrep::RemoteSpoon.new(
		@egg,
		@spoon_handle,
		@cert_retriever
	)
	@where_spoon = @egg.is_local? ? @local_spoon : @remote_spoon
	@spoon_phone = SaladPrep::NginxPhone.new(
		@egg,
		SaladPrep::Resorcerer,
		@where_spoon
	)
	@w_spoon = SaladPrep::WSpoon.new(@egg, @where_spoon, @spoon_phone)
	@remote = <%=ucPrefix%>Remote.new(@egg)
	@client_launcher = SaladPrep::NodeClientLauncher.new(
		@egg, 
		node_version: NODE_VERSION
	)

<% if apiLang.key == API_CHOICE_KEYS::PYTHON %>
	@api_launcher = SaladPrep::PyAPILauncher.new(
		egg: @egg,
		dbass: @dbass,
		w_spoon: @w_spoon,
		monty: @monty
	)
<% elsif apiLang.key == API_CHOICE_KEYS::JAVA %>
	@api_launcher = SaladPrep::JavaApiLauncher.new(
		egg: @egg,
		dbass: @dbass,
		w_spoon: @w_spoon
	)
<% elsif apiLang.key == API_CHOICE_KEYS::NONE %>
	@api_launcher = SaladPrep::StaticAPILauncher.new(
		egg: @egg,
		dbass: @dbass,
		w_spoon: @w_spoon,
		client_launcher: @client_launcher
	)
<% end %>

	@installer = <%=ucPrefix%>Installion.new(
		egg: @egg,
<% if apiLang.key == API_CHOICE_KEYS::PYTHON %>
		monty: @monty,
		w_spoon: @w_spoon
<% end %>
	)
	@binstallion = <%=ucPrefix%>Binstallion.new(
		@egg,
		File.join(
			@egg.repo_path,
			"dev_ops"
		)
	)
<% if apiLang.key == API_CHOICE_KEYS::PYTHON %>
	@test_honcho = SaladPrep::PyTestHoncho.new(
		egg: @egg,
		dbass: @dbass,
		box_box: @box_box,
		monty: @monty
	)
<% else %>
	@test_honcho = SaladPrep::TestHoncho.new(
			egg: @egg,
			dbass: @dbass,
			box_box: @box_box
		)
<% end %>


	def self.egg
		@egg
	end


	def self.box_box
		@box_box
	end


	def self.dbass
		@dbass
	end


	def self.w_spoon
		@w_spoon
	end
	
	def self.libby
		@monty
	end

<% if apiLang.key == API_CHOICE_KEYS::PYTHON %>
	def self.monty
		@monty
	end
<% end %>

	def self.remote
		@remote
	end


	def self.api_launcher
		@api_launcher
	end


	def self.client_launcher
		@client_launcher
	end


	def self.installion
		@installer
	end


	def self.binstallion
		@binstallion
	end


	def self.test_honcho
		@test_honcho
	end


	def self.w_spoon
		@w_spoon
	end


	def self.local_spoon
		@local_spoon
	end

	Canary = SaladPrep::Canary
	BoxBox = SaladPrep::BoxBox
	Toob = SaladPrep::Toob


end
