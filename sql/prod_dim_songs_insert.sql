-- Perform a deletion and insertion within a transaction
-- to ensure we don't have duplicate songs in the dimension
-- table since we don't have access to relational integrity
-- in Redshift
BEGIN TRANSACTION;

-- Delete any records from the song dimension that have a
-- corresponding id in the staging table
DELETE FROM dim_songs
USING stg_songs 
WHERE dim_songs.song_id = stg_songs.song_id;

-- Insert the whole staging songs table into the song dimension
INSERT INTO dim_songs (song_id, title , artist_id, start_year, duration)
(
    SELECT
        song_id
        , title
        , artist_id
        , year
        , duration
    FROM 
        stg_songs
);

END TRANSACTION;
