CREATE TABLE IF NOT EXISTS dim_users (
    user_id BIGINT PRIMARY KEY NOT NULL
    , first_name VARCHAR(MAX) NOT NULL
    , last_name VARCHAR(MAX) NOT NULL
    , gender CHAR(1)
    , level CHAR(4)
);
