SELECT
    p.exp_id,
    t.job_id,
    r.date_added,
    p.project,
    p."name" as exp_name,
    r.event_name,
    t.labels,
    r.context,
    r.metrics
FROM {schema}.job t
JOIN {schema}.experiment p
ON t.exp_id = p.exp_id
JOIN {schema}.record r
ON t.job_id = r.job_id
WHERE t.exp_id = %(exp_id)s
