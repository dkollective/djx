from djx.backend import psql as backend
from djx.utils import get_method, get_worker_info
from djx.store import get_all_data, store_data
from djx.log import setup_logging

import djx.example.src.iris

import structlog

logger = structlog.get_logger()


def get_func_from_source(entry, source_type, **kwargs):
    if source_type == 'PYTHON_MODULE':
        return get_method(entry)
    else:
        raise NotImplementedError(f'Source type {source_type} not implemented.')


def run_task(*, plan_id, task_id, source, project, data, parameter, labels, worker):
    log = logger.bind(
        task_id=task_id,
        labels=labels,
        project=project,
        worker=worker)
    log.info('get data')
    data_local, data_stored = get_all_data(data)

    func = get_func_from_source(**source)

    log.info('run task')
    output_files, output_records = func(data_local, **parameter)

    log.info('store data')
    output_files = store_data(output_files)
    return {
        'task_id': task_id,
        'output_files': output_files,
        'output_records': output_records,
        'data_stored': data_stored,
        'status': 'FINISHED'
    }


def run_next(plan_id):
    worker = get_worker_info()
    setup_logging()
    log = logger.new(
        plan_id=plan_id,
        worker=worker)
    task = backend.get_next_task(plan_id, worker)
    if not task:
        log.info(f'No unassigned task found for plan {plan_id}.')
        return
    else:
        try:
            result = run_task(**task)
            backend.update_task(result)
        except BaseException as e:
            result = {
                'task_id': task['task_id'],
                'output_files': None,
                'output_records': None,
                'data_stored': None,
                'status': 'FAILED'
            }
            backend.update_task(result)
            raise e
