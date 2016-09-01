#!/bin/bash

export CILOGON_CLIENT_ID="myproxy:oa4mp,2012:/client/CONF_CLIENTID"
export CILOGON_RSA_KEY_PATH="/srv/oauth-privkey.pem"
export CILOGON_CSR_PATH="/srv/oauth-cert.csr"
export OAUTH_CALLBACK_URL="https://CONF_JUPYTERHUBHOSTNAME/oauth_callback"

export PATH=/srv/anaconda/bin:$PATH

exec jupyterhub -f jupyterhub_config.py
