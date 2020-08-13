#PBS -N {job_id}
#PBS -l walltime=8:0:0
#PBS -l mem=4gb
#PBS -j oe
#PBS -o {log_file}
#PBS -m n
#PBS -d .

module load python/3.7

source .venv/bin/activate

echo "Entered environment"

{command} {run_dir}