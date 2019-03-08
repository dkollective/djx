import os
import psycopg2
import psycopg2.extras
from psycopg2.extras import Json
from pkg_resources import resource_filename


db_info = {
    'host': os.environ['DJX_PG_HOST'],
    'port': os.environ['DJX_PG_PORT'],
    'user': os.environ['DJX_PG_USER'],
    'password': os.environ['DJX_PG_PASSWORD'],
    'dbname': os.environ['DJX_PG_DBNAME']
}

SCHEMA = os.environ['DJX_PG_SCHEMA']


def to_json(d):
    if isinstance(d, (dict, list)):
        return Json(d)
    else:
        return d


def dict_to_json(d):
    return {k: to_json(v) for k, v in d.items()}


def get_connection():
    conn = psycopg2.connect(
        **db_info, cursor_factory=psycopg2.extras.RealDictCursor)
    return conn


def setup_ddl():
    query = load_query('ddl.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, {})


def load_query(filename):
    fname = resource_filename(__name__, os.path.join('resources', filename))
    with open(fname, 'r') as f:
        return f.read().format(schema=SCHEMA)


def insert_plan(plan):
    query = load_query('insert_plan.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, dict_to_json(plan))
        inserted = cursor.fetchall()
    print(inserted)
    return inserted[0]['plan_id']


def insert_tasks(tasks):
    print(tasks)
    columns = ['plan_id', 'parameter', 'data', 'labels']
    data = [
        [to_json(task.get(col)) for col in columns]
        for task in tasks
    ]
    query = load_query('insert_tasks.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        psycopg2.extras.execute_values(
            cursor, query, data, template=None, page_size=10)
        records = cursor.fetchall()
    return [r['task_id'] for r in records]


def get_next_task(batch_id):
    query = load_query('get_task.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, {'batch_id': batch_id})
        records = cursor.fetchall()
    return records[0]


def update_task(task):
    query = load_query('update_task.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, dict_to_json(task))

setup_ddl()
