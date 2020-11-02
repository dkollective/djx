#!/bin/bash
#
#SBATCH --workdir=.
#SBATCH --cores=8
#SBATCH --output={log_file}
#SBATCH --job-name={job_id}
#!/bin/bash

module load python/3.7

source .venv/bin/activate

echo "Entered environment"

{command} {run_dir} {in_dir}
