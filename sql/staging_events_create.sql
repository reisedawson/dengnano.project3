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
