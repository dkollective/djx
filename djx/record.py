import logging
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
    metrics_str = [f'{k}:{v}' for k, v in metrics.items()]
    context_str = [f'{k}:{v}' for k, v in context.items()]
    log.warning(
        event_name + ' >> ' + ' | '.join(context_str) + ' >> ' + ' | '.join(metrics_str))
