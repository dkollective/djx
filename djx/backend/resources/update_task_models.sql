UPDATE {schema}.task
SET
date_updated = NOW(),
output_models = output_models || %(output_models)s,
WHERE task_id = %(task_id)s;
