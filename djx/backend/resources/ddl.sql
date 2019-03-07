CREATE IF NOT EXISTS TABLE {schema}.plan (
	plan_id serial NOT NULL,
    project text NULL,
    "name" text NULL,
    source jsonb NULL,
    task jsonb NULL,
    plan jsonb NULL,
    date_created timestamp NOW(),
	PRIMARY KEY (plan_id)
);

CREATE IF NOT EXISTS  TABLE {schema}.task (
	task_id serial NOT NULL,
    plan_id NOT NULL,
    task jsonb NULL,
    labels jsonb NULL,
    worker text NULL,
    "status" text NULL,
    date_created timestamp NOW(),
    date_started timestamp NULL,
    date_finished timestamp NULL,
    output_records jsonb NULL,
    output_files jsonb NULL,
	PRIMARY KEY (task_id)
);

CREATE IF NOT EXISTS INDEX ON {schema}.task(plan_id);
