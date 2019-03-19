INSERT INTO {schema}.experiment (project, "name", source, job, experiment)
VALUES (%(project)s, %(name)s, %(source)s, %(job)s, %(experiment)s)
RETURNING exp_id
