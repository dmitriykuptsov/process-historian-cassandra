create database ph;

use ph;

create table if not exists Verifications (
    username varchar(100),
    email varchar(100) NOT NULL,
    token varchar(256) NOT NULL,
    exp INT DEFAULT 0
)

create table if not exists Users (
    username varchar(100) PRIMARY KEY,
    email varchar(100),
    password varchar(200) NOT NULL,
    salt varchar(200) NOT NULL
);

create table if not exists Sensors (
    tag varchar(100) PRIMARY KEY,
    description varchar(1000),
    master_secret varchar(200),
    is_public_read INT DEFAULT FALSE,
    owner varchar(100)
);

create table if not exists Attributes (
    tag varchar(100),
    attribute varchar(100),
    PRIMARY KEY(tag, attribute),
    FOREIGN KEY (tag) 
        REFERENCES Sensors(tag) 
        ON DELETE CASCADE
);

create table if not exists SensorPermissions (
    tag varchar(100),
    username varchar(100),
    owner varchar(100),
    allowed bit,
    PRIMARY KEY(tag, username),
    FOREIGN KEY (tag) 
        REFERENCES Sensors(tag) 
        ON DELETE CASCADE,
    FOREIGN KEY (username) 
        REFERENCES Users(username) 
        ON DELETE CASCADE
);

create table if not exists Alerts(
    tag varchar(100) not null,
    timestamp datetime not null,
    type int not null,
    comment varchar(100) default "",
    PRIMARY KEY(tag, timestamp, type),
    FOREIGN KEY (tag)
        REFERENCES Sensors(tag) 
        ON DELETE CASCADE
);



INSERT INTO Users(username, password, salt) VALUES("admin", SHA2(CONCAT("password", "DanWocsAtAv8"), 256), "DanWocsAtAv8");