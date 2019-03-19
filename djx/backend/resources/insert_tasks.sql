INSERT INTO {schema}.task (plan_id, parameter, "data", labels, data_stored)
VALUES %s
RETURNING task_id
