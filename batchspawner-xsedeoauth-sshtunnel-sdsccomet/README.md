Jupyterhub-Comet deployment at San Diego Supercomputer Center
=============================================================

Author: [Andrea Zonca](http://twitter.com/andreazonca)

## Summary

Jupyterhub deployment on a single machine that authenticates users with [XSEDE](http://xsede.org) accounts
and launches Jupyter Notebooks on computing nodes of the Comet Supercomputer going through the SLURM
scheduler.

## Requirements

At SDSC we use a SDSC Cloud Ubuntu 14.04 Openstack virtual machine, but any distribution would be fine.
I recommend to use Anaconda, but another Python 3 installation would work (Jupyterhub requires Python 3), required packages:

* `jupyterhub`
* `oauthenticator`
* `batchspawner`

On the system you also need to install `gsissh` for logging into a XSEDE Supercomputer, there are packages from Globus online for Debian and Ubuntu.

It is convenient to install `supervisord` to handle automatically starting Jupyterhub at reboot and restart if anything goes wrong, but it is not necessary.

It would also be better to use NGINX to handle SSL and proxy Jupyterhub, but I wanted to keep the setup simple.

## Files

* `jupyterhub.sh`: bash script to launch the Jupyterhub service, to be run as `root`
* `jupyterhub.conf`: configuration file for `supervisord`, copy to `/etc/supervisor/conf.d` and start/stop Jupyterhub with `supervisorctl`
* `comet_spawner.py`: subclass of `SlurmSpawner` from `batchspawner`, see <https://github.com/jupyterhub/batchspawner/>, sets up a form for the users to configure the SLURM job properties
* `xsede_oauthenticator.py`:  subclass of `CILogonOAuthenticator` from `oauthenticator`, see <https://github.com/jupyterhub/oauthenticator/>, configures authentication via XSEDE credentials and gets a certificate to be used by the spawner to launche the SLURM job.

See the docstrings and comments in the files for more details

I have some undefined variables in the files that start with `CONF_` for sensible configuration details I removed.

## Network setup

A key configuration element for spawners launching remote Jupyter Notebooks is making the right ports available.

* `batchspawner` automatically takes care of communicating to the Jupyter Notebooks running remotely the IP address of the Jupyterhub server, I setup the Jupyterhub instance so that it accepts incoming connections from all Comet computing nodes.
* The Jupyter Notebooks also need to be able to communicate with Jupyterhub on port 8081, for this I setup a SSH tunnel, the easiest way is to create a `tunnelbot` user that has no shell access but can only setup tunnels. Then dump the private RSA key of this user into the SLURM job, this way once the job starts, we can create a local tunnel and make the 8081 port of Jupyterhub instance available locally to the Comet computing node.
