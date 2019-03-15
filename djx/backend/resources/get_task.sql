SELECT t.plan_id, t.task_id, source, project, parameter, "data", labels, data_stored, output_models
FROM {schema}.task t
JOIN {schema}.plan p
ON t.plan_id = p.plan_id
WHERE t.task_id = %(task_id)s
