import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
staging_events_table_drop = open('sql/staging_events_drop.sql', 'r').read()
staging_songs_table_drop = open('sql/staging_songs_drop.sql', 'r').read()
songplay_table_drop = open('sql/prod_fact_songplays_drop.sql', 'r').read()
user_table_drop = open('sql/prod_dim_users_drop.sql', 'r').read()
song_table_drop = open('sql/prod_dim_songs_drop.sql', 'r').read()
artist_table_drop = open('sql/prod_dim_artists_drop.sql', 'r').read()
time_table_drop = open('sql/prod_dim_time_drop.sql', 'r').read()

# CREATE TABLES
staging_events_table_create = open('sql/staging_events_create.sql', 'r').read()
staging_songs_table_create = open('sql/staging_songs_create.sql', 'r').read()
songplay_table_create = open('sql/prod_fact_songplays_create.sql', 'r').read()
user_table_create = open('sql/prod_dim_users_create.sql', 'r').read()
song_table_create = open('sql/prod_dim_songs_create.sql', 'r').read()
artist_table_create = open('sql/prod_dim_artists_create.sql', 'r').read()
time_table_create = open('sql/prod_dim_time_create.sql', 'r').read()

# STAGING TABLES
staging_events_copy = open('sql/staging_events_copy.sql', 'r').read().format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'].replace("'",""))
staging_songs_copy = open('sql/staging_songs_copy.sql', 'r').read().format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'].replace("'",""))

# FINAL TABLES
songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

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
insert_table_queries = [songplay_table_insert,
                        user_table_insert,
                        song_table_insert,
                        artist_table_insert,
                        time_table_insert]
