CREATE TABLE IF NOT EXISTS dim_songs (
    song_id VARCHAR(MAX) PRIMARY KEY NOT NULL
    , title VARCHAR(MAX) NOT NULL
    , artist_id VARCHAR(MAX) NOT NULL
    , start_year SMALLINT
    , duration DECIMAL(10,6)
);
