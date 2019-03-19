-- DROP TABLE IF EXISTS {schema}.experiment;
-- DROP TABLE IF EXISTS {schema}.job;
-- DROP TABLE IF EXISTS {schema}.record;


CREATE TABLE IF NOT EXISTS {schema}.experiment (
	exp_id serial NOT NULL,
    project text NULL,
    "name" text NULL,
    source jsonb NULL,
    job jsonb NULL,
    experiment jsonb NULL,
    date_created timestamp DEFAULT NOW(),
	PRIMARY KEY (exp_id)
);

CREATE TABLE IF NOT EXISTS {schema}.job (
	job_id serial NOT NULL,
    exp_id integer NOT NULL,
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
	PRIMARY KEY (job_id)
);


CREATE TABLE IF NOT EXISTS {schema}.record (
    record_id serial NOT NULL,
    job_id integer NOT NULL,
    date_added timestamp DEFAULT NOW(),
    "event_name" text NULL,
    context jsonb NULL,
    metrics jsonb NULL,
    artifacts jsonb NULL,
	PRIMARY KEY (record_id)
);

CREATE INDEX IF NOT EXISTS job_exp_id ON {schema}.job(exp_id);
