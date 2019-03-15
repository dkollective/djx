import logging
import pandas as pd
from toolz import dissoc
from djx.task import get_task_id
from djx.backend import psql as backend

log = logging.getLogger(__name__)

__context = {}


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


def rec(event_name, **metrics):
    task_id = get_task_id()
    context = __context.get(task_id, {})
    backend.add_record(
        task_id, event_name, __context.get(task_id, {}), metrics)
    metrics_str = ' | '.join([f'{k}:{v}' for k, v in metrics.items()])
    context_str = ' | '.join([f'{k}:{v}' for k, v in context.items()])
    log.warning(f'{task_id} >> {event_name} >> {context_str} >> {metrics_str}')


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


