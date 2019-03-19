UPDATE {schema}.job
SET
date_updated = NOW(),
data_stored = data_stored || %(data_stored)s
WHERE job_id = %(job_id)s;
