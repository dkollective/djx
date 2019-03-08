UPDATE {schema}.tasks
SET "status" = %(status)s,
date_finished = NOW(),
output_records = %(output_records)s,
output_files = %(output_files)s,
data_stored =  %(data_stored)s,
WHERE task_id = %(task_id)s;
