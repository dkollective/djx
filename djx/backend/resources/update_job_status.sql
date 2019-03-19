UPDATE {schema}.job
SET "status" = %(status)s,
date_updated = NOW(),
date_finished = CASE WHEN %(status)s='FINISHED' THEN NOW() ELSE NULL END
WHERE job_id = %(job_id)s;
