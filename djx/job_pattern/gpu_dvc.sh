#!/bin/bash
#
#SBATCH --workdir=.
#SBATCH --cores=1
#SBATCH --output={log_file}
#SBATCH --job-name={job_id}
#SBATCH --gres=gpu

module load python/3.7

source .venv/bin/activate

dvc run -f {dvc_file} -d {python_file} -d {job_file} \
    -o {out_path} \
    python {python_file} {job_file} {out_path}