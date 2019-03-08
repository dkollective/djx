WITH ot as (
    SELECT plan_id, task_id, "entry", project, parameter, "data", labels
    FROM {schema}.tasks t
    JOIN {schema}.plans p
    ON t.plan_id = p.plan_id
    WHERE plan_id = %(plan_id)s
    AND "status" = 'UNASSIGNED'
    LIMIT 1
)
UPDATE dummy
SET ot.status = 'ASSIGNED',
ot.worker = %(worker)s,
ot.date_started = NOW()
FROM ot
WHERE dummy.task_id = ot.task_id
RETURNING *;
