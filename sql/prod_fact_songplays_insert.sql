-- Insert the whole staging events table into the songplays fact table
-- In reality I would make sure to do some kind of clearing down of the
-- staging area following this. 
-- TODO: This may be something I could add within a transaction to this
--       script once all is complete/tested/approved. 
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
