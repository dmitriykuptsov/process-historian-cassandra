CREATE KEYSPACE ph WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};
CREATE TABLE ph.ph_data (
    tag text,
    date_bucket date,
    hour int,
    ts timestamp,
    value float,
    PRIMARY KEY ((tag, date_bucket, hour), ts) )
WITH CLUSTERING ORDER BY (ts ASC);
