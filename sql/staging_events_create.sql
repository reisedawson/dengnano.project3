CREATE TABLE IF NOT EXISTS stg_events (
    artist VARCHAR(max)
    , auth VARCHAR(max)
    , firstName VARCHAR(max)
    , gender VARCHAR(1)
    , itemInSession BIGINT
    , lastName VARCHAR(max)
    , length DECIMAL(10,6)
    , level VARCHAR(4)
    , location VARCHAR(max)
    , method VARCHAR(10)
    , page VARCHAR(10)
    , registration VARCHAR(max)
    , sessionId BIGINT
    , song VARCHAR(max)
    , status SMALLINT
    , ts BIGINT
    , userAgent VARCHAR(max)
    , userId BIGINT
);
