import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
staging_events_table_drop = """
    DROP TABLE IF EXISTS stg_events;
"""

staging_songs_table_drop = """
    DROP TABLE IF EXISTS stg_songs;
"""

songplay_table_drop = """
    DROP TABLE IF EXISTS fact_songplays;
"""

user_table_drop = """
    DROP TABLE IF EXISTS dim_users;
"""

song_table_drop = """
    DROP TABLE IF EXISTS dim_songs;
"""

artist_table_drop = """
    DROP TABLE IF EXISTS dim_artists;
"""

time_table_drop = """
    DROP TABLE IF EXISTS dim_time;
"""


# CREATE TABLES
staging_events_table_create = """
    CREATE TABLE IF NOT EXISTS stg_events (
        artist VARCHAR(max)
        , auth VARCHAR(max)
        , firstName VARCHAR(max)
        , gender VARCHAR(max)
        , itemInSession BIGINT
        , lastName VARCHAR(max)
        , length DECIMAL(10,6)
        , level VARCHAR(max)
        , location VARCHAR(max)
        , method VARCHAR(max)
        , page VARCHAR(max)
        , registration VARCHAR(max)
        , sessionId BIGINT
        , song VARCHAR(max)
        , status SMALLINT
        , ts BIGINT
        , userAgent VARCHAR(max)
        , userId BIGINT
    );
"""

staging_songs_table_create = """
    CREATE TABLE IF NOT EXISTS stg_songs (
        num_songs INT
        , artist_id VARCHAR(max)
        , artist_latitude VARCHAR(max)
        , artist_longitude VARCHAR(max)
        , artist_location VARCHAR(max)
        , artist_name VARCHAR(max)
        , song_id VARCHAR(max)
        , title VARCHAR(max)
        , duration DECIMAL(10,6)
        , year INT
    );
"""

songplay_table_create = """
    CREATE TABLE IF NOT EXISTS fact_songplays (
        songplay_id BIGINT IDENTITY(0, 1) NOT NULL
        , start_time TIMESTAMPTZ NOT NULL distkey sortkey
        , user_id BIGINT
        , user_level CHAR(4)
        , song_id VARCHAR(max) NOT NULL
        , artist_id VARCHAR(max) NOT NULL
        , session_id BIGINT
        , songplay_location VARCHAR(max)
        , user_agent VARCHAR(max)
    );
"""

user_table_create = """
    CREATE TABLE IF NOT EXISTS dim_users (
        user_id BIGINT PRIMARY KEY NOT NULL distkey
        , first_name VARCHAR(max) NOT NULL
        , last_name VARCHAR(max) NOT NULL
        , gender CHAR(1)
        , user_level CHAR(4)
    );
"""

song_table_create = """
    CREATE TABLE IF NOT EXISTS dim_songs (
        song_id VARCHAR(max) PRIMARY KEY NOT NULL distkey
        , title VARCHAR(max) NOT NULL
        , artist_id VARCHAR(max) NOT NULL
        , song_year SMALLINT
        , duration DECIMAL(10, 6)
    );
"""

artist_table_create = """
    CREATE TABLE IF NOT EXISTS dim_artists (
        artist_id VARCHAR(max) PRIMARY KEY NOT NULL
        , artist_name VARCHAR(max) NOT NULL
        , artist_location VARCHAR(max)
        , latitude DECIMAL(9, 6)
        , longitude DECIMAL(9, 6)
    ) DISTSTYLE ALL;
"""

time_table_create = """
    CREATE TABLE IF NOT EXISTS dim_time (
        start_time TIMESTAMPTZ PRIMARY KEY NOT NULL distkey sortkey
        , start_hour SMALLINT NOT NULL
        , start_day  SMALLINT NOT NULL
        , start_week  SMALLINT NOT NULL
        , start_month  SMALLINT NOT NULL
        , start_year  SMALLINT NOT NULL
        , start_weekday  SMALLINT NOT NULL
    );
"""


# STAGING TABLES
staging_events_copy = """
    COPY stg_events FROM {}
    credentials 'aws_iam_role={}'
    json 'auto' compupdate off region 'us-west-2';
""".format(config['S3']['LOG_DATA'],
           config['IAM_ROLE']['ARN'].replace("'", ""))

