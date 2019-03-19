import logging
import os
import uuid
import pandas as pd
from toolz import dissoc
from djx.task import get_task_id
from djx.data_utils import copy_file
from djx.backend import psql as backend

log = logging.getLogger(__name__)

__context = {}

ARTIFACT_STORE = os.environ['DJX_ARTIFACT_STORE']
DATA_TEMP = os.environ['DJX_DATA_TEMP']


def create_artifact_path():
    path = os.path.join(ARTIFACT_STORE, uuid.uuid4().hex + '.pkl')
    return path


def store_artifact(temp_path):
    _, extension = os.path.splitext(temp_path)
    artifact_id = uuid.uuid4().hex
    if extension:
        filename = artifact_id + extension
    else:
        filename = artifact_id
    path = os.path.join(ARTIFACT_STORE, filename)
    copy_file(temp_path, path)
    return path


def store_artifacts(artifacts):
    return {name: store_artifact(path) for name, path in artifacts.items()}


def reset():
    global __context
    task_id = get_task_id()
    __context[task_id] = {}


def bind(**context):
    global __context
    task_id = get_task_id()
    __context[task_id] = {**__context.get(task_id, {}), **context}


def rm(*args):
    global __context
    task_id = get_task_id()
    __context[task_id] = {
        k: v for k, v in __context.get(task_id, {}).items() if k not in args}


def rec(event_name, metrics={}, context={}, artifacts={}):
    task_id = get_task_id()
    _artifacts = store_artifacts(artifacts)
    context = {**__context.get(task_id, {}), **context}
    backend.add_record(
        task_id, event_name, context, metrics, _artifacts)
    metrics_str = ' | '.join([f'{k}:{v}' for k, v in metrics.items()])
    context_str = ' | '.join([f'{k}:{v}' for k, v in context.items()])
    artifact_str = '\n stored >> '.join([''] + [f'{k} : {v}' for k, v in _artifacts.items()])
    log_str = f'{task_id} >> {event_name} >> {context_str} >> {metrics_str}{artifact_str}'
    log.info(log_str)


def get_plan_records_df(plan_id):
    records = backend.get_plan_records(plan_id)
    order = ['plan_id', 'task_id', 'date_added', 'project', 'plan_name', 'event_name']
    expand = ['labels', 'context', 'metrics']
    expand_set = {ex: set() for ex in expand}
    _records = []
    for rec in records:
        _rec = dissoc(rec, *expand)
        for ex in expand:
            _ex_rec = {f'{ex}.{k}': v for k, v in rec[ex].items()}
            _rec = {**_rec, **_ex_rec}
            expand_set[ex] |= _ex_rec.keys()
        _records.append(_rec)
    for ex in expand:
        order += list(expand_set[ex])
    return pd.DataFrame.from_records(_records)[order]


def get_temp_path():
    return os.path.join(DATA_TEMP, uuid.uuid4().hex + '.pkl')
