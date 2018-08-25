import os
import importlib.machinery

slurm_config = importlib.machinery.SourceFileLoader('slurm_config','/opt/jupyterhub/config/slurm_config.py').load_module()
form_config = importlib.machinery.SourceFileLoader('form_config','/opt/jupyterhub/config/form_config.py').load_module()



# SPAWNER CONFIGURATION

# Increase spawner timeout to be tolerant of longer queue wait times.
c.Spawner.http_timeout = 300
c.Spawner.start_timeout = 300

# https://github.com/jupyterhub/jupyterhub/issues/929
c.Spawner.notebook_dir = '/'
c.Spawner.default_url = '/tree/home/{username}'

# OptionsSpawner: Attach options forms to any JupyterHub spawner using only configuration.
# https://github.com/ResearchComputing/jupyterhub-options-spawner
c.JupyterHub.spawner_class = 'optionsspawner.OptionsFormSpawner'

# The OptionsSpawner wraps SlurmSpawner from https://github.com/jupyterhub/batchspawner
c.OptionsFormSpawner.child_class = 'batchspawner.SlurmSpawner'
c.OptionsFormSpawner.child_config = slurm_config.spawner_config
c.OptionsFormSpawner.form_fields = form_config.form_fields

# HUB CONFIGURATION

# Set the log level by value or name.
c.JupyterHub.log_level = 'DEBUG'
c.JupyterHub.extra_log_file = '/var/log/jupyterhub/debug-log.log'

# Allow servers to persist between restarts of the hub itself
c.JupyterHub.cleanup_servers = False

# We're doing SSL through the Hub's built-in capabilities, so host on 443
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 443

# Make sure that the remote notebook servers can contact the hub
jupyterhub_hostname = os.environ.get('HOSTNAME')
c.JupyterHub.hub_ip = jupyterhub_hostname

c.JupyterHub.cookie_secret_file = '/opt/jupyterhub/jupyterhub_cookie_secret'

c.JupyterHub.db_url = '/opt/jupyterhub/jupyterhub.sqlite'

# SSL Config
c.JupyterHub.ssl_cert = os.environ.get('JUPYTERHUB_CERT_PATH')
c.JupyterHub.ssl_key = os.environ.get('JUPYTERHUB_KEY_PATH')

# Configure the admin interface
admins_env = os.environ.get('JUPYTERHUB_ADMINS', '')
admins = tuple(admins_env.split()) if admins_env else ()
c.Authenticator.admin_users = admins
c.JupyterHub.admin_access = True
