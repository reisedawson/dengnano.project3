CREATE TABLE IF NOT EXISTS dim_users (
    user_id BIGINT PRIMARY KEY NOT NULL
    , first_name VARCHAR(max) NOT NULL
    , last_name VARCHAR(max) NOT NULL
    , gender CHAR(1)
    , user_level CHAR(4)
);
