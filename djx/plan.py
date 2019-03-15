from djx.utils import load_yaml, get_commit, get_repro
from djx.backend import psql as backend
from djx.grid import parse_grid
from toolz import get_in
import datetime


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


def preprocess_plan(plan):
    return deepscan([], plan, plan)


def add_plan(plan_file):
    plan = load_yaml(plan_file)
    plan = preprocess_plan(plan)
    plan_id = backend.insert_plan(plan)
    if not plan['plan']:
        tasks = [plan['task']]
    elif 'grid' in plan['plan']:
        tasks = parse_grid(plan['plan']['grid'], plan['task'])
    else:
        raise NotImplementedError('Currently only grid plan implemented.')
    tasks = [{**t, 'plan_id': plan_id} for t in tasks]
    backend.insert_tasks(tasks)
    print(f'Added plan {plan_id}')
    return plan_id
