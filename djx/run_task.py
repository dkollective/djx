from djx.utils import get_method


def run_task(task):
    entry = task['_entry']
    func = get_method(entry)
    res = func(**task['params'])
    return {**task, 'result': res}