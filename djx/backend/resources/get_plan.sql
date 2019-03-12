SELECT t.plan_id, t.task_id, source, project, parameter, "data", labels, data_stored, output_records, output_models
FROM {schema}.task t
JOIN {schema}.plan p
ON t.plan_id = p.plan_id
WHERE t.plan_id = %(plan_id)s
