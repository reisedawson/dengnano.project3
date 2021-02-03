CREATE TABLE IF NOT EXISTS dim_songs (
    song_id VARCHAR(max) PRIMARY KEY NOT NULL
    , title VARCHAR(max) NOT NULL
    , artist_id VARCHAR(max) NOT NULL
    , song_year SMALLINT
    , duration DECIMAL(10, 6)
);
