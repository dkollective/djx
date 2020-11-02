#!/bin/bash -l
#
#SBATCH --workdir=.
#SBATCH --cores=2
#SBATCH --output={log_file}
#SBATCH --job-name={job_id}
#SBATCH --gres=gpu
#SBATCH --partition gpu

set -e

module load python/3.7
module load cuda

source .venv/bin/activate

echo "Entered environment"

{command} {run_dir} {in_dir}
