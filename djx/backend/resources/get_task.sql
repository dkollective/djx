WITH ot as (
    SELECT *
    FROM {schema}.tasks
    WHERE plan_id = %(plan_id)s
    AND "status" = 'UNASSIGNED'
    LIMIT 1
)
UPDATE dummy
SET ot.status = 'ASSIGNED',
ot.worker = %(worker)s,
ot.date_started = NOW()
FROM ot
WHERE dummy.task_id = ot.taks_id
RETURNING *;
