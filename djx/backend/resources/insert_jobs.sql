INSERT INTO {schema}.job (exp_id, parameter, "data", labels, data_stored)
VALUES %s
RETURNING job_id
