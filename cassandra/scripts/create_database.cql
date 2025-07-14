CREATE KEYSPACE ph WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};
CREATE TABLE ph.ph (
    tag text,
    date_bucket date,
    ts timestamp,
    value float,
    PRIMARY KEY ((tag, date_bucket), ts) )
WITH CLUSTERING ORDER BY (ts ASC);
