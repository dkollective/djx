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


def assert_same_length(grid_dim):
    list_len = [len(l) for l in _list]
    assert min(list_len) == max(list_len), 'Different lengths in same dim.'


def parse_simple(tasks, **grid_dim):
    _tasks = []
    keys, values = list(grid_dim.items())[0]
    for task in tasks:
        for v in values:
            _task = assoc_in(task, ['labels', keys], v)
            _task = assoc_in(task, keys.split('.'), v)
            _tasks.append(_task)
    return tasks


def get_dim_length(merge, replace, labels):
    lists = [list(merge.values()) + list(replace.values()) + labels]
    lens = [len(l) for l in lists]
    assert min(list_len) == max(list_len), 'Different lengths in same dim.'
    return min(list_len)


def parse_advanced(tasks, *, labels, name, merge={}, replace={}):
    _tasks = []
    for task in tasks:
        dim_length = get_dim_length(merge, replace, labels)
        for i in range(dim_length):
            _task = assoc_in(task, ['labels', name], labels[i])
            for keys, values in merge.items():
                k_list = keys.split('.')
                old_v = get_in(keys, task)
                new_v = deepmerge(values[i], old_v)
                _task = assoc_in(task, keys, new_v)
            for keys, values in replace.items():
                _task = assoc_in(task, keys.split('.'), values[i])
            _tasks.append(_task)
    return _tasks


def parse_dim(tasks, grid_dim):
    if len(grid_dim) == 1:
        return parse_simple(tasks, **grid_dim)
    else:
        return parse_advanced(tasks, **grid_dim)


def parse_grid(grid, base_task):
    tasks = [[{'labels': {}, **base_task}]]
    for grid_dim in grid:
        tasks = parse_dim(tasks, grid_dim)
    return tasks

