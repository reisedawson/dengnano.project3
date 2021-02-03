-- Perform a deletion and insertion within a transaction
-- to ensure we don't have duplicate times in the dimension
-- table since we don't have access to relational integrity
-- in Redshift
BEGIN TRANSACTION;

-- Delete any records from the time dimension that have a
-- corresponding id in the staging table
DELETE FROM dim_time
USING stg_events 
WHERE dim_time.start_time = TIMESTAMP 'epoch' + stg_events.ts/1000 *INTERVAL '1 second';

-- Insert the whole staging songs table into the time dimension
INSERT INTO dim_time (start_time, start_hour, start_day, start_week, start_month, start_year, start_weekday)
(
    SELECT
        TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second'
        , EXTRACT(hour FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second')
        , EXTRACT(day FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second')
        , EXTRACT(week FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second')
        , EXTRACT(month FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second')
        , EXTRACT(year FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second')
        , EXTRACT(weekday FROM TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second')
    FROM 
        stg_events
    WHERE
        page = 'NextSong'
);

END TRANSACTION;
