# Jupyter-Summit deployment at University of Colorado Boulder Research Computing
---

Author: [Zebula Sampedro](https://github.com/zebulasampedro) &lt;sampedro@colorado.edu&gt;

## Summary

Abridged configuration of the Jupyter deployment at CU Research Computing, which runs JupyterHub on a single node, and spawns Notebook servers on the [RMACC Summit](https://www.colorado.edu/rc/resources/summit) cluster via the Slurm scheduler. To allow users to configure Notebook server scheduling parameters during spawn, we use [OptionsFormSpawner](https://github.com/ResearchComputing/jupyterhub-options-spawner) to wrap [SlurmSpawner](https://github.com/jupyterhub/batchspawner).

The Notebook servers are run in Singularity containers configured to use certain host services directly, like Slurm and SSSD. These containerized Notebook servers use the host Slurm to run multi-node IPyParallel clusters, with each IPEngine also running in a container.

## JupyterHub Config Files
The `jupyterhub-config/` directory contains the three configuration files used in our deployment.

### `jupyterhub_config.py`
The primary configuration file loaded by the `jupyterhub -f`. A rough outline of the configuration:
* Increases the spawner timeout to accommodate longer queue waits.
* Sets up the `OptionsFormSpawner` to wrap the `SlurmSpawner`.
* Sets the default location of the Notebook to the user's home directory.
* Makes sure the JupyterHub server is configured to be contacted by remote Notebook servers running on the compute cluster.

We are currently using JupyterHub's built-in SSL, but are moving towards Nginx for SSL and HTTP -> HTTPS redirection. The Hub uses our PAM stack for auth.

### `form_config.py`
Configuration for the `OptionsFormSpawner` form fields that allow for user-configuration of spawn options and Slurm scheduling parameters. The values specified in these fields will be applied to the corresponding traits of the wrapped child spawner, `SlurmSpawner`.

SlurmSpawner will expose any trait prefixed with `req_` to the Slurm command templates it uses. The variable is usable in the template with the prefix removed. The options form config leverages this to expand the number of queueing options available to the Sbatch script.

### `slurm_config.py`
Configuration for the `SlurmSpawner`, applied by the `OptionsFormSpawner.child_config` trait. There are two major components to this file: the Sbatch script that will start the Notebook server, and the Slurm command configuration that the spawner will use to control the notebook server's lifecycle.

## Singularity Notebook Servers
The `singularity-notebook-ipyparallel/` directory contains the files and configuration for the Jupyter Notebook containers, as well as the Ipyparallel profile.

### Jupyter Notebook Image
Singularity base image for Jupyter Notebook servers running on RC resources. Can be started either via JupyterHub or directly by the end-user in a tunneling setup.

The container is started with a number of non-standard bind mounts _(example below)_ to allow for direct access to host services like Slurm, SSSD, and PAM. The first section of the Singularity recipe `%post` block configures the container-internal dependencies for these mounted services.
```
singularity shell \
  --bind /var/lib/sss/pipes \
  --bind /home/slurm \
  --bind /var/run/munge \
  --bind /etc/slurm \
  --bind /curc/slurm \
  jupyter-notebook.img
```

### IPyParallel
The `singularity-notebook-ipyparallel/profile_example-shas/` directory contains the IPyParallel profile we preload into the notebook image as an example for our end-users. This profile uses the `SlurmEngineSetLauncher` to start ipengines using Slurm. The `$CONTAINER_PATH` environment variable set by the initial SlurmSpawner script ensures that the ipengines start in a new instance of the same image the notebook server is running on.

## Omissions
Our deployment also containerizes JupyterHub using Docker and Docker Compose to improve change management and automation capabilities. We omitted this bit of the config for brevity, and also because there exist other _(likely better and more generic)_ examples for this deployment strategy.

## Future Plans
* Add more dynamic form capabilities to OptionsFormSpawner.
* Make more Singularity stacks available to our end-users. High on the list are R and PySpark.
* Extend SlurmSpawner to provide more informative error messaging and status feedback to end-users.
* Place JupyterHub behind Nginx for SSL, redirection, and better outage messaging.
* Make JupyterLab available to end-users.
* Develop extensions for JupyterLab to allow for interactive creation of Sbatch job scripts, and job queue management.
* Research, evaluate, and document strategies for making Jupyter the central component in our science gateway efforts moving forward.
