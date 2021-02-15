-- Finally, after updating all dimensions, insert all
-- NextSong events into the songplays fact table, then
-- empty the events staging table 
BEGIN TRANSACTION;

-- Insert the whole staging events table into the songplays fact table
INSERT INTO fact_songplays (start_time, user_id, user_level, song_id, artist_id, session_id, songplay_location, user_agent)
(
    SELECT
        TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second'
        , userId
        , level
        , song
        , artist
        , sessionId
        , location
        , userAgent
    FROM 
        stg_events
    WHERE
        page = 'NextSong'
);

-- Empty the staging table now we have used all the data from it
DELETE FROM stg_events;

END TRANSACTION;
