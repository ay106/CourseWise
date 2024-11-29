-- SQL to create profile picture table in cwise database
use cwise_db;

DROP TABLE IF EXISTS picfile;

CREATE TABLE picfile (
    `uid` int PRIMARY KEY,
    `filename` varchar(50),
    foreign key (`uid`) references `user` (`uid`) 
        on delete cascade on update cascade
);
describe picfile;