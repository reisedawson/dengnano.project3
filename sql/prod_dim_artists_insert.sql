-- Perform a deletion and insertion within a transaction
-- to ensure we don't have duplicate artists in the dimension
-- table since we don't have access to relational integrity
-- in Redshift
BEGIN TRANSACTION;

-- Delete any records from the artist dimension that have a
-- corresponding id in the staging table
DELETE FROM dim_artists
USING stg_songs 
WHERE dim_artists.artist_id = stg_songs.artist_id;

-- Insert the whole staging songs table into the artist dimension
INSERT INTO dim_artists (artist_id, artist_name, artist_location, latitude, longitude)
(
    SELECT
        artist_id
        , artist_name
        , artist_location
        , artist_latitude
        , artist_longitude
    FROM 
        stg_songs
);

END TRANSACTION;
