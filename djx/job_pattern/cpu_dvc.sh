#PBS -N {job_id}
#PBS -l walltime=4:0:0
#PBS -l mem=2gb
#PBS -j oe
#PBS -o {log_file}
#PBS -m n
#PBS -d .

module load python/3.7

source .venv/bin/activate

echo "Entered environment"

cd {run_dir} 

dvc run  -d ../../../{python_file} -d {job_file} -n foo -o {out_path} \
    python ../../../{python_file} {job_file} {out_path}