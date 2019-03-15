SELECT
    p.plan_id,
    t.task_id,
    r.date_added,
    p.project,
    p."name" as plan_name,
    r.event_name,
    t.labels,
    r.context,
    r.metrics
FROM {schema}.task t
JOIN {schema}.plan p
ON t.plan_id = p.plan_id
JOIN {schema}.record r
ON t.task_id = r.task_id
WHERE t.plan_id = %(plan_id)s
