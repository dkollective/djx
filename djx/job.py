import logging
from djx.backend import psql as backend
from djx.utils import get_method, get_worker_info

log = logging.getLogger()


__job = {}


def new_job(job):
    global __job
    __job = job


def get_job_id():
    return __job.get('job_id')


def get_labels():
    return __job.get('labels')


def get_data_path(name):
    return __job['data_stored'].get(name)


def get_func_from_source(entry, source_type, **kwargs):
    if source_type == 'PYTHON_MODULE':
        return get_method(entry)
    else:
        raise NotImplementedError(f'Source type {source_type} not implemented.')


def run_job(job):
    new_job(job)
    log.info('get data')
    func = get_func_from_source(**job['source'])
    log.info('run job')
    func(**job['parameter'])


def run_next(exp_id):
    worker = get_worker_info()
    job = backend.get_next_job(exp_id, worker)
    if not job:
        log.info(f'No unassigned job found for exp {exp_id}.')
        return
    else:
        job_id = job['job_id']
        try:
            run_job(job)
            backend.update_job_status(job_id, 'FINISHED')
        except BaseException as e:
            backend.update_job_status(job_id, 'FAILED')
            raise e
        return job_id
