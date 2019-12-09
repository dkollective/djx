import datetime
import logging
import os
from djx.utils import load_yaml, get_commit, get_repro, save_yaml
# from djx.backend import psql as backend
from djx.grid import parse_grid
from toolz import get_in
import uuid
import subprocess

log = logging.getLogger(__name__)


JOB_FOLDER = os.environ['DJX_JOB_FOLDER']
LOG_FOLDER = os.environ['LOG_FOLDER']



cpu_job_file = """
#PBS -N {job_id}
#PBS -l walltime=10:0:0
#PBS -l mem=10gb
#PBS -j oe
#PBS -o {o}
#PBS -m n
#PBS -d .

module load python/3.7

source ~/.env

source .venv/bin/activate

"""



gpu_job_file = """
#!/bin/bash
#
#SBATCH --workdir=.
#SBATCH --cores=2
#SBATCH --output={logpath}
#SBATCH --job-name={job_id}
#SBATCH --gres=gpu

module load python/3.7

source ~/.env

source .venv/bin/activate

"""



def get_uuid():
    return str(uuid.uuid4())

def queue_job(job):
    job_id = job['job_id']
    jobpath = os.path.join(JOB_FOLDER, job_id + '.yml')
    logpath = os.path.join(LOG_FOLDER, job_id + '.log')

    save_yaml(job, jobpath)

    command = job['command']


    if job['machine'] == 'cpu':
        with open('./job.pbs', 'w') as f:
            f.write((cpu_job_file + command).format(job_id=job_id, o=logpath, jobpath=jobpath))
        command = 'qsub ./job.pbs'
    elif job['machine'] == 'gpu':
        with open('./job.sh', 'w') as f:
            f.write((gpu_job_file + command).format(job_id=job_id, o=logpath, jobpath=jobpath))
        command = 'sbatch ./job.sh'
    elif job['machine'] == 'local':
        command = command.format(jobpath=jobpath)

    subprocess.run(command, stdout=subprocess.PIPE, shell=True, check=True)


def deepscan(keys, current, base):
    if isinstance(current, dict):
        return {k: deepscan(keys + [k], v, base) for k, v in current.items()}
    elif isinstance(base, list):
        return [deepscan(keys + [i], v, base) for i, v in enumerate(current)]
    else:
        return parse_value(current, keys, base)


def parse_value(value, keys, base):
    if value == '__REPO_FROM_ENTRY':
        entry = get_in(keys[:-1] + ['entry'], base)
        return get_repro(entry)
    elif value == '__COMMIT_FROM_ENTRY':
        entry = get_in(keys[:-1] + ['entry'], base)
        return get_commit(entry)
    elif value == '__NOW':
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return value


def preprocess_exp(exp):
    exp = deepscan([], exp, exp)
    return exp


def add_exp(exp_file):
    exp = load_yaml(exp_file)
    # print(exp)
    exp = preprocess_exp(exp)
    # print(exp)
    if not exp['experiment']:
       jobs = [exp['job']]
    elif 'grid' in exp['experiment']:
        jobs = parse_grid(exp['experiment']['grid'], exp['job'])
    # print(jobs)

    exp_id = get_uuid()
    jobs = [{**t, **exp['meta'], 'exp_id': exp_id, 'job_id': get_uuid()} for t in jobs]

    for j in jobs:
        queue_job(j)
    # exp_id = backend.insert_exp(exp)
    # data_local, data_stored = get_all_data(exp['data'])
    # job = {**exp['job'], 'data': exp['data'], 'data_stored': data_stored}
    # if not exp['experiment']:
    #     jobs = [job]
    # elif 'grid' in exp['experiment']:
    #     jobs = parse_grid(exp['experiment']['grid'], job)
    # else:
    #     raise NotImplementedError('Currently only grid exp implemented.')
    # jobs = [{**t, 'exp_id': exp_id} for t in jobs]
    # backend.insert_jobs(jobs)
    # log.info(f'Added exp {exp_id}')
    # return exp_id
