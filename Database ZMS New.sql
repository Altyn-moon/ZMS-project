-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: work_portal
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `documents`
--

DROP TABLE IF EXISTS `documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `work_card_id` int NOT NULL,
  `type` enum('Certificate','DRW','Instruction') NOT NULL,
  `number` varchar(100) DEFAULT NULL,
  `pdf_file` longblob NOT NULL,
  `url` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `operation_description_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_documents_work_card` (`work_card_id`),
  KEY `fk_documents_operation_description` (`operation_description_id`),
  CONSTRAINT `fk_documents_operation_description` FOREIGN KEY (`operation_description_id`) REFERENCES `operation_descriptions` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_documents_work_card` FOREIGN KEY (`work_card_id`) REFERENCES `work_cards` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents`
--

LOCK TABLES `documents` WRITE;
/*!40000 ALTER TABLE `documents` DISABLE KEYS */;
/*!40000 ALTER TABLE `documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operation_descriptions`
--

DROP TABLE IF EXISTS `operation_descriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operation_descriptions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `work_card_id` int NOT NULL COMMENT 'ссылка на work_cards',
  `operation` varchar(255) DEFAULT NULL COMMENT 'название операции',
  `equipment` varchar(255) DEFAULT NULL COMMENT 'оборудование',
  `user_id` int DEFAULT NULL COMMENT 'ответственный (users.id)',
  `documents_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `work_card_id` (`work_card_id`),
  KEY `responsible_user_id` (`user_id`),
  KEY `fk_operation_documents` (`documents_id`),
  CONSTRAINT `fk_operation_documents` FOREIGN KEY (`documents_id`) REFERENCES `documents` (`id`),
  CONSTRAINT `operation_descriptions_ibfk_1` FOREIGN KEY (`work_card_id`) REFERENCES `work_cards` (`id`),
  CONSTRAINT `operation_descriptions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operation_descriptions`
--

LOCK TABLES `operation_descriptions` WRITE;
/*!40000 ALTER TABLE `operation_descriptions` DISABLE KEYS */;
INSERT INTO `operation_descriptions` VALUES (1,1,'Производственная проверка','-----',2,NULL);
/*!40000 ALTER TABLE `operation_descriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `role` enum('admin','worker','inspector') NOT NULL,
  `login` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `uid` varchar(50) DEFAULT NULL,
  `job_title` varchar(100) DEFAULT NULL,
  `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=180 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Shagirova Arailym','admin','a.shagirova','Zms2025!','53 61 0E 4F','Координатор','2025-04-25 16:38:30'),(2,'Sabyrzhan Altynai','inspector','a.sabyrzhan','Zms2025!','91 41 0B 4F','Инспектор','2025-04-25 16:38:30'),(3,'Kenzhegali Asel','worker','a.kenzhegali','Zms2025!','1E A2 0D 4F','Оператор станка','2025-04-25 16:38:30'),(4,'Ibagaliev Aibolat','worker','a.ibagaliev','Zms2025!','AA 7F 00 64','Оператор станка','2025-05-21 14:37:23'),(5,'Berdigaliev Abilai','worker','a.berdigaliev','Zms2025!','BE BB C5 D4','Оператор станка','2025-05-21 14:37:23'),(6,'Yerbolatov Rauan','worker','r.yerbolatov','Zms2025!','77 94 0D 4F','Оператор станка','2025-05-21 14:37:23'),(7,'Igilikov Azamat','worker','a.igilikov','Zms2025!','5A B9 0B 4F','Оператор станка','2025-05-21 14:37:23'),(8,'Karataev Kuanish','worker','k.karataev','Zms2025!','29 71 ED BB','Оператор станка','2025-05-21 14:37:23'),(9,'Muslimov Aibek','worker','a.muslimov','Zms2025!','6A E3 17 64','Оператор станка','2025-05-21 14:37:23'),(10,'Sailauov Salaua','worker','s.sailauov','Zms2025!','CA EC 07 B5','Оператор станка','2025-05-21 14:37:23'),(11,'Saktaganov Oryngali','worker','o.saktaganov','Zms2025!','81 05 CA 93','Оператор станка','2025-05-21 14:37:23'),(12,'Tazhmuratov Bakyt','worker','b.tazhmuratov','Zms2025!','8A CC E6 63','Оператор станка','2025-05-21 14:37:23'),(13,'Abu Abzal','worker','a.abu','Zms2025!','FA F6 FD 63','Оператор станка','2025-05-21 14:37:23'),(14,'Otemisov Baktiyar','worker','b.otemisov','Zms2025!','BA 6D EC B4','Оператор станка','2025-05-21 14:37:23'),(15,'Sapanov Murat','worker','m.sapanov','Zms2025!','DA D4 12 B5','Оператор станка','2025-05-21 14:37:23'),(16,'Adilbaev Zhasulan','worker','z.adilbaev','Zms2025!','2E 2A C0 D4','Оператор станка','2025-05-21 14:37:23'),(17,'Balimov Zholzhan','worker','z.balimov','Zms2025!','6A 60 FE B4','Оператор станка','2025-05-21 14:37:23'),(18,'Yergaliev Amandyk','worker','a.yergaliev','Zms2025!','6A 22 02 B5','Оператор станка','2025-05-21 14:37:23'),(19,'Zhilkishiev Nurbulat','worker','n.zhilkishiev','Zms2025!','7A 25 0A B5','Оператор станка','2025-05-21 14:37:23'),(20,'Kuanbaev Asylbek','worker','a.kuanbaev','Zms2025!','AA 56 FB B4','Оператор станка','2025-05-21 14:37:23'),(21,'Mukashev Tynyshbek','worker','t.mukashev','Zms2025!','13 63 0B 4F','Оператор станка','2025-05-21 14:37:23'),(22,'Seitpeev Zhanibek','worker','z.seitpeev','Zms2025!','7A 2E 0D B5','Оператор станка','2025-05-21 14:37:23'),(23,'Andir Altynbek','worker','a.andir','Zms2025!','6B AD 0D 4F','Оператор станка','2025-05-21 14:37:23'),(24,'Bekturlin Zhanibek','worker','z.bekturlin','Zms2025!','75 78 0E 4F','Оператор станка','2025-05-21 14:37:23'),(25,'Alishev Alibek','worker','a.alishev','Zms2025!','3A 96 F2 B4','Оператор станка','2025-05-21 14:37:23'),(26,'Amankulov Targin','worker','t.amankulov','Zms2025!','BA A9 F6 63','Оператор станка','2025-05-21 14:37:23'),(27,'Bagitzhanov Berkhan','worker','b.bagitzhanov','Zms2025!','0A 11 E9 B4','Оператор станка','2025-05-21 14:37:23'),(28,'Zhurimbaev Erzhan','worker','e.zhurimbaev','Zms2025!','DA BA 08 64','Оператор станка','2025-05-21 14:37:23'),(29,'Isekenov Arystanbek','worker','a.isekenov','Zms2025!','FA DE 12 B5','Оператор станка','2025-05-21 14:37:23'),(30,'Kabdulov Asylan','worker','a.kabdulov','Zms2025!','BD 19 0B 4F','Оператор станка','2025-05-21 14:37:23'),(31,'Kaliyev Alikhan','worker','a.kaliyev','Zms2025!','DA C1 0C B5','Оператор станка','2025-05-21 14:37:23'),(32,'Mendigaliyev Zhumabek','worker','z.mendigaliyev','Zms2025!','9A 4A FD B4','Оператор станка','2025-05-21 14:37:23'),(33,'Rysbaev Nursultan','worker','n.rysbaev','Zms2025!','CC 6F 0E 4F','Оператор станка','2025-05-21 14:37:23'),(34,'Saparov Nurolla','worker','n.saparov','Zms2025!','32 25 0B 4F','Оператор станка','2025-05-21 14:37:23'),(35,'Satybaldy Adilzhan','worker','a.satybaldy','Zms2025!','26 8D 0D 4F','Оператор станка','2025-05-21 14:37:23'),(36,'Shubakov Sairan','worker','s.shubakov','Zms2025!','0E BC 0A 4F','Оператор станка','2025-05-21 14:37:23'),(37,'Kurmanov Anuar','worker','a.kurmanov','Zms2025!','30 14 0E 4F','Оператор станка','2025-05-21 14:37:23'),(38,'Gusmanov Bekbolat','worker','b.gusmanov','Zms2025!','83 7C 0E 4F','Оператор станка','2025-05-21 14:37:23');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `work_cards`
--

DROP TABLE IF EXISTS `work_cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `work_cards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `work_order_id` int NOT NULL COMMENT 'ссылка на work_orders',
  `title` varchar(255) NOT NULL COMMENT 'потребность или название',
  `material` text COMMENT 'материал',
  `cast_number` varchar(50) DEFAULT NULL COMMENT 'номер плавки',
  `user_id` int DEFAULT NULL,
  `documents_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `work_order_id` (`work_order_id`),
  KEY `fk_user_id` (`user_id`),
  KEY `fk_work_cards_documents` (`documents_id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_work_cards_documents` FOREIGN KEY (`documents_id`) REFERENCES `documents` (`id`) ON DELETE SET NULL,
  CONSTRAINT `work_cards_ibfk_1` FOREIGN KEY (`work_order_id`) REFERENCES `work_orders` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_cards`
--

LOCK TABLES `work_cards` WRITE;
/*!40000 ALTER TABLE `work_cards` DISABLE KEYS */;
INSERT INTO `work_cards` VALUES (1,1,'Изготовление переводников №1','Сталь AISI 4145 H Mod','9266, 9890',NULL,NULL),(2,1,'Изготовление переводников №2','Сталь AISI 4145 H Mod','B 74701',NULL,NULL);
/*!40000 ALTER TABLE `work_cards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `work_orders`
--

DROP TABLE IF EXISTS `work_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `work_orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `work_number` varchar(100) DEFAULT NULL,
  `work_date` date DEFAULT NULL,
  `work_revision` varchar(50) DEFAULT NULL,
  `work_order_number` varchar(100) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `prepared_by` varchar(100) DEFAULT NULL,
  `quote_number` varchar(200) DEFAULT NULL,
  `customer` varchar(255) DEFAULT NULL,
  `ordered_by` varchar(100) DEFAULT NULL,
  `customer_po_number` varchar(100) DEFAULT NULL,
  `rig_number` varchar(100) DEFAULT NULL,
  `well_number` varchar(100) DEFAULT NULL,
  `q_ty` varchar(50) DEFAULT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `serial_number` varchar(100) DEFAULT NULL,
  `job_description` text,
  `job_number` varchar(100) DEFAULT NULL,
  `job_date` date DEFAULT NULL,
  `job_revision` varchar(50) DEFAULT NULL,
  `grease_number` varchar(100) DEFAULT NULL,
  `protector_number` varchar(100) DEFAULT NULL,
  `request_number` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_orders`
--

LOCK TABLES `work_orders` WRITE;
/*!40000 ALTER TABLE `work_orders` DISABLE KEYS */;
INSERT INTO `work_orders` VALUES (1,1,'2025-05-15 11:59:54','ZMS-TH-QP-101-F-002','2025-05-15','Рев.00','1135-24','2025-05-15','2025-05-16','Жексенов Д.Е.','1135-24 Rev.0','ТОО\"Сервисноебуровое предприятие\"','Мукашов Аслан','SLSMRW002036','Нет','Нет','2','шт.','Переводник 165','1135-1,1135-2','Предоставить материал сталь 4145 и изготовить переводник 165 по чертежу 7196.00.000 и нарезать резьбовое соединение','ZMS-TH-QP-101-QCP-002-F-001','2025-05-15','Рев.00','CMTSP002628','---','SLSMRW002036'),(2,1,'2025-05-16 12:10:47','апсирольбд','2025-05-16','01','0','2025-05-16','2025-05-17','Алтын','0','ТШО','пмирто','0','0','0','1','шт','апмриол','0','рногшждльроипеакуы','самперноглшдж','2025-05-16','00','0','0','0');
/*!40000 ALTER TABLE `work_orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `work_times`
--

DROP TABLE IF EXISTS `work_times`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `work_times` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT 'кто работал (users.id)',
  `operation_description_id` int NOT NULL COMMENT 'ссылка на операцию',
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `duration_minutes` int GENERATED ALWAYS AS (timestampdiff(MINUTE,`start_time`,`end_time`)) STORED,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `operation_description_id` (`operation_description_id`),
  CONSTRAINT `work_times_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `work_times_ibfk_2` FOREIGN KEY (`operation_description_id`) REFERENCES `operation_descriptions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_times`
--

LOCK TABLES `work_times` WRITE;
/*!40000 ALTER TABLE `work_times` DISABLE KEYS */;
INSERT INTO `work_times` (`id`, `user_id`, `operation_description_id`, `start_time`, `end_time`) VALUES (3,2,1,'2025-04-28 08:00:00','2025-04-28 10:30:00');
/*!40000 ALTER TABLE `work_times` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-22 10:14:32
