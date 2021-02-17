CREATE TABLE IF NOT EXISTS stg_songs (
    num_songs INT
    , artist_id VARCHAR(max)
    , artist_latitude DECIMAL(9, 6)
    , artist_longitude DECIMAL(9, 6)
    , artist_location VARCHAR(max)
    , artist_name VARCHAR(max)
    , song_id VARCHAR(max)
    , title VARCHAR(max)
    , duration DECIMAL(10,6)
    , year INT
);
