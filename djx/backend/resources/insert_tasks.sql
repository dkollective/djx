INSERT INTO {schema}.task (plan_id, parameter, "data", labels)
VALUES %s
RETURNING task_id
