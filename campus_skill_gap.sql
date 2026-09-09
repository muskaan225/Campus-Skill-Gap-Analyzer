-- MySQL dump 10.13  Distrib 9.6.0, for macos15.7 (arm64)
--
-- Host: localhost    Database: campus_skill_gap
-- ------------------------------------------------------
-- Server version	9.6.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--


--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'Placement Admin','admin@gmail.com','admin123');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assessment_results`
--

DROP TABLE IF EXISTS `assessment_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assessment_results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `career_id` int NOT NULL,
  `match_percentage` decimal(5,2) NOT NULL,
  `assessment_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `career_id` (`career_id`),
  CONSTRAINT `assessment_results_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
  CONSTRAINT `assessment_results_ibfk_2` FOREIGN KEY (`career_id`) REFERENCES `careers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessment_results`
--

LOCK TABLES `assessment_results` WRITE;
/*!40000 ALTER TABLE `assessment_results` DISABLE KEYS */;
INSERT INTO `assessment_results` VALUES (1,2,1,67.00,'2026-09-04 10:54:19'),(2,2,4,71.00,'2026-09-04 11:03:53'),(3,2,6,60.00,'2026-09-06 04:31:38'),(4,2,1,56.00,'2026-09-06 04:37:10'),(5,2,1,67.00,'2026-09-06 04:49:01'),(6,2,1,56.00,'2026-09-06 05:00:55'),(7,2,1,56.00,'2026-09-06 05:05:32'),(8,2,1,78.00,'2026-09-06 05:30:37'),(9,2,1,44.00,'2026-09-06 05:45:16'),(10,2,1,67.00,'2026-09-08 06:05:47'),(11,2,1,67.00,'2026-09-08 06:07:22');
/*!40000 ALTER TABLE `assessment_results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `career_skills`
--

DROP TABLE IF EXISTS `career_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `career_skills` (
  `id` int NOT NULL AUTO_INCREMENT,
  `career_id` int NOT NULL,
  `skill_id` int NOT NULL,
  `required_level` varchar(50) DEFAULT 'Intermediate',
  PRIMARY KEY (`id`),
  UNIQUE KEY `career_id` (`career_id`,`skill_id`),
  KEY `skill_id` (`skill_id`),
  CONSTRAINT `career_skills_ibfk_1` FOREIGN KEY (`career_id`) REFERENCES `careers` (`id`),
  CONSTRAINT `career_skills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `career_skills`
--

LOCK TABLES `career_skills` WRITE;
/*!40000 ALTER TABLE `career_skills` DISABLE KEYS */;
INSERT INTO `career_skills` VALUES (1,1,20,'Intermediate'),(2,1,18,'Intermediate'),(3,1,4,'Intermediate'),(4,1,16,'Intermediate'),(5,1,2,'Intermediate'),(6,1,17,'Intermediate'),(7,1,19,'Intermediate'),(8,1,1,'Intermediate'),(9,1,9,'Intermediate'),(16,2,6,'Intermediate'),(17,2,16,'Intermediate'),(18,2,5,'Intermediate'),(19,2,7,'Intermediate'),(20,2,10,'Intermediate'),(21,2,8,'Intermediate'),(22,2,9,'Intermediate'),(23,3,11,'Advanced'),(24,3,12,'Intermediate'),(25,3,1,'Intermediate'),(26,3,9,'Intermediate'),(27,3,13,'Intermediate'),(30,4,18,'Intermediate'),(31,4,16,'Intermediate'),(32,4,2,'Intermediate'),(33,4,10,'Intermediate'),(34,4,17,'Intermediate'),(35,4,1,'Intermediate'),(36,4,9,'Intermediate'),(37,5,15,'Intermediate'),(38,5,14,'Intermediate'),(39,5,1,'Intermediate'),(40,5,9,'Intermediate'),(41,5,13,'Intermediate'),(44,6,6,'Intermediate'),(45,6,16,'Intermediate'),(46,6,5,'Intermediate'),(47,6,7,'Intermediate'),(48,6,8,'Intermediate');
/*!40000 ALTER TABLE `career_skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `careers`
--

DROP TABLE IF EXISTS `careers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `careers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `career_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `career_name` (`career_name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `careers`
--

LOCK TABLES `careers` WRITE;
/*!40000 ALTER TABLE `careers` DISABLE KEYS */;
INSERT INTO `careers` VALUES (4,'Backend Developer'),(7,'Business Analyst'),(3,'Data Analyst'),(5,'Data Scientist'),(2,'Full Stack Developer'),(1,'Software Developer'),(6,'Web Developer');
/*!40000 ALTER TABLE `careers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skills`
--

DROP TABLE IF EXISTS `skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skills` (
  `id` int NOT NULL AUTO_INCREMENT,
  `skill_name` varchar(100) NOT NULL,
  `category` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `skill_name` (`skill_name`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skills`
--

LOCK TABLES `skills` WRITE;
/*!40000 ALTER TABLE `skills` DISABLE KEYS */;
INSERT INTO `skills` VALUES (1,'Python','Programming'),(2,'Java','Programming'),(3,'C++','Programming'),(4,'DSA','Programming'),(5,'HTML','Web Development'),(6,'CSS','Web Development'),(7,'JavaScript','Web Development'),(8,'React','Web Development'),(9,'SQL','Database'),(10,'MongoDB','Database'),(11,'Excel','Data Analytics'),(12,'Power BI','Data Analytics'),(13,'Statistics','Data Analytics'),(14,'Pandas','Data Science'),(15,'Machine Learning','Data Science'),(16,'Git & GitHub','Tools'),(17,'OOP','Core Computer Science'),(18,'DBMS','Core Computer Science'),(19,'Operating Systems','Core Computer Science'),(20,'Computer Networks','Core Computer Science');
/*!40000 ALTER TABLE `skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_skills`
--

DROP TABLE IF EXISTS `student_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_skills` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `skill_id` int NOT NULL,
  `proficiency` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_id` (`student_id`,`skill_id`),
  KEY `skill_id` (`skill_id`),
  CONSTRAINT `student_skills_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
  CONSTRAINT `student_skills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=261 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_skills`
--

LOCK TABLES `student_skills` WRITE;
/*!40000 ALTER TABLE `student_skills` DISABLE KEYS */;
INSERT INTO `student_skills` VALUES (241,2,1,'Intermediate'),(242,2,2,'Intermediate'),(243,2,3,'Beginner'),(244,2,4,'Beginner'),(245,2,5,'Intermediate'),(246,2,6,'Intermediate'),(247,2,7,'Beginner'),(248,2,8,'Beginner'),(249,2,9,'Intermediate'),(250,2,10,'Beginner'),(251,2,11,'Intermediate'),(252,2,12,'Beginner'),(253,2,13,'Beginner'),(254,2,14,'Beginner'),(255,2,15,'Beginner'),(256,2,16,'Intermediate'),(257,2,17,'Intermediate'),(258,2,18,'Intermediate'),(259,2,19,'Beginner'),(260,2,20,'Beginner');
/*!40000 ALTER TABLE `student_skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'sdfdf','sdsd@gmail.com','112343'),(2,'jennie','jennie@gmail.com','12345');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-08 12:46:01
