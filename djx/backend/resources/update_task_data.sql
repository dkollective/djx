UPDATE {schema}.task
SET
date_updated = NOW(),
data_stored = data_stored || %(data_stored)s
WHERE task_id = %(task_id)s;
