UPDATE {schema}.task
SET "status" = %(status)s,
date_updated = NOW(),
date_finished = CASE WHEN %(status)s='FINISHED' THEN NOW() ELSE NULL END
WHERE task_id = %(task_id)s;
