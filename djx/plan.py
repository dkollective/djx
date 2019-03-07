from djx.utils import get_git_info, load_yaml
from backend import psql as backend
from grid import parse_grid


def preprocess_plan(plan):
    if plan['source'] == 'FROM_CURRENT_ENTRY':
        repository, commit = get_git_info(plan['entry'])
        plan = {**plan, 'source': {'repository': repository, 'commit': commit}}
    return plan


def add_plan(plan_file):
    plan = load_yaml(plan_file)
    plan = preprocess_plan(plan)
    plan_id = backend.insert_plan(plan)
    if 'grid' in plan:
        tasks = parse_grid(plan['task'], plan['grid'])
    else:
        tasks = [plan['task']]
    tasks = [{'task': t, 'plain_id': plan_id} for t in tasks]
    backend.insert_tasks(tasks)
    print(f'Added plan {plan_id}')
    return plan_id
