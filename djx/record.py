from djx.task import get_task_id
from djx.backend import psql as backend


__context = {}


def reset():
    global __context
    task_id = get_task_id()
    __context[task_id] = {}


def bind(**context):
    global __context
    task_id = get_task_id()
    __context[task_id] = {**__context, **context}


def rm(*args):
    global __context
    task_id = get_task_id()
    __context[task_id] = {k: v for k, v in __context.items() if k not in args}


def rec(event_name, **metrics):
    task_id = get_task_id()
    backend.add_record(
        task_id, event_name, __context.get(task_id, {}), metrics)
