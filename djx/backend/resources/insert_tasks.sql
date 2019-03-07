INSERT INTO {schema}.plan (plan_id, task, worker, "status", date_created, date_started, date_finished, output_records, output_files)
VALUES %s
RETURNING task_id
