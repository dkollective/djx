INSERT INTO {schema}.plan (project, "name", source, task, plan, date_created)
VALUES (%(project)s, %(name)s, %(source)s, %(task)s, %(plan)s, %(date_created)s)
RETURNING plan_id
