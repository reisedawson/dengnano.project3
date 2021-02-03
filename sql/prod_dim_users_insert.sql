-- Perform a deletion and insertion within a transaction
-- to ensure we don't have duplicate users in the dimension
-- table since we don't have access to relational integrity
-- in Redshift
BEGIN TRANSACTION;

-- Delete any records from the users dimension that have a
-- corresponding id in the staging table
DELETE FROM dim_users
USING stg_events 
WHERE dim_users.user_id = stg_events.userId
AND stg_events.page = 'NextSong';

-- Insert the whole staging events table into the users dimension
INSERT INTO dim_users (user_id, first_name, last_name, gender, user_level)
(
    SELECT
        userId
        , firstName
        , lastName
        , gender
        , level
    FROM 
        stg_events
    WHERE
        page = 'NextSong'
        AND userId IS NOT NULL
);

END TRANSACTION;
