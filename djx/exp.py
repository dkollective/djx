from time import sleep
import logging
import os
from djx.utils import load_yaml, save_yaml
from djx.grid import parse_grid
from djx.merge import deepermerge
from toolz import keyfilter
import uuid
import subprocess


log = logging.getLogger(__name__)


def pick(whitelist, d):
    return keyfilter(lambda k: k in whitelist, d)


def omit(blacklist, d):
    return keyfilter(lambda k: k not in blacklist, d)


def get_uuid():
    return str(uuid.uuid4())


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def write_file(string, filename):
    with open(filename, 'w') as f:
        f.write(string)


def create_script(script_name, command, **kwargs):
    script_file = os.path.join(os.path.dirname(__file__), f'job_pattern/{script_name}.sh')
    script_str = read_file(script_file)
    command = command.format(**kwargs)
    kwargs = {'in_dir': '', **kwargs, 'command': command}
    script_str = script_str.format(**kwargs)
    return script_str


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


starter = {
    'cpu': 'sbatch {}',
    'gpu': 'sbatch {}',
    'local': 'bash {}',
    'local_parallel': 'bash {}',
    'test': 'bash {}',
}


def queue_job(job, exp_dir):
    job_id = job['job_id']
    run_dir = f'{exp_dir}/{job_id}'
    job_file = f'{run_dir}/job.yml'
    script_file = f'{run_dir}/run.sh'
    log_file = f'{run_dir}/log.log'
    output_path = f'{run_dir}'
    script_name = job['exec']['script_name']
    job_only = job['exec'].get('job_only', False)

    script_str = create_script(
        **job['exec'], job_id=job_id, job_file=job_file,
        log_file=log_file, output_path=output_path, run_dir=run_dir)

    if job.get('params_only'):
        job = job['params']

    if 'output_path' not in job:
        job['output_path'] = os.path.join(os.getcwd(), output_path)

    ensure_dir(run_dir)
    save_yaml(job, job_file)

    write_file(script_str, script_file)

    if not job_only:
        start_command = starter[script_name].format(script_file)
        print(start_command)
        sleep(1)
        subprocess.run(start_command, stdout=subprocess.PIPE, shell=True, check=True)


def add_job_ids(jobs):
    ids = set()
    for idx, job in enumerate(jobs):
        labels = job.get('labels', job['params'].get('labels', {}))
        job_id = "__".join(f"{k}_{v}" for k, v in labels.items())
        ids.add(job_id)
        yield {**job, 'job_id': job_id}


def get_subdirs(_dir):
    return [
        o
        for o in os.listdir(_dir)
        if os.path.isdir(os.path.join(_dir, o))
    ]


def parse_parent(base_job, strategy, folder_name, base_dir, parent_name):
    parent_folder = os.path.join(base_dir, folder_name)
    for job_name in get_subdirs(parent_folder):
        parent_job_folder = os.path.join(parent_folder, job_name)
        parent_job_file = os.path.join(parent_job_folder, f'{parent_name}.yml')
        parent_job = load_yaml(parent_job_file)
        labels = {**base_job.get('labels', {}), **parent_job.get('labels', {})}
        _exec = {'in_dir': parent_job_folder, **base_job['exec']}
        yield {**base_job, 'labels': labels, 'exec': _exec}


def include_files(exp):
    if 'include' in exp:
        include = exp.pop('include')
        for inc in include:
            new = load_yaml(inc)
            exp = deepermerge(exp, new)
    return exp


def add_exp(exp_file):
    exp = load_yaml(exp_file)
    exp = include_files(exp)
    exp_dir = os.path.splitext(exp_file)[0]

    if 'grid' in exp:
        base_job = omit(['grid'], exp)
        jobs = parse_grid(exp['grid'], base_job)
    elif 'parent' in exp:
        raise NotImplementedError('Currently not implemented')
        base_job = omit(['parent'], exp)
        jobs = parse_parent(base_job=base_job, base_dir=base_dir, **exp['parent'])
    else:
        jobs = [exp]

    exp_id = get_uuid()
    jobs = [{**t, 'exp_id': exp_id} for t in add_job_ids(jobs)]

    for j in jobs:
        queue_job(j, exp_dir)
