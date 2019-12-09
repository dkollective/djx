import os
import subprocess
from djx.utils import get_method, get_worker_info, load_yaml, ensure_directory
from pandas.io.json import json_normalize

import structlog
from structlog.threadlocal import (
    bind_threadlocal,
    clear_threadlocal,
    merge_threadlocal_context,
)
from structlog import configure


JOB_FOLDER = os.environ['DJX_JOB_FOLDER']
REC_FOLDER = os.environ['DJX_RECORDS_FOLDER']


def get_func_from_source(entry, source_type, **kwargs):
    if source_type == 'PYTHON_MODULE':
        return get_method(entry)
    else:
        raise NotImplementedError('Source type {source_type} not implemented.'.format(source_type=source_type))


def setup_logger(job):
    exp_id = job['exp_id']
    job_id = job['job_id']
    logdir = os.path.join(REC_FOLDER, exp_id)
    ensure_directory(logdir)
    logpath = os.path.join(logdir, job_id + '.log')

    configure(
        processors=[
            merge_threadlocal_context,
            structlog.processors.TimeStamper(),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.PrintLoggerFactory(open(logpath, 'w'))
    )

    clear_threadlocal()
    bind_threadlocal(**job['labels'], job_id=job['job_id'], exp_id=job['exp_id'], worker=get_worker_info())

    return structlog.get_logger()


def run_job(job_id):

    jobpath = os.path.join(JOB_FOLDER, job_id + '.yml')

    job = load_yaml(jobpath)

    log = setup_logger(job)

    log.info('Start Job')
    func = get_func_from_source(**job['source'])
    func(**job['parameter'])

