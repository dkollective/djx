import logging
from djx.backend import psql as backend
from djx.utils import get_method, get_worker_info

log = logging.getLogger()


__task = {}


def new_task(task):
    global __task
    __task = task


def get_task_id():
    return __task.get('task_id')


def get_labels():
    return __task.get('labels')


def get_data_path(name):
    return __task['data_stored'].get(name)


def get_func_from_source(entry, source_type, **kwargs):
    if source_type == 'PYTHON_MODULE':
        return get_method(entry)
    else:
        raise NotImplementedError(f'Source type {source_type} not implemented.')


def run_task(task):
    new_task(task)
    log.info('get data')
    func = get_func_from_source(**task['source'])
    log.info('run task')
    func(**task['parameter'])


def run_next(plan_id):
    worker = get_worker_info()
    task = backend.get_next_task(plan_id, worker)
    if not task:
        log.info(f'No unassigned task found for plan {plan_id}.')
        return
    else:
        task_id = task['task_id']
        try:
            run_task(task)
            backend.update_task_status(task_id, 'FINISHED')
        except BaseException as e:
            backend.update_task_status(task_id, 'FAILED')
            raise e
        return task_id
