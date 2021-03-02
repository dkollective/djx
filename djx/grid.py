from toolz import get_in, assoc_in
from djx.merge import deepmerge


def parse_simple(jobs, grid_dim):
    _jobs = []
    dim_length = get_dim_length(grid_dim.values())
    for job in jobs:
        for v_id in range(dim_length):
            _job = job
            for keys, values in grid_dim.items():
                split_keys = keys.split('.')
                value = values[v_id]
                _job = assoc_in(_job, split_keys, value)
            if len(grid_dim.values()) == 1:
                _job = assoc_in(_job, ['labels', split_keys[-1]], value)
            _jobs.append(_job)
    return _jobs


def get_dim_length(ll):
    lens = [len(l) for l in ll]
    assert min(lens) == max(lens), 'Different lengths in same dimension.'
    return min(lens)


def parse_list(jobs, grid_dim):
    _jobs = []
    for job in jobs:
        for grid_val in grid_dim:
            _job = job
            for keys, value in grid_val.items():
                k_list = keys.split('.')
                old_v = get_in(k_list, job)
                new_v = deepmerge(old_v, value)
                _job = assoc_in(_job, k_list, new_v)
            _jobs.append(_job)
    return _jobs


def parse_dim(jobs, grid_dim):
    if isinstance(grid_dim, dict):
        return parse_simple(jobs, grid_dim)
    elif isinstance(grid_dim, list):
        return parse_list(jobs, grid_dim)
    else:
        raise ValueError("Unkown grid type.")


def parse_grid(grid, base_job):
    dummy = {'labels': {}, 'params': {}}
    jobs = [{**dummy, **base_job}]
    for grid_dim in grid:
        jobs = parse_dim(jobs, grid_dim)
    return jobs
