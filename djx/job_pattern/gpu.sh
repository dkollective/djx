#!/bin/bash -l
#
#SBATCH --workdir=.
#SBATCH --output={log_file}
#SBATCH --job-name={job_id}
#SBATCH --cpus-per-task {cores}
#SBATCH --mem {memory}GB
#SBATCH --gres=gpu
#SBATCH --partition gpu

set -e

module load python/3.9
module load cuda

source .venv/bin/activate

echo "Entered environment"

{command}
