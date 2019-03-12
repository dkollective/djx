UPDATE {schema}.task
SET "status" = %(status)s,
date_updated = NOW()
WHERE task_id = %(task_id)s;
