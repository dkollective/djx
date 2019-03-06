import pandas as pd

PLAN_FILE = 'data/batch.pkl'
TASK_FILE = 'data/task.pkl'


def write_plan(plan):
    try:
        df = pd.read_pickle(PLAN_FILE).reset_index(drop=True)
    except BaseException:
        df = pd.DataFrame().from_records(plan)
    else:
        df = df.append(plan)
    df.set_index('task_id', drop=False).to_pickle(PLAN_FILE)


def write_task(task):
    try:
        df = pd.read_pickle(TASK_FILE).reset_index(drop=True)
    except BaseException:
        df = pd.DataFrame().from_records(task)
    else:
        df = df.append(task)
    df.set_index('task_id', drop=False).to_pickle(TASK_FILE)


def get_plan(plan_ids):
    try:
        df = pd.read_pickle(PLAN_FILE)
        plan = df[df['plan_id'].isin(plan_ids)].to_records()
    except:
        plan = []
    return plan


def get_task(**kwargs):
    try:
        df = pd.read_pickle(TASK_FILE)
        selections = [
            df[k].isin(v) if isinstance(v, list) else df[k] == v
            for k, v in kwargs.items()
        ]
        task = df[all(selections)].to_records()
    except:
        task = []
    return task


def get_next_task(plan_ids):
    try:
        df = pd.read_pickle(TASK_FILE)
        completed_tasks = set(df.loc[df['state'] == 'COMPLETED', 'task_id'])
        dfp = df[df['plan_id'].isin(plan_ids)]
        
        pending = df['dependencies'].apply(lambda dep: set(dep).isubset(completed_tasks))
        task_id = pending.iloc[0].task_id
        df.loc[task_id,'state'] = 'RUNNING'
        df.to_pickle(TASK_FILE)
        plan = df[task_id].to_dict()
    except:
        plan = None
    return plan


