SELECT t.exp_id, t.job_id, source, project, parameter, "data", labels, data_stored, output_models
FROM {schema}.job t
JOIN {schema}.experiment p
ON t.exp_id = p.exp_id
WHERE t.job_id = %(job_id)s
