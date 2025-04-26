-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: mydatabase
-- ------------------------------------------------------
-- Server version	8.0.41

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

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('d3d26bf18989');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_access_log`
--

DROP TABLE IF EXISTS `api_access_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_access_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `endpoint` varchar(255) DEFAULT NULL,
  `method` varchar(10) DEFAULT NULL,
  `status_code` int DEFAULT NULL,
  `auth_result` enum('success','fail') DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `api_access_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_access_log`
--

LOCK TABLES `api_access_log` WRITE;
/*!40000 ALTER TABLE `api_access_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_access_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enterprise`
--

DROP TABLE IF EXISTS `enterprise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enterprise` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enterprise`
--

LOCK TABLES `enterprise` WRITE;
/*!40000 ALTER TABLE `enterprise` DISABLE KEYS */;
INSERT INTO `enterprise` VALUES (1,'Paie&RH'),(2,'BoardRiders');
/*!40000 ALTER TABLE `enterprise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incident_log`
--

DROP TABLE IF EXISTS `incident_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incident_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `reported_by` int DEFAULT NULL,
  `message` text,
  `error_type` varchar(255) DEFAULT NULL,
  `status` enum('open','resolved') DEFAULT NULL,
  `resolution_notes` text,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reported_by` (`reported_by`),
  CONSTRAINT `incident_log_ibfk_1` FOREIGN KEY (`reported_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incident_log`
--

LOCK TABLES `incident_log` WRITE;
/*!40000 ALTER TABLE `incident_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `incident_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `content` text,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ticket_id` (`ticket_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`id`),
  CONSTRAINT `message_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (1,1,2,'test','2025-04-24 17:26:09');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model_version`
--

DROP TABLE IF EXISTS `model_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `model_version` (
  `id` int NOT NULL AUTO_INCREMENT,
  `version_tag` varchar(50) DEFAULT NULL,
  `description` text,
  `accuracy` float DEFAULT NULL,
  `trained_on` datetime DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `version_tag` (`version_tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_version`
--

LOCK TABLES `model_version` WRITE;
/*!40000 ALTER TABLE `model_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `model_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monitoring_metric`
--

DROP TABLE IF EXISTS `monitoring_metric`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monitoring_metric` (
  `id` int NOT NULL AUTO_INCREMENT,
  `model_version_id` int DEFAULT NULL,
  `metric_name` varchar(255) DEFAULT NULL,
  `value` float DEFAULT NULL,
  `recorded_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `model_version_id` (`model_version_id`),
  CONSTRAINT `monitoring_metric_ibfk_1` FOREIGN KEY (`model_version_id`) REFERENCES `model_version` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monitoring_metric`
--

LOCK TABLES `monitoring_metric` WRITE;
/*!40000 ALTER TABLE `monitoring_metric` DISABLE KEYS */;
/*!40000 ALTER TABLE `monitoring_metric` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prediction`
--

DROP TABLE IF EXISTS `prediction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prediction` (
  `id` int NOT NULL AUTO_INCREMENT,
  `message_id` int DEFAULT NULL,
  `sentiment` enum('positive','neutral','negative') DEFAULT NULL,
  `confidence` float DEFAULT NULL,
  `model_version_id` int DEFAULT NULL,
  `predicted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `message_id` (`message_id`),
  KEY `model_version_id` (`model_version_id`),
  CONSTRAINT `prediction_ibfk_1` FOREIGN KEY (`message_id`) REFERENCES `message` (`id`),
  CONSTRAINT `prediction_ibfk_2` FOREIGN KEY (`model_version_id`) REFERENCES `model_version` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prediction`
--

LOCK TABLES `prediction` WRITE;
/*!40000 ALTER TABLE `prediction` DISABLE KEYS */;
/*!40000 ALTER TABLE `prediction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `retraining_log`
--

DROP TABLE IF EXISTS `retraining_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `retraining_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `model_version_id` int DEFAULT NULL,
  `triggered_by` int DEFAULT NULL,
  `log` text,
  `status` enum('success','failed','pending') DEFAULT NULL,
  `started_at` datetime DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `model_version_id` (`model_version_id`),
  KEY `triggered_by` (`triggered_by`),
  CONSTRAINT `retraining_log_ibfk_1` FOREIGN KEY (`model_version_id`) REFERENCES `model_version` (`id`),
  CONSTRAINT `retraining_log_ibfk_2` FOREIGN KEY (`triggered_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retraining_log`
--

LOCK TABLES `retraining_log` WRITE;
/*!40000 ALTER TABLE `retraining_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `retraining_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_case`
--

DROP TABLE IF EXISTS `test_case`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_case` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_run_id` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `result` enum('pass','fail') DEFAULT NULL,
  `details` text,
  PRIMARY KEY (`id`),
  KEY `test_run_id` (`test_run_id`),
  CONSTRAINT `test_case_ibfk_1` FOREIGN KEY (`test_run_id`) REFERENCES `test_run` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_case`
--

LOCK TABLES `test_case` WRITE;
/*!40000 ALTER TABLE `test_case` DISABLE KEYS */;
/*!40000 ALTER TABLE `test_case` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_run`
--

DROP TABLE IF EXISTS `test_run`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_run` (
  `id` int NOT NULL AUTO_INCREMENT,
  `run_date` datetime DEFAULT NULL,
  `result` enum('pass','fail') DEFAULT NULL,
  `triggered_by` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `triggered_by` (`triggered_by`),
  CONSTRAINT `test_run_ibfk_1` FOREIGN KEY (`triggered_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_run`
--

LOCK TABLES `test_run` WRITE;
/*!40000 ALTER TABLE `test_run` DISABLE KEYS */;
/*!40000 ALTER TABLE `test_run` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket` (
  `id` int NOT NULL AUTO_INCREMENT,
  `subject` text,
  `status` enum('open','closed','pending') DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES (1,'Retard','open',2,'2025-04-24 17:26:09');
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_user`
--

DROP TABLE IF EXISTS `ticket_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_user` (
  `ticket_id` int NOT NULL,
  `user_id` int NOT NULL,
  `role` varchar(50) DEFAULT NULL,
  `joined_at` datetime DEFAULT NULL,
  PRIMARY KEY (`ticket_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `ticket_user_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`id`),
  CONSTRAINT `ticket_user_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_user`
--

LOCK TABLES `ticket_user` WRITE;
/*!40000 ALTER TABLE `ticket_user` DISABLE KEYS */;
INSERT INTO `ticket_user` VALUES (1,2,'creator','2025-04-24 17:26:09');
/*!40000 ALTER TABLE `ticket_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `enterprise_id` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('user','admin') DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `enterprise_id` (`enterprise_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`enterprise_id`) REFERENCES `enterprise` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,1,'Shaney Carrere','carrereshaney@hotmail.com','scrypt:32768:8:1$4doZI8NT5OnHG84S$871e07b7cb006fadc7d1a103257b278356ddf9005d3364bd92339e84db1a6024a9c5d1303356b5be75255d0122775e48cd1e5f87afc0d2f3e34a9035dc6146c2','admin',1,'2025-04-24 10:57:09'),(2,2,'Mathieu','mathieu@test.com','scrypt:32768:8:1$tqHI8VNnQAqDRKsM$32cbbaaae66d13dc4baa01501fe7e2f6419914b8581f067a3c26f822f7605a88b7f1c700b6bfea285faa7293b13420f802d4e344ee6e886bfe345d3c8ac6ab82','user',1,'2025-04-24 11:42:48');
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

-- Dump completed on 2025-04-25 11:14:10
