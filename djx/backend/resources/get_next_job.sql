WITH ot as (
    SELECT t.exp_id, t.job_id, source, project, parameter, "data", labels
    FROM {schema}.job t
    JOIN {schema}.experiment p
    ON t.exp_id = p.exp_id
    WHERE t.exp_id = %(exp_id)s
    AND "status" = 'UNASSIGNED'
    LIMIT 1
)
UPDATE {schema}.job tt
SET "status" = 'ASSIGNED',
worker = %(worker)s,
date_started = NOW()
FROM ot
WHERE tt.job_id = ot.job_id
RETURNING tt.exp_id, tt.job_id, source, project, tt.data, tt.data_stored, tt.parameter, tt.labels, tt.worker;
