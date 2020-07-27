#!/bin/bash
#
#SBATCH --workdir=.
#SBATCH --cores=1
#SBATCH --output={log_file}
#SBATCH --job-name={job_id}

module load python/3.7

source .venv/bin/activate

echo "Entered environment"

python {python_file} {job_file} {out_path} 