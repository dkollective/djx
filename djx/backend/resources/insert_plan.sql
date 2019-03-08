INSERT INTO {schema}.plan (project, "name", source, task, plan)
VALUES (%(project)s, %(name)s, %(source)s, %(task)s, %(plan)s)
RETURNING plan_id
