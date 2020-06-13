#PBS -N {job_id}
#PBS -l walltime=4:0:0
#PBS -l mem=2gb
#PBS -j oe
#PBS -o {log_path}
#PBS -m n
#PBS -d .

module load python/3.7

source ~/.env

source .venv/bin/activate

{command}