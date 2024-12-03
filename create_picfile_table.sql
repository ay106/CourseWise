-- SQL to create profile picture table in cwise database
use cwise_db;

DROP TABLE IF EXISTS picfile;

CREATE TABLE picfile (
    `uid` int PRIMARY KEY,
    `filename` varchar(50),
    foreign key (`uid`) references `user` (`uid`) 
        on delete cascade on update cascade
);

-- default user
-- INSERT INTO `user` (`uid`,`name`,`profile_pic`,`email`,`password`)
-- VALUES (0, 'default_user',NULL,NULL,NULL);

-- INSERT INTO picfile (`uid`, `filename`) 
-- VALUES (0, 'default.jpg');

DESCRIBE picfile;