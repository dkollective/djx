import datetime
import logging
from djx.utils import load_yaml, get_commit, get_repro
# from djx.backend import psql as backend
from djx.grid import parse_grid
from djx.data import get_all_data
from toolz import get_in

log = logging.getLogger(__name__)


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
    exp = preprocess_exp(exp)
    print(exp)
    
    
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