staging_songs_copy = """
    COPY stg_songs FROM {}
    credentials 'aws_iam_role={}'
    json 'auto' compupdate off region 'us-west-2';
""".format(config['S3']['SONG_DATA'],
           config['IAM_ROLE']['ARN'].replace("'", ""))


# FINAL TABLES
songplay_table_insert = """
    -- Finally, after updating all dimensions, insert all
    -- NextSong events into the songplays fact table, then
    -- empty the events staging table
    BEGIN TRANSACTION;

    -- Insert the whole staging events table into the songplays fact table
    INSERT INTO fact_songplays (start_time, user_id, user_level, song_id,
                                artist_id, session_id, songplay_location,
                                user_agent)
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
"""

user_table_insert = """
    -- Perform a deletion and insertion within a transaction
    -- to ensure we don't have duplicate users in the dimension
    -- table since we don't have access to relational integrity
    -- in Redshift
    BEGIN TRANSACTION;

    -- Delete any records from the users dimension that have a
    -- corresponding id in the staging table
    DELETE FROM dim_users
    USING stg_events
    WHERE dim_users.user_id = stg_events.userId
    AND stg_events.page = 'NextSong';

    -- Insert the whole staging events table into the users dimension
    INSERT INTO dim_users (user_id, first_name, last_name, gender, user_level)
    (
        SELECT
            userId
            , firstName
            , lastName
            , gender
            , level
        FROM
            stg_events
        WHERE
            page = 'NextSong'
            AND userId IS NOT NULL
    );

    END TRANSACTION;
"""

song_table_insert = """
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
    INSERT INTO dim_songs (song_id, title , artist_id, song_year, duration)
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
"""

artist_table_insert = """
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
    INSERT INTO dim_artists (artist_id, artist_name, artist_location, latitude,
                             longitude)
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
"""

time_table_insert = """
    -- Perform a deletion and insertion within a transaction
    -- to ensure we don't have duplicate times in the dimension
    -- table since we don't have access to relational integrity
    -- in Redshift
    BEGIN TRANSACTION;

    -- Delete any records from the time dimension that have a
    -- corresponding id in the staging table
    DELETE FROM dim_time
    USING stg_events
    WHERE dim_time.start_time = TIMESTAMP 'epoch'
                                + stg_events.ts/1000 *INTERVAL '1 second'
    AND stg_events.page = 'NextSong';

    -- Insert the whole staging events table into the time dimension
    INSERT INTO dim_time (start_time, start_hour, start_day, start_week,
                          start_month, start_year, start_weekday)
    (
        SELECT
            TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second'
            , EXTRACT(hour FROM TIMESTAMP 'epoch'
                        + ts/1000 *INTERVAL '1 second')
            , EXTRACT(day FROM TIMESTAMP 'epoch'
                        + ts/1000 *INTERVAL '1 second')
            , EXTRACT(week FROM TIMESTAMP 'epoch'
                        + ts/1000 *INTERVAL '1 second')
            , EXTRACT(month FROM TIMESTAMP 'epoch'
                        + ts/1000 *INTERVAL '1 second')
            , EXTRACT(year FROM TIMESTAMP 'epoch'
                        + ts/1000 *INTERVAL '1 second')
            , EXTRACT(weekday FROM TIMESTAMP 'epoch'
                        + ts/1000 *INTERVAL '1 second')
        FROM
            stg_events
        WHERE
            page = 'NextSong'
    );

    END TRANSACTION;
"""


# QUERY LISTS
create_table_queries = [staging_events_table_create,
                        staging_songs_table_create,
                        songplay_table_create,
                        user_table_create,
                        song_table_create,
                        artist_table_create,
                        time_table_create]
drop_table_queries = [staging_events_table_drop,
                      staging_songs_table_drop,
                      songplay_table_drop,
                      user_table_drop,
                      song_table_drop,
                      artist_table_drop,
                      time_table_drop]
copy_table_queries = [staging_events_copy,
                      staging_songs_copy]
insert_table_queries = [song_table_insert,
                        artist_table_insert,
                        time_table_insert,
                        user_table_insert,
                        songplay_table_insert]
