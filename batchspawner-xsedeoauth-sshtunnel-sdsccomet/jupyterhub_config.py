# The public facing ip of the proxy
c.JupyterHub.ip = '0.0.0.0'
# The public facing port of the proxy
c.JupyterHub.port = 443
# The port for this process
c.JupyterHub.hub_port = 8081
# The ip for this process
c.JupyterHub.hub_ip = '0.0.0.0'
# Number of days for a login cookie to be valid. Default is two weeks.
c.JupyterHub.cookie_max_age_days = 8

import os
pjoin = os.path.join
cred = CONF_KEYSFOLDER
c.JupyterHub.ssl_key = pjoin(cred, 'privkey.pem')
c.JupyterHub.ssl_cert = pjoin(cred, 'fullchain.pem')

# append jupyterhub_config folder to path in order to load the authenticator
# and spawner classes
import sys
sys.path.append(os.path.dirname(__file__))

#### Authenticator ####

from xsede_oauthenticator import XSEDEOAuthenticator
c.JupyterHub.authenticator_class = XSEDEOAuthenticator
c.CILogonOAuthenticator.user_cert_dir = pjoin('/srv/jupyterhub/usercred')

#### Spawner ####

from comet_spawner import CometSpawner
c.JupyterHub.spawner_class = CometSpawner
c.SlurmSpawner.req_nprocs = '2'
c.SlurmSpawner.req_queue = 'compute'
c.SlurmSpawner.req_runtime = '12:00:00'
c.SlurmSpawner.req_memory = '4gb'
c.SlurmSpawner.req_host = 'comet.sdsc.edu'
c.SlurmSpawner.batch_script = '''#!/bin/bash
#SBATCH --job-name="jupyterhub"
#SBATCH --output="jupyterhub.%j.%N.out"
#SBATCH --partition={queue}
#SBATCH --nodes=1
###SBATCH --ntasks-per-node=24 # needs to be modified for shared queues
###SBATCH --export=ALL
#SBATCH --time={runtime}
#SBATCH --export={keepvars}
#SBATCH --get-user-env=L
{other}

export PATH=/oasis/projects/nsf/csb136/zonca/anaconda/bin:$PATH
#export PATH=/oasis/projects/nsf/csb136/zonca/anaconda/bin:/opt/gnu/gcc/bin:/opt/gnu/bin:/opt/mvapich2/intel/ib/bin:/opt/intel/composer_xe_2013_sp1.2.144/bin/intel64:/opt/intel/composer_xe_2013_sp1.2.144/mpirt/bin/intel64:/opt/intel/composer_xe_2013_sp1.2.144/debugger/gdb/intel64_mic/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/ibutils/bin:/usr/java/latest/bin:/opt/pdsh/bin:/opt/rocks/bin:/opt/rocks/sbin:/opt/sdsc/bin:/opt/sdsc/sbin;
export PYTHONPATH=;

# create tunnelbot private SSH key
TUNNELBOT_RSA_PATH=$(mktemp)
echo "-----BEGIN RSA PRIVATE KEY-----
CONF_TUNNELBOTRSAPRIVATEKEY
-----END RSA PRIVATE KEY-----" > $TUNNELBOT_RSA_PATH
chmod 600 $TUNNELBOT_RSA_PATH

# create tunnel from Comet to Jupyterhub
ssh -o "StrictHostKeyChecking no" -i $TUNNELBOT_RSA_PATH -N -f -L 8081:localhost:8081 tunnelbot@CONF_JUPYTERHUBHOSTNAME

{cmd}
'''
c.SlurmSpawner.batch_submit_cmd = 'env X509_USER_PROXY="/tmp/cert.{username}" gsissh {username}@{host} sbatch'
c.SlurmSpawner.batch_query_cmd = '''env X509_USER_PROXY="/tmp/cert.{username}" gsissh {username}@{host} 'squeue -h -j {job_id} -o "%T %B"' '''
c.SlurmSpawner.batch_cancel_cmd = '''env X509_USER_PROXY="/tmp/cert.{username}" gsissh {username}@{host} scancel {job_id}'''
c.SlurmSpawner.state_exechost_exp = r'\1.sdsc.edu'
c.SlurmSpawner.cmd = ["python", "/oasis/scratch/comet/zonca/temp_project/jupyterhub-singleuser"]
c.SlurmSpawner.start_timeout = 7200
c.SlurmSpawner.startup_poll_interval = 5.0
c.SlurmSpawner.http_timeout = 7200
