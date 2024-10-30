use cwise_db;

drop table if exists user;
drop table if exists department;
drop table if exists course;
drop table if exists professor;
drop table if exists review;


CREATE TABLE user (
  `uid` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(50),
  `profile_pic` varchar(100),
  `email` varchar(30),
  `password` varchar(30)
);

CREATE TABLE department (
  `did` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(30)
);

CREATE TABLE course (
  `cid` int PRIMARY KEY AUTO_INCREMENT,
  `did` int,
  `course_code` varchar(10),
  `name` varchar(30)
);

CREATE TABLE professor (
  `pid` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(30),
  `department_id` int
);

CREATE TABLE review (
  `rid` int PRIMARY KEY AUTO_INCREMENT,
  `course_id` int,
  `user_id` int,
  `difficulty` enum("Easy","Medium","Hard"),
  `credit` enum("Credit","Credit-Non","Mandatory Credit-Non"),
  `prof_name` varchar(40),
  `prof_id` int,
  `prof_rating` enum("1","2","3","4","5"),
  `sem` enum("Fall","Winter","Spring","Summer"),
  `year` char(4),
  `take_again` enum("Yes","No"),
  `load_heavy` enum("Light","Medium","Heavy"),
  `office_hours` enum("Always Available","Sometimes Available","Never Available","Need to Schedule"),
  `helped_learn` enum("Yes","No"),
  `stim_interest` enum("Yes","No"),
  `description` varchar(255),
  `last_updated` timestamp
);

ALTER TABLE `course` ADD FOREIGN KEY (`did`) REFERENCES `department` (`did`);

ALTER TABLE `professor` ADD FOREIGN KEY (`department_id`) REFERENCES `department` (`did`);

ALTER TABLE `review` ADD FOREIGN KEY (`course_id`) REFERENCES `course` (`cid`);

ALTER TABLE `review` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`uid`);

ALTER TABLE `review` ADD FOREIGN KEY (`prof_id`) REFERENCES `professor` (`pid`);
