Jupyterhub-Comet deployment at San Diego Supercomputer Center
=============================================================

Author: [Andrea Zonca](http://twitter.com/andreazonca)

## Summary

Jupyterhub deployment on a single machine that authenticates users with [XSEDE](http://xsede.org) accounts
and launches Jupyter Notebooks on computing nodes of the Comet Supercomputer going through the SLURM
scheduler.

## Files

* `jupyterhub.sh`: bash script to launch the Jupyterhub service, to be run as `root`
* `jupyterhub.conf`: configuration file for `supervisord`, copy to `/etc/supervisor/conf.d` and start/stop Jupyterhub with `supervisorctl`
* `comet_spawner.py`: subclass of `SlurmSpawner` from `batchspawner`, see <https://github.com/jupyterhub/batchspawner/>, sets up a form for the users to configure the SLURM job properties
* `xsede_oauthenticator.py`:  subclass of `CILogonOAuthenticator` from `oauthenticator`, see <https://github.com/jupyterhub/oauthenticator/>, configures authentication via XSEDE credentials and gets a certificate to be used by the spawner to launche the SLURM job.

See the docstrings and comments in the files for more details

I have some undefined variables in the files that start with `CONF_` for sensible configuration details I removed.
