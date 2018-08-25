# Configuration file for ipcluster.

c.IPClusterEngines.engine_launcher_class = 'ipyparallel.apps.launcher.SlurmEngineSetLauncher'
c.SlurmLauncher.qos = 'normal'
c.SlurmLauncher.timelimit = '1:00:00'

c.SlurmEngineSetLauncher.batch_template = """#!/bin/bash
#SBATCH --partition shas
#SBATCH --qos {qos}
#SBATCH --job-name ipengine
#SBATCH --ntasks {n}
# This will run a single ipengine per CPU
#SBATCH --cpus-per-task 1
# Use ntasks-per-node=1 to run one ipengine per node
#SBATCH --time {timelimit}
#SBATCH --output {profile_dir}/log/slurm.out

ml gcc singularity/2.4.2
ml openmpi/2.0.1

# Run each IPEngine in a new instance of the current container.

export SINGULARITYENV_JUPYTERHUB_API_TOKEN=$JUPYTERHUB_API_TOKEN
export SINGULARITYENV_XDG_RUNTIME_DIR=$HOME/.singularity-jupyter-run
export SINGULARITYENV_CONTAINER_PATH=$CONTAINER_PATH
mpirun singularity run \
  --bind /var/lib/sss/pipes \
  --bind /home/slurm \
  --bind /var/run/munge \
  --bind /etc/slurm \
  --bind /etc/pam.d \
  $CONTAINER_PATH \
  ipengine --profile-dir="{profile_dir}" --cluster-id="{cluster_id}"
"""
