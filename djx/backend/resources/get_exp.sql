SELECT t.exp_id, t.job_id, source, project, parameter, "data", labels, data_stored, output_records, output_models
FROM {schema}.job t
JOIN {schema}.experiment p
ON t.exp_id = p.exp_id
WHERE t.exp_id = %(exp_id)s
