-- MariaDB dump 10.19  Distrib 10.5.22-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: cwise_db
-- ------------------------------------------------------
-- Server version	10.5.22-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `did` int(11) DEFAULT NULL,
  `course_code` varchar(10) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`cid`),
  KEY `did` (`did`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`did`) REFERENCES `department` (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,18,'CS 111','Computer Programming and Problem Solving'),(2,18,'CS 230','Data Structures'),(3,18,'CS 231','Fundamental Algorithms'),(4,18,'CS 235','Theory of Computation'),(5,18,'CS 240','Foundations of Computer Systems with Laboratory'),(6,18,'CS 304','Databases with Web Interfaces'),(7,53,'RUSS 276','Fedor Dostoevsky: The Seer of Spirit (in English)'),(8,18,'CS 242','Computer Networks'),(9,8,'ASTR 100','Life in the Universe');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `department` (
  `did` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (1,'Africana Studies'),(2,'American Studies'),(3,'Anthropology'),(4,'Arabic'),(5,'Art Department'),(6,'Art History'),(7,'Art-Studio'),(8,'Astronomy'),(9,'Biochemistry'),(10,'Biological Sciences'),(11,'Chemistry'),(12,'Chinese Language and Culture'),(13,'Cinema and Media Studies'),(14,'Classical Civilization'),(15,'Classical Studies Department'),(16,'Cognitive and Linguistic Sci'),(17,'Comparative Literature'),(18,'Computer Science'),(19,'East Asian Languages and Cultures'),(20,'Economics'),(21,'Education'),(22,'Engineering'),(23,'English'),(24,'Environmental Studies'),(25,'French'),(26,'Geosciences'),(27,'German'),(28,'Greek'),(29,'Hindi/Urdu'),(30,'History'),(31,'Italian Studies'),(32,'Japanese Language and Culture'),(33,'Jewish Studies'),(34,'Korean Language and Culture'),(35,'Latin'),(36,'Latin American Studies'),(37,'Linguistics'),(38,'Mathematics'),(39,'Media Arts & Sciences'),(40,'Medieval/Ren Studies'),(41,'Middle Eastern Studies'),(42,'Music'),(43,'Neuroscience'),(44,'Peace and Justice Studies'),(45,'Philosophy'),(46,'Physical Education'),(47,'Physics'),(48,'Political Science'),(49,'Portuguese'),(50,'Psychology'),(51,'Quantitative Reasoning'),(52,'Religion'),(53,'Russian'),(54,'Russian Area Studies'),(55,'Sociology'),(56,'South Asia Studies Program'),(57,'Spanish'),(58,'Statistics'),(59,'Theatre Studies'),(60,'Women\'s and Gender Studies'),(61,'Writing');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `picfile`
--

DROP TABLE IF EXISTS `picfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `picfile` (
  `uid` int(11) NOT NULL,
  `filename` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`uid`),
  CONSTRAINT `picfile_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `picfile`
--

LOCK TABLES `picfile` WRITE;
/*!40000 ALTER TABLE `picfile` DISABLE KEYS */;
/*!40000 ALTER TABLE `picfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `professor`
--

DROP TABLE IF EXISTS `professor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `professor` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`pid`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `professor_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `department` (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `professor`
--

LOCK TABLES `professor` WRITE;
/*!40000 ALTER TABLE `professor` DISABLE KEYS */;
INSERT INTO `professor` VALUES (1,'Scott Anderson',18),(2,'Peter Mawhorter',18),(3,'Brian Brubach',18),(4,'Alexa VanHattum',18),(5,'Smaranda Sandu',18),(6,'Catherine Delcourt',18),(7,'Christine Bassem',18),(8,'Franklyn Turbak',18),(9,'Yaniv Yacoby',18),(10,'Eni Mustafaraj',18),(11,'Vinitha Gadiraju',18),(12,'Orit Shaer',18),(13,'Brian Tjaden',18),(14,'Stella Kakavouli',18),(15,'Carolyn Anderson',18),(16,'Sohie Lee',18),(17,'Sara Melnick',18),(18,'Panagiotis Metaxas',18),(19,'Jordan Tynes',18),(22,'Andrew Davis',18),(23,'Adam Weiner',53),(24,'Hora Mishra',8),(25,'Alla Lvovna',53);
/*!40000 ALTER TABLE `professor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `review` (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `difficulty` enum('Easy','Medium','Hard') DEFAULT NULL,
  `credit` enum('Credit','Credit-Non','Mandatory Credit-Non') DEFAULT NULL,
  `prof_name` varchar(40) DEFAULT NULL,
  `prof_id` int(11) DEFAULT NULL,
  `prof_rating` enum('1','2','3','4','5') DEFAULT NULL,
  `sem` enum('Fall','Winter','Spring','Summer') DEFAULT NULL,
  `year` char(4) DEFAULT NULL,
  `take_again` enum('Yes','No') DEFAULT NULL,
  `load_heavy` enum('Light','Medium','Heavy') DEFAULT NULL,
  `office_hours` enum('Always Available','Sometimes Available','Never Available','Need to Schedule') DEFAULT NULL,
  `helped_learn` enum('Yes','No') DEFAULT NULL,
  `stim_interest` enum('Yes','No') DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `last_updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`rid`),
  KEY `course_id` (`course_id`),
  KEY `user_id` (`user_id`),
  KEY `prof_id` (`prof_id`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`cid`),
  CONSTRAINT `review_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`uid`),
  CONSTRAINT `review_ibfk_3` FOREIGN KEY (`prof_id`) REFERENCES `professor` (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES (2,4,1,'Medium','Credit','Smaranda Sandu',5,'5','Spring','2021','Yes','Medium','Sometimes Available','Yes','Yes','Kinda confusing but very interesting! Get ready to go to office hours.','2024-12-04 15:59:04'),(3,6,1,'Medium','Credit','Scott Anderson',NULL,'5','Fall','2024','Yes','Medium','Sometimes Available','Yes','Yes','I learned a lot about mysql and web development!','2024-11-06 00:39:09'),(4,3,1,'Hard','Credit','Brian Brubach',NULL,'4','Spring','2023','No','Heavy','Sometimes Available','Yes','Yes','Very difficult. Made me rethink the major.','2024-11-06 01:01:06'),(5,1,1,'Medium','Mandatory Credit-Non','Andrew Davis',22,'5','Fall','2021','Yes','Medium','Sometimes Available','Yes','Yes','Prof. Davis\'s class made me love coding! Take this class asap!! ','2024-11-06 13:31:30'),(6,5,1,'Hard','Credit','Alexa VanHattum',4,'5','Fall','2023','Yes','Heavy','Sometimes Available','Yes','Yes','The course is pretty difficult but you learn a lot of important information about systems. ','2024-11-06 13:35:18'),(7,2,1,'Hard','Credit','Catherine Delcourt',6,'4','Fall','2022','No','Heavy','Sometimes Available','Yes','Yes','Big jump from CS111','2024-11-09 14:55:19'),(8,7,1,'Medium','Credit','Adam Weiner',23,'4','Spring','2023','Yes','Medium','Need to Schedule','Yes','Yes','Lots of readings but they are interesting. My favorite book that we read in this class is The Brothers Karamazov!','2024-11-21 17:21:36'),(14,8,1,'Medium','Credit','Christine Bassem',7,'5','Fall','2023','Yes','Medium','Sometimes Available','Yes','Yes','It was really cool to learn about networks and protocols. I think this class is important for all CS majors to take. ','2024-11-21 17:29:26'),(15,2,1,'Hard','Credit','Catherine Delcourt',1,'4','Spring','2024','No','Heavy','Sometimes Available','Yes','Yes','Why do we have to learn Java?','2024-12-03 15:36:54');
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `profile_pic` varchar(100) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Vaishu Chintam',NULL,'jc103@wellesley.edu','password'),(2,'Mukhlisa Nematova',NULL,'mn109@wellesley.edu','password'),(3,'Kathy Yang',NULL,'ky107@wellesley.edu','password'),(5,'default_user',NULL,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-04 14:15:11
