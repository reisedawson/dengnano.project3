CREATE TABLE IF NOT EXISTS dim_artists (
    artist_id VARCHAR(MAX) PRIMARY KEY NOT NULL
    , artist_name VARCHAR(MAX) NOT NULL
    , artist_location VARCHAR(MAX)
    , latitude GEOMETRY
    , longitude GEOMETRY
);
