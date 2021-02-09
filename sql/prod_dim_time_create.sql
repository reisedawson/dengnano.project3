CREATE TABLE IF NOT EXISTS dim_time (
    start_time TIMESTAMPTZ PRIMARY KEY NOT NULL distkey sortkey
    , start_hour SMALLINT NOT NULL
    , start_day  SMALLINT NOT NULL
    , start_week  SMALLINT NOT NULL
    , start_month  SMALLINT NOT NULL
    , start_year  SMALLINT NOT NULL
    , start_weekday  SMALLINT NOT NULL
);
