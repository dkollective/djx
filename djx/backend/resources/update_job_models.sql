UPDATE {schema}.job
SET
date_updated = NOW(),
output_models = output_models || %(output_models)s
WHERE job_id = %(job_id)s;
