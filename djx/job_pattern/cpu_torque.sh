#PBS -l nodes=1:ppn={cores}
#PBS -N {job_id}
#PBS -l walltime={hours}:0:0
#PBS -l mem={memory}gb
#PBS -j oe
#PBS -o {log_file}
#PBS -m n
#PBS -d .

module load python/3.7
module load cuda

source .venv/bin/activate

echo "Entered environment"

{command} {run_dir} {in_dir}
