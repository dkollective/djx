WITH ot as (
    SELECT t.plan_id, t.task_id, source, project, parameter, "data", labels
    FROM {schema}.task t
    JOIN {schema}.plan p
    ON t.plan_id = p.plan_id
    WHERE t.plan_id = %(plan_id)s
    AND "status" = 'UNASSIGNED'
    LIMIT 1
)
UPDATE {schema}.task tt
SET "status" = 'ASSIGNED',
worker = %(worker)s,
date_started = NOW()
FROM ot
WHERE tt.task_id = ot.task_id
RETURNING tt.plan_id, tt.task_id, source, project, tt.data, tt.parameter, tt.labels, tt.worker;
