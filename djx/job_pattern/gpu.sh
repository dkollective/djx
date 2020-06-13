#!/bin/bash
#
#SBATCH --workdir=.
#SBATCH --cores=1
#SBATCH --output={log_path}
#SBATCH --job-name={job_id}
#SBATCH --gres=gpu

module load python/3.7

source ~/.env

source .venv/bin/activate

{command}