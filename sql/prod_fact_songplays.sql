CREATE TABLE IF NOT EXISTS fact_songplays (
    songplay_id BIGINT IDENTITY(0, 1) NOT NULL
    , start_time TIMESTAMPTZ NOT NULL
    , user_id BIGINT NOT NULL
    , user_level CHAR(4)
    , song_id VARCHAR(max) NOT NULL
    , artist_id VARCHAR(max) NOT NULL
    , session_id BIGINT NOT NULL
    , songplay_location VARCHAR(max)
    , user_agent VARCHAR(max)
);
