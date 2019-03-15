CREATE TABLE IF NOT EXISTS {schema}.plan (
	plan_id serial NOT NULL,
    project text NULL,
    "name" text NULL,
    source jsonb NULL,
    task jsonb NULL,
    plan jsonb NULL,
    date_created timestamp DEFAULT NOW(),
	PRIMARY KEY (plan_id)
);

CREATE TABLE IF NOT EXISTS {schema}.task (
	task_id serial NOT NULL,
    plan_id integer NOT NULL,
    labels jsonb NULL,
    parameter jsonb NULL,
    "data" jsonb NULL,
    worker text NULL,
    "status" text DEFAULT 'UNASSIGNED',
    date_created timestamp DEFAULT NOW(),
    date_updated timestamp DEFAULT NOW(),
    date_started timestamp NULL,
    date_finished timestamp NULL,
    data_stored jsonb DEFAULT '{{}}'::jsonb,
    output_models jsonb DEFAULT '{{}}'::jsonb,
	PRIMARY KEY (task_id)
);


CREATE TABLE IF NOT EXISTS {schema}.record (
    record_id serial NOT NULL,
    task_id integer NOT NULL,
    date_added timestamp DEFAULT NOW(),
    "event_name" text NULL,
    context jsonb NULL,
    metrics jsonb NULL,
	PRIMARY KEY (record_id)
);

CREATE INDEX IF NOT EXISTS task_plan_id ON {schema}.task(plan_id);
