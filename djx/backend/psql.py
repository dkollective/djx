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


def insert_exp(exp):
    query = load_query('insert_exp.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, dict_to_json(exp))
        inserted = cursor.fetchall()
    print(inserted)
    return inserted[0]['exp_id']


def insert_jobs(jobs):
    print(jobs)
    columns = ['exp_id', 'parameter', 'data', 'labels', 'data_stored']
    data = [
        [to_json(job.get(col)) for col in columns]
        for job in jobs
    ]
    query = load_query('insert_jobs.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        psycopg2.extras.execute_values(
            cursor, query, data, template=None, page_size=10)
        records = cursor.fetchall()
    return [r['job_id'] for r in records]


def get_next_job(exp_id, worker):
    query = load_query('get_next_job.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, {'exp_id': exp_id, 'worker': worker})
        records = cursor.fetchall()
    if records:
        return records[0]


def update_job_data(job_id, data_stored):
    query = load_query('update_job_data.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            query, {'job_id': job_id, 'data_stored': to_json(data_stored)})


def update_job_status(job_id, status):
    query = load_query('update_job_status.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            query, {'job_id': job_id, 'status': status})


def update_job_models(job_id, output_models):
    query = load_query('update_job_models.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            query, {'job_id': job_id, 'output_models': to_json(output_models)})


def add_record(job_id, event_name, context, metrics, artifacts):
    query = load_query('add_record.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            query, {
                'job_id': job_id, 'event_name': event_name,
                'context': to_json(context), 'metrics': to_json(metrics),
                'artifacts': to_json(artifacts)
            })


def get_exp_records(exp_id):
    query = load_query('get_exp_records.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, {'exp_id': exp_id})
        records = cursor.fetchall()
    if records:
        return records


def get_job(job_id):
    query = load_query('get_job.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, {'job_id': job_id})
        records = cursor.fetchall()
    if records:
        return records[0]


def get_exp(exp_id):
    query = load_query('get_job.sql')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, {'exp_id': exp_id})
        records = cursor.fetchall()
    if records:
        return records


setup_ddl()
