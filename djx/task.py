import structlog
from backend import psql as backend
from djx.utils import get_method
from djx.store import get_all_data, store_data

logger = structlog.get_logger()


def run_task(*, plan_id, task_id, entry, project, task, labels):
    log = logger.new(
        plan_id=plan_id,
        task_id=task_id,
        labels=labels,
        project=project)
    log.info('get data')
    data = get_all_data(task['data'])
    func = get_method(entry)

    log.info('run task')
    output_files, output_records = func(data, **task['parameter'])

    log.info('store data')
    output_files = store_data(output_files)
    return {
        'task_id': task_id,
        'output_files': output_files,
        'output_records': output_records,
        'status': 'FINISHED'
    }


def run_next(plan_id):
    task = backend.get_next_task(plan_id)
    try:
        result = run_task(task)
        backend.update_task(result)
    except BaseException as e:
        result = {
            'task_id': task['task_id'],
            'output_files': None,
            'output_records': None
            'status': 'FAILED'
        }
        backend.update_task(result)
        raise e
