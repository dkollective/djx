import logging
from djx.utils import get_method, get_worker_info, load_yaml



from pandas.io.json import json_normalize

JOB_FOLDER = os.environ['DJX_JOB_FOLDER']



def get_func_from_source(entry, source_type, **kwargs):
    if source_type == 'PYTHON_MODULE':
        return get_method(entry)
    else:
        raise NotImplementedError(f'Source type {source_type} not implemented.')


def run(job_id):

    jobpath = os.path.join(JOB_FOLDER, job_id + '.yml')
    job = load_yaml(jobpath)

    worker = get_worker_info()
    job['worker'] = worker

    normalized_job = json_normalize(job)

    with mlflow.start_run():
        mlflow.log_params(normalized_job)
        func = get_func_from_source(**job['source'])
        func(**job['parameter'])

