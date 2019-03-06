from djx.utils import get_git_info
from uuid import uuid4
from itertools import product
from toolz.dicttoolz import assoc_in
from functools import partial


def merge(base, new):
    if isinstance(base, dict) and isinstance(new, dict):
        return {
            key: merge(base.get(key, {}), new.get(key, {}))
            for key in (base.keys() | new.keys())
        }
    elif isinstance(base, list) and isinstance(new, list):
        if len(base) == len(new):
            return [merge(b, n) for b, n in zip(base, new)]
        else:
            return new
    else:
        return new


def apply_deep(obj, fdict):
    if isinstance(obj, dict):
        applied = {kk: v for k in obj if k in fdict for kk, v in fdict[k](obj[k]).items()}
        filtered = {k: apply_deep(v, fdict) for k, v in obj.items() if k not in fdict}
        return {**applied, **filtered}
    elif isinstance(obj, list):
        return [apply_deep(item, fdict) for item in obj]
    else:
        return obj


def _file(file, base_path):
    return load_yaml(os.path.join(base_path, file))


def preparse(plan, plan_path):
    spezial_keys = {
        '_file': partial(_file, base_path=plan_path)
    }
    return apply_deep(obj, spezial_keys)


def reduce_stage(previous_stage=[], reduction=None, **kwargs):
    ptasks = [t['task_id'] for t in previous_stage]
    if reduction == 'each':
        tasks = [
            task
            for dependency in ptasks
            for task in parse_stage(dependencies=[dependency], **kwargs)
        ]
    elif reduction == 'reduce':
        tasks = parse_stage(dependencies=ptasks, **kwargs)
    else:
        tasks = parse_stage(**kwargs)
    return tasks


def parse_stage(grid=None, plan_id=None, job_id=None, stage=None, **base_task):
    if plan_id is not None:
        return get_task(plan_id=plan_id, stage=stage)
    elif job_id is not None:
        return get_task(job_id=job_id)
    elif grid is not None:
        return parse_grid(grid, priority=0, **base_task)
    else:
        return [base_task]


def parse_pipeline(pipeline, **info):
    pipeline = preparse(pipeline)
    stage_tasks = []
    tasks = []
    for stage in pipeline:
        stage_tasks = reduce_stage(stage_tasks, **stage)
        tasks += stage_tasks
    tasks = [{**t, **info} for t in tasks]
    return tasks


def flatten_single_path(obj):
    if isinstance(obj, dict):
        key, value = list(obj.items())[0]
        val, path = flatten_single_path(value)
        return val, [key] + path
    else:
        return obj, []


def parse_simple_grid(dim_name, dim_values):
    values, path = flatten_single_path(dim_values)
    return [{'params': assoc_in({}, path, val), 'tags': {dim_name: val}} for val in values]


def parse_deep_grid(dim_name, dim_values):
    return [
        {'params': list(val.values())[0], 'tags': {dim_name: list(val.keys())[0]}}
        for val in dim_values
    ]


def parse_grid(grid, **base_task):
    _grid = [[base_task]]
    for dimension in grid:
        kv = list(dimension.items())
        assert len(kv) == 1, f'Nested objects are not allowed here. ({kv})'
        dim_name, dim_values = kv[0]
        if isinstance(dim_values, list):
            expander = parse_deep_grid
        else:
            expander = parse_simple_grid
        _grid.append(expander(dim_name, dim_values))
    _tasks = list(product(*_grid))
    return _tasks


def enrich_task(task):
    project, commit = get_git_info(**task)
    task['project'] = project
    task['commit'] = commit
    task['task_id'] = uuid4().hex
    return task
