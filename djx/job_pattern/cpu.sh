#!/bin/bash
#
#SBATCH --workdir=.
#SBATCH --cores={cores}
#SBATCH --time {hours}:0:0
#SBATCH --mem {memory}GB
#SBATCH --output={log_file}
#SBATCH --job-name={job_id}
#SBATCH --partition {partition}
#!/bin/bash

module load python/3.7

source .venv/bin/activate

echo "Entered environment"

{command} {run_dir} {in_dir}
