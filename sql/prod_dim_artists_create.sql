CREATE TABLE IF NOT EXISTS dim_artists (
    artist_id VARCHAR(max) PRIMARY KEY NOT NULL
    , artist_name VARCHAR(max) NOT NULL
    , artist_location VARCHAR(max)
    , latitude DECIMAL(9, 6)
    , longitude DECIMAL(9, 6)
);
