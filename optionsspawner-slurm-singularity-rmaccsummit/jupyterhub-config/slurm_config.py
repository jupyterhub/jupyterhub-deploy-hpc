summit_script = """#!/bin/bash
#SBATCH --partition={partition}
#SBATCH --qos={qos}
#SBATCH --account={account}
#SBATCH --time={runtime}
#SBATCH --nodes={nodes}
#SBATCH --ntasks-per-node={ntasks}
#SBATCH --output={homedir}/.jupyterhub-slurmspawner.log
#SBATCH --open-mode=append
#SBATCH --job-name=spawner-jupyterhub
#SBATCH --workdir={homedir}
#SBATCH --export={keepvars}
#SBATCH --uid={username}

ml singularity/2.4.2

# jupyter-singleuser anticipates that environment will be dropped during sudo, however
# it is retained by batchspawner. The XDG_RUNTIME_DIR variable must be unset to force a
# fallback, otherwise a permissions error occurs when starting the notebook.
# https://github.com/jupyter/notebook/issues/1318

export SINGULARITYENV_JUPYTERHUB_API_TOKEN=$JUPYTERHUB_API_TOKEN
export SINGULARITYENV_XDG_RUNTIME_DIR=$HOME/.singularity-jupyter-run
export SINGULARITYENV_CONTAINER_PATH={image_path}
singularity run \
  --bind /var/lib/sss/pipes \
  --bind /home/slurm \
  --bind /var/run/munge \
  --bind /etc/slurm \
  --bind /curc/slurm \
  --bind /etc/pam.d \
  $SINGULARITYENV_CONTAINER_PATH {cmd}
"""

spawner_config = {
    'batch_script': summit_script,
    'batch_submit_cmd': """sudo -E -u {username} SLURM_CONF=/curc/slurm/{cluster}/etc/slurm.conf sbatch""",
    'batch_query_cmd': """sudo -E -u {username} SLURM_CONF=/curc/slurm/{cluster}/etc/slurm.conf squeue -h -j {job_id} -o "%T %B" """,
    'batch_cancel_cmd': """sudo -E -u {username} SLURM_CONF=/curc/slurm/{cluster}/etc/slurm.conf scancel {job_id}""",
}
