from toolz import get_in, assoc_in


def deepmerge(base, new):
    if isinstance(base, dict) and isinstance(new, dict):
        return {**base, **new}
    elif isinstance(base, list) and isinstance(new, list):
        if len(base) == len(new):
            return [deepmerge(b, n) for b, n in zip(base, new)]
        else:
            ValueError('Length of list in deepmerge do not match.')
    else:
        return new


def parse_simple(tasks, grid_dim):
    _tasks = []
    dim_length = get_dim_length(grid_dim.values())
    for task in tasks:
        for v_id in range(dim_length):
            _task = task
            for keys, values in grid_dim.items():
                split_keys = keys.split('.')
                value = values[v_id]
                _task = assoc_in(_task, split_keys, value)
            if len(grid_dim.values()) == 1:
                _task = assoc_in(_task, ['labels', split_keys[-1]], value)
            _tasks.append(_task)
    return _tasks


def get_dim_length(ll):
    lens = [len(l) for l in ll]
    assert min(lens) == max(lens), 'Different lengths in same dimension.'
    return min(lens)


def parse_list(tasks, grid_dim):
    _tasks = []
    for task in tasks:
        for grid_val in grid_dim:
            _task = task
            for keys, value in grid_val.items():
                k_list = keys.split('.')
                old_v = get_in(k_list, task)
                new_v = deepmerge(old_v, value)
                _task = assoc_in(_task, k_list, new_v)
            _tasks.append(_task)
    return _tasks


def parse_dim(tasks, grid_dim):
    if isinstance(grid_dim, dict):
        return parse_simple(tasks, grid_dim)
    elif isinstance(grid_dim, list):
        return parse_list(tasks, grid_dim)
    else:
        raise ValueError("Unkown grid type.")


def parse_grid(grid, base_task):
    dummy = {'labels': {}, 'parameter': {}, 'data': {}, 'data_stored': {}}
    tasks = [{**dummy, **base_task}]
    for grid_dim in grid:
        tasks = parse_dim(tasks, grid_dim)
    return tasks
