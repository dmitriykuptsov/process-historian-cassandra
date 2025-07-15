create database ph;

use ph;

create table if not exists Users (
    username varchar(100) PRIMARY KEY,
    password varchar(200) NOT NULL,
    salt varchar(200) NOT NULL
);

create table if not exists Sensors (
    tag varchar(100) PRIMARY KEY,
    description varchar(1000),
    master_secret varchar(200)
);

create table if not exists Attributes (
    tag varchar(100),
    attribute varchar(100),
    PRIMARY KEY(tag, attribute),
    FOREIGN KEY (tag) 
        REFERENCES Sensors(tag) 
        ON DELETE CASCADE
);