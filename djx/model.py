import os
import uuid
from joblib import dump, load
from djx.backend import psql as backend
from djx.task import get_task_id

MODEL_STORE = os.environ['DJX_MODEL_STORE']


def save(model, name):
    model_path = os.path.join(MODEL_STORE, uuid.uuid4().hex + '.pkl')
    dump(model, model_path)
    task_id = get_task_id()
    backend.update_task_files(task_id, {name: model_path})


def load(task_id, name):
    task = backend.get_task(task_id)
    model_path = task['output_model'][name]
    model = load(model_path)
    return model
