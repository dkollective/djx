INSERT INTO {schema}.plan (plan_id, task, labels)
VALUES %s
RETURNING task_id
