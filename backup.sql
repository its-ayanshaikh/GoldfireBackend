-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: localhost    Database: goldfire_db
-- ------------------------------------------------------
-- Server version	8.0.44-0ubuntu0.22.04.2

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
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) NOT NULL,
  `branch_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `accounts_user_branch_id_38ec6caf_fk_company_branch_id` (`branch_id`),
  CONSTRAINT `accounts_user_branch_id_38ec6caf_fk_company_branch_id` FOREIGN KEY (`branch_id`) REFERENCES `company_branch` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$1000000$HCklUedp1GrRkwC4lz71hP$ZCR7srcKZbSb4ibGWaf2x9Ys13//BSVtit0tYs1ih44=','2026-01-20 08:10:36.248351',1,'admin','','','',1,1,'2026-01-05 19:20:08.214008','',NULL),(2,'pbkdf2_sha256$1000000$drdGcHtmSlickGhA597asT$VSP012JbfPI1zZ1CLBMGd9fWNu0iH8RmrKT0jTBpwbM=','2026-01-21 12:46:28.402535',0,'riyaz','','','',0,1,'2026-01-05 19:20:47.341033','admin',NULL),(17,'pbkdf2_sha256$1000000$VVoCVW5HvlM7ZZJFPmX1MP$um/KSYuDbbS4TRqf+e/w0btKE1zfFkECg49D1cUbnx0=','2026-01-16 09:00:54.933723',0,'8849422705','','','SAHIKHASAD859@gmail.com',0,1,'2026-01-08 07:02:40.380352','employee',2),(18,'pbkdf2_sha256$1000000$sT3ksW0oLxyrQ1lX42cEgq$gTWMDD5SiS2U22hMHp7QxCG6N9D6dUkH5lnHcmjqXrc=','2026-01-23 07:17:25.550924',0,'7862903286','','','NK6356014@gmail.com',0,1,'2026-01-08 07:02:40.716405','employee',2),(19,'pbkdf2_sha256$1000000$j5pCsWoAIKahbUt0G0KWik$ujhkiRJDk36TiB77qIpL7DZzMEKr59ay+wHUVk8FR5U=','2026-01-11 07:36:11.621621',0,'9316125344','','','FS2277837@gmail.com',0,1,'2026-01-08 07:02:40.995719','employee',3),(20,'pbkdf2_sha256$1000000$9CvDkapPzrzH0HSXzEvfUR$vD/9JjuBUa/vP90k2LbT9YoD4HxOSVZ4GNj6i9K/HMQ=','2026-01-16 11:55:06.154605',0,'7433995507','','','ADNANWARSI5507@gmail.com',0,1,'2026-01-08 07:02:41.241525','employee',1),(21,'pbkdf2_sha256$1000000$aGElshXZV0GoV1PXaPKV60$f83Cy1pHsQMOZoO9w9BSNis8NKFziPD/OPIOaW96BSQ=','2026-01-11 07:36:44.182860',0,'9106604285','','','SAIYEDRUSHAN476@gmail.com',0,1,'2026-01-08 07:02:41.487967','employee',1),(22,'pbkdf2_sha256$1000000$Wl7kslXXzyeVYUo83dPGB5$G1Zyr0/H1NGfOlnDk36LkOMCA69am7DQDfHmLsAE8tg=','2026-01-11 10:18:46.187846',0,'9998738361','','','AFVANSHAIKH55@gmail.com',0,1,'2026-01-08 07:02:41.825019','employee',2),(23,'pbkdf2_sha256$1000000$p042uEdXAFnv5mKkhUcTgv$yBaDKj5gmY0w3eOqp9/APmtk3Kusu0c6PtsLmH6ZogA=','2026-01-12 11:29:20.586714',0,'9104260308','','','AMANKHALANI786@gmail.com',0,1,'2026-01-08 07:02:42.112962','employee',3),(24,'pbkdf2_sha256$1000000$TbooAr5wXnwUQmfdaA5CF6$q4NDDDvKUJv0xXNvoYkC8haLNpaqeVrIDukfhAfZGnc=','2026-01-17 10:47:33.295230',0,'8141505049','','','SHAIKHMASOOMALI2@gmail,com',0,1,'2026-01-08 07:02:42.372107','employee',1),(25,'pbkdf2_sha256$1000000$wCpKRWy7jtjgIVEUOTWMPB$faDZGcGmYmmbLTQASFyc+6hntuYeEnCy0PTQI8warzM=','2026-01-11 08:00:49.053307',0,'6351951725','','','HASANSHAIKH7668@gmail.com',0,1,'2026-01-08 07:02:42.628116','employee',1),(26,'pbkdf2_sha256$1000000$xrXj0Jils7iigPbgR6n8fh$rAujiyOzkVQcTvqNJ6BnRUg9DBquvz10nqg8W/H77/0=','2026-01-11 11:55:21.436731',0,'8200159741','','','PATHANSAKIBKHAN@gmail.com',0,1,'2026-01-08 07:02:42.899386','employee',2),(27,'pbkdf2_sha256$1000000$dYWeomq1pRXUoKj1Tw4tWy$IFju9yJAaZcI9bCtNVXJgNEwy87LRtU0p5UJuQe/880=','2026-01-11 13:26:32.543197',0,'9664551270','','','SHAIKH.AK1999@gmail.com',0,1,'2026-01-08 07:02:43.156169','employee',1),(28,'pbkdf2_sha256$1000000$EFEQnf1PV2cSsoAkbzP9ou$UXp6wITF1HAxK9Qu3lp5HUq3sN4dhmlNnDsOH+0e9f8=','2026-01-12 19:09:27.399475',0,'816068529','','','SC8160608529@gmail.com',0,1,'2026-01-08 07:02:43.418419','employee',1),(29,'pbkdf2_sha256$1000000$07lD9gSMOPlcNBE1IYEprX$F5lScwaDhHJFDxYnUhlpOQazDcCoLl1z5/0y1kHpciQ=','2026-01-18 06:06:49.354282',0,'9824041586','','','MINIG9898@gmail.com',0,1,'2026-01-08 07:02:43.677177','employee',3),(30,'pbkdf2_sha256$1000000$bRfMomVhsSMNyCphUzQujo$AuWTg7a0X6kS2Uy4XLT6Afz357aC/Un1T5WR7pQYn2s=','2026-01-18 06:08:51.499428',0,'gf_jamalpur','','','',0,1,'2026-01-08 08:03:17.938065','cashier',1);
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=193 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add company',6,'add_company'),(22,'Can change company',6,'change_company'),(23,'Can delete company',6,'delete_company'),(24,'Can view company',6,'view_company'),(25,'Can add branch',7,'add_branch'),(26,'Can change branch',7,'change_branch'),(27,'Can delete branch',7,'delete_branch'),(28,'Can view branch',7,'view_branch'),(29,'Can add role',8,'add_role'),(30,'Can change role',8,'change_role'),(31,'Can delete role',8,'delete_role'),(32,'Can view role',8,'view_role'),(33,'Can add employee',9,'add_employee'),(34,'Can change employee',9,'change_employee'),(35,'Can delete employee',9,'delete_employee'),(36,'Can view employee',9,'view_employee'),(37,'Can add attendance',10,'add_attendance'),(38,'Can change attendance',10,'change_attendance'),(39,'Can delete attendance',10,'delete_attendance'),(40,'Can view attendance',10,'view_attendance'),(41,'Can add leave',11,'add_leave'),(42,'Can change leave',11,'change_leave'),(43,'Can delete leave',11,'delete_leave'),(44,'Can view leave',11,'view_leave'),(45,'Can add leave swap request',12,'add_leaveswaprequest'),(46,'Can change leave swap request',12,'change_leaveswaprequest'),(47,'Can delete leave swap request',12,'delete_leaveswaprequest'),(48,'Can view leave swap request',12,'view_leaveswaprequest'),(49,'Can add monthly leave request',13,'add_monthlyleaverequest'),(50,'Can change monthly leave request',13,'change_monthlyleaverequest'),(51,'Can delete monthly leave request',13,'delete_monthlyleaverequest'),(52,'Can view monthly leave request',13,'view_monthlyleaverequest'),(53,'Can add monthly leave item',14,'add_monthlyleaveitem'),(54,'Can change monthly leave item',14,'change_monthlyleaveitem'),(55,'Can delete monthly leave item',14,'delete_monthlyleaveitem'),(56,'Can view monthly leave item',14,'view_monthlyleaveitem'),(57,'Can add paid leave request',15,'add_paidleaverequest'),(58,'Can change paid leave request',15,'change_paidleaverequest'),(59,'Can delete paid leave request',15,'delete_paidleaverequest'),(60,'Can view paid leave request',15,'view_paidleaverequest'),(61,'Can add salary',16,'add_salary'),(62,'Can change salary',16,'change_salary'),(63,'Can delete salary',16,'delete_salary'),(64,'Can view salary',16,'view_salary'),(65,'Can add sales commission',17,'add_salescommission'),(66,'Can change sales commission',17,'change_salescommission'),(67,'Can delete sales commission',17,'delete_salescommission'),(68,'Can view sales commission',17,'view_salescommission'),(69,'Can add category',18,'add_category'),(70,'Can change category',18,'change_category'),(71,'Can delete category',18,'delete_category'),(72,'Can view category',18,'view_category'),(73,'Can add commission',19,'add_commission'),(74,'Can change commission',19,'change_commission'),(75,'Can delete commission',19,'delete_commission'),(76,'Can view commission',19,'view_commission'),(77,'Can add model',20,'add_model'),(78,'Can change model',20,'change_model'),(79,'Can delete model',20,'delete_model'),(80,'Can view model',20,'view_model'),(81,'Can add quantity',21,'add_quantity'),(82,'Can change quantity',21,'change_quantity'),(83,'Can delete quantity',21,'delete_quantity'),(84,'Can view quantity',21,'view_quantity'),(85,'Can add rack',22,'add_rack'),(86,'Can change rack',22,'change_rack'),(87,'Can delete rack',22,'delete_rack'),(88,'Can view rack',22,'view_rack'),(89,'Can add serial number',23,'add_serialnumber'),(90,'Can change serial number',23,'change_serialnumber'),(91,'Can delete serial number',23,'delete_serialnumber'),(92,'Can view serial number',23,'view_serialnumber'),(93,'Can add sub brand',24,'add_subbrand'),(94,'Can change sub brand',24,'change_subbrand'),(95,'Can delete sub brand',24,'delete_subbrand'),(96,'Can view sub brand',24,'view_subbrand'),(97,'Can add sub category',25,'add_subcategory'),(98,'Can change sub category',25,'change_subcategory'),(99,'Can delete sub category',25,'delete_subcategory'),(100,'Can view sub category',25,'view_subcategory'),(101,'Can add type',26,'add_type'),(102,'Can change type',26,'change_type'),(103,'Can delete type',26,'delete_type'),(104,'Can view type',26,'view_type'),(105,'Can add brand',27,'add_brand'),(106,'Can change brand',27,'change_brand'),(107,'Can delete brand',27,'delete_brand'),(108,'Can view brand',27,'view_brand'),(109,'Can add hsn',28,'add_hsn'),(110,'Can change hsn',28,'change_hsn'),(111,'Can delete hsn',28,'delete_hsn'),(112,'Can view hsn',28,'view_hsn'),(113,'Can add product',29,'add_product'),(114,'Can change product',29,'change_product'),(115,'Can delete product',29,'delete_product'),(116,'Can view product',29,'view_product'),(117,'Can add task',30,'add_task'),(118,'Can change task',30,'change_task'),(119,'Can delete task',30,'delete_task'),(120,'Can view task',30,'view_task'),(121,'Can add task submission',31,'add_tasksubmission'),(122,'Can change task submission',31,'change_tasksubmission'),(123,'Can delete task submission',31,'delete_tasksubmission'),(124,'Can view task submission',31,'view_tasksubmission'),(125,'Can add task image',32,'add_taskimage'),(126,'Can change task image',32,'change_taskimage'),(127,'Can delete task image',32,'delete_taskimage'),(128,'Can view task image',32,'view_taskimage'),(129,'Can add purchase',33,'add_purchase'),(130,'Can change purchase',33,'change_purchase'),(131,'Can delete purchase',33,'delete_purchase'),(132,'Can view purchase',33,'view_purchase'),(133,'Can add vendor',34,'add_vendor'),(134,'Can change vendor',34,'change_vendor'),(135,'Can delete vendor',34,'delete_vendor'),(136,'Can view vendor',34,'view_vendor'),(137,'Can add purchase receipt',35,'add_purchasereceipt'),(138,'Can change purchase receipt',35,'change_purchasereceipt'),(139,'Can delete purchase receipt',35,'delete_purchasereceipt'),(140,'Can view purchase receipt',35,'view_purchasereceipt'),(141,'Can add vendor return monthly',36,'add_vendorreturnmonthly'),(142,'Can change vendor return monthly',36,'change_vendorreturnmonthly'),(143,'Can delete vendor return monthly',36,'delete_vendorreturnmonthly'),(144,'Can view vendor return monthly',36,'view_vendorreturnmonthly'),(145,'Can add user',37,'add_user'),(146,'Can change user',37,'change_user'),(147,'Can delete user',37,'delete_user'),(148,'Can view user',37,'view_user'),(149,'Can add customer',38,'add_customer'),(150,'Can change customer',38,'change_customer'),(151,'Can delete customer',38,'delete_customer'),(152,'Can view customer',38,'view_customer'),(153,'Can add payment',39,'add_payment'),(154,'Can change payment',39,'change_payment'),(155,'Can delete payment',39,'delete_payment'),(156,'Can view payment',39,'view_payment'),(157,'Can add product transfer',40,'add_producttransfer'),(158,'Can change product transfer',40,'change_producttransfer'),(159,'Can delete product transfer',40,'delete_producttransfer'),(160,'Can view product transfer',40,'view_producttransfer'),(161,'Can add replacement bill',41,'add_replacementbill'),(162,'Can change replacement bill',41,'change_replacementbill'),(163,'Can delete replacement bill',41,'delete_replacementbill'),(164,'Can view replacement bill',41,'view_replacementbill'),(165,'Can add replacement item',42,'add_replacementitem'),(166,'Can change replacement item',42,'change_replacementitem'),(167,'Can delete replacement item',42,'delete_replacementitem'),(168,'Can view replacement item',42,'view_replacementitem'),(169,'Can add replacement payment',43,'add_replacementpayment'),(170,'Can change replacement payment',43,'change_replacementpayment'),(171,'Can delete replacement payment',43,'delete_replacementpayment'),(172,'Can view replacement payment',43,'view_replacementpayment'),(173,'Can add replacement refund',44,'add_replacementrefund'),(174,'Can change replacement refund',44,'change_replacementrefund'),(175,'Can delete replacement refund',44,'delete_replacementrefund'),(176,'Can view replacement refund',44,'view_replacementrefund'),(177,'Can add return bill',45,'add_returnbill'),(178,'Can change return bill',45,'change_returnbill'),(179,'Can delete return bill',45,'delete_returnbill'),(180,'Can view return bill',45,'view_returnbill'),(181,'Can add return item',46,'add_returnitem'),(182,'Can change return item',46,'change_returnitem'),(183,'Can delete return item',46,'delete_returnitem'),(184,'Can view return item',46,'view_returnitem'),(185,'Can add bill',47,'add_bill'),(186,'Can change bill',47,'change_bill'),(187,'Can delete bill',47,'delete_bill'),(188,'Can view bill',47,'view_bill'),(189,'Can add bill item',48,'add_billitem'),(190,'Can change bill item',48,'change_billitem'),(191,'Can delete bill item',48,'delete_billitem'),(192,'Can view bill item',48,'view_billitem');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company_branch`
--

DROP TABLE IF EXISTS `company_branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_branch` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `address` longtext,
  `phone` varchar(20) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `gst` varchar(50) DEFAULT NULL,
  `last_bill_number` int unsigned NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `company_id` bigint NOT NULL,
  `latitude` varchar(15) DEFAULT NULL,
  `longitude` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `company_branch_company_id_80c2a051_fk_company_company_id` (`company_id`),
  CONSTRAINT `company_branch_company_id_80c2a051_fk_company_company_id` FOREIGN KEY (`company_id`) REFERENCES `company_company` (`id`),
  CONSTRAINT `company_branch_chk_1` CHECK ((`last_bill_number` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_branch`
--

LOCK TABLES `company_branch` WRITE;
/*!40000 ALTER TABLE `company_branch` DISABLE KEYS */;
INSERT INTO `company_branch` VALUES (1,'JAMALPUR','JAMALPUR','9874563211',NULL,'24COOPG1950F1Z3',0,'active','2026-01-05 19:23:10.910746',1,'23.0130647','72.5819066'),(2,'ROYAL AKBAR','ROYAL AKBAR, SARKHEJ','1234567890',NULL,'24ATTPG1992R2ZQ',0,'active','2026-01-05 19:23:51.795776',1,'22.99344','72.52396'),(3,'SARKHEJ','SARKHEJ','9874562311',NULL,'24ATTPG1992R2ZQ',0,'active','2026-01-05 19:24:06.742894',1,'22.987736','72.511671'),(4,'JAMALPUR GROUND','NEAR JAMALPUR DARVAJA','9924722619','','',0,'active','2026-01-19 13:17:49.826523',1,'','');
/*!40000 ALTER TABLE `company_branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company_company`
--

DROP TABLE IF EXISTS `company_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_company` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `address` longtext,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_company`
--

LOCK TABLES `company_company` WRITE;
/*!40000 ALTER TABLE `company_company` DISABLE KEYS */;
INSERT INTO `company_company` VALUES (1,'GOLDFIRE','','9924722619',NULL,'2026-01-05 19:23:03.791092');
/*!40000 ALTER TABLE `company_company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=158 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-01-05 19:20:50.916883','2','riyaz (admin)',1,'[{\"added\": {}}]',37,1),(2,'2026-01-05 19:23:03.793087','1','GOLDFIRE',1,'[{\"added\": {}}]',6,1),(3,'2026-01-05 19:25:51.155709','1','Cover',1,'[{\"added\": {}}]',18,1),(4,'2026-01-05 19:26:02.341910','2','Glass',1,'[{\"added\": {}}]',18,1),(5,'2026-01-05 19:26:44.783563','3','Earphone',1,'[{\"added\": {}}]',18,1),(6,'2026-01-05 19:26:50.094902','4','Headphone',1,'[{\"added\": {}}]',18,1),(7,'2026-01-05 19:26:59.028596','5','Buds',1,'[{\"added\": {}}]',18,1),(8,'2026-01-05 19:27:03.293069','6','Charger',1,'[{\"added\": {}}]',18,1),(9,'2026-01-05 19:27:10.703696','7','Powerbank',1,'[{\"added\": {}}]',18,1),(10,'2026-01-05 19:27:15.081521','8','Speaker',1,'[{\"added\": {}}]',18,1),(11,'2026-01-05 19:27:27.162646','9','Lamination',1,'[{\"added\": {}}]',18,1),(12,'2026-01-05 19:27:32.894566','10','Stand',1,'[{\"added\": {}}]',18,1),(13,'2026-01-05 19:27:39.080758','11','Cabel',1,'[{\"added\": {}}]',18,1),(14,'2026-01-05 19:28:09.690023','2','Tuffun',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',18,1),(15,'2026-01-05 19:28:26.597115','7','Power Bank',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',18,1),(16,'2026-01-05 19:28:44.047444','12','Wireless Charger',1,'[{\"added\": {}}]',18,1),(17,'2026-01-05 19:29:00.753893','13','Watch',1,'[{\"added\": {}}]',18,1),(18,'2026-01-05 19:29:10.072444','14','Pencil',1,'[{\"added\": {}}]',18,1),(19,'2026-01-05 19:29:14.339885','15','Keyboard',1,'[{\"added\": {}}]',18,1),(20,'2026-01-05 19:29:18.878177','16','Camera Ring',1,'[{\"added\": {}}]',18,1),(21,'2026-01-05 19:29:28.041245','17','Watch Belt',1,'[{\"added\": {}}]',18,1),(22,'2026-01-05 19:29:32.462468','18','Water Pouch',1,'[{\"added\": {}}]',18,1),(23,'2026-01-05 19:29:41.353537','19','Magsafe Accesories',1,'[{\"added\": {}}]',18,1),(24,'2026-01-06 08:40:52.023843','2','ROYAL AKBAR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(25,'2026-01-06 09:43:57.287994','1','Phone (Cover)',1,'[{\"added\": {}}]',25,1),(26,'2026-01-06 09:44:06.525771','2','Charger (Cover)',1,'[{\"added\": {}}]',25,1),(27,'2026-01-06 09:44:16.478201','3','Buds (Cover)',1,'[{\"added\": {}}]',25,1),(28,'2026-01-06 09:44:21.113505','4','Tablet (Cover)',1,'[{\"added\": {}}]',25,1),(29,'2026-01-06 09:44:26.541723','5','Watch (Cover)',1,'[{\"added\": {}}]',25,1),(30,'2026-01-06 09:44:38.228763','6','Laptop (Cover)',1,'[{\"added\": {}}]',25,1),(31,'2026-01-06 09:44:50.660287','7','Phone (Tuffun)',1,'[{\"added\": {}}]',25,1),(32,'2026-01-06 09:44:56.233901','8','Tablet (Tuffun)',1,'[{\"added\": {}}]',25,1),(33,'2026-01-06 09:45:01.195437','9','Watch (Tuffun)',1,'[{\"added\": {}}]',25,1),(34,'2026-01-06 09:45:19.580078','10','Wired (Earphone)',1,'[{\"added\": {}}]',25,1),(35,'2026-01-06 09:45:25.201521','11','Wireless (Tuffun)',1,'[{\"added\": {}}]',25,1),(36,'2026-01-06 09:45:36.066784','12','Wired (Headphone)',1,'[{\"added\": {}}]',25,1),(37,'2026-01-06 09:45:46.057784','13','Wireless (Earphone)',1,'[{\"added\": {}}]',25,1),(38,'2026-01-06 09:46:03.502675','14','Phone (Charger)',1,'[{\"added\": {}}]',25,1),(39,'2026-01-06 09:46:10.373810','15','Watch (Charger)',1,'[{\"added\": {}}]',25,1),(40,'2026-01-06 09:46:15.600776','16','Car (Charger)',1,'[{\"added\": {}}]',25,1),(41,'2026-01-06 09:46:26.507658','17','Wirelss (Charger)',1,'[{\"added\": {}}]',25,1),(42,'2026-01-06 09:46:32.950137','18','All in one (Charger)',1,'[{\"added\": {}}]',25,1),(43,'2026-01-06 09:46:57.658730','19','Wired (Power Bank)',1,'[{\"added\": {}}]',25,1),(44,'2026-01-06 09:47:04.982522','20','Wireless (Power Bank)',1,'[{\"added\": {}}]',25,1),(45,'2026-01-06 09:47:23.767655','21','Wired (Speaker)',1,'[{\"added\": {}}]',25,1),(46,'2026-01-06 09:47:32.767421','22','Wireless (Speaker)',1,'[{\"added\": {}}]',25,1),(47,'2026-01-06 09:47:49.432237','23','Glossy (Lamination)',1,'[{\"added\": {}}]',25,1),(48,'2026-01-06 09:47:58.650931','24','Matt (Lamination)',1,'[{\"added\": {}}]',25,1),(49,'2026-01-06 09:48:06.602827','25','Privacy (Lamination)',1,'[{\"added\": {}}]',25,1),(50,'2026-01-06 09:48:24.493932','26','Auto Repair (Lamination)',1,'[{\"added\": {}}]',25,1),(51,'2026-01-06 09:48:30.748646','27','Print (Lamination)',1,'[{\"added\": {}}]',25,1),(52,'2026-01-06 09:48:42.191185','28','Leather (Lamination)',1,'[{\"added\": {}}]',25,1),(53,'2026-01-06 09:48:51.544058','29','Leather Print (Lamination)',1,'[{\"added\": {}}]',25,1),(54,'2026-01-06 09:49:06.734657','30','Laptop (Lamination)',1,'[{\"added\": {}}]',25,1),(55,'2026-01-06 09:49:14.798753','31','Transperent (Lamination)',1,'[{\"added\": {}}]',25,1),(56,'2026-01-06 09:49:28.762536','32','Table (Stand)',1,'[{\"added\": {}}]',25,1),(57,'2026-01-06 09:49:36.037338','33','Car (Stand)',1,'[{\"added\": {}}]',25,1),(58,'2026-01-06 09:49:46.747836','34','Bike (Stand)',1,'[{\"added\": {}}]',25,1),(59,'2026-01-06 09:49:58.082254','35','Activa (Stand)',1,'[{\"added\": {}}]',25,1),(60,'2026-01-06 09:50:05.478749','36','Tripod (Stand)',1,'[{\"added\": {}}]',25,1),(61,'2026-01-06 09:50:21.633289','37','Type C (Cabel)',1,'[{\"added\": {}}]',25,1),(62,'2026-01-06 09:50:41.417685','38','V8 (Cabel)',1,'[{\"added\": {}}]',25,1),(63,'2026-01-06 09:51:10.489663','39','Lightning (Cabel)',1,'[{\"added\": {}}]',25,1),(64,'2026-01-06 09:51:23.459279','40','All in one (Cabel)',1,'[{\"added\": {}}]',25,1),(65,'2026-01-06 09:51:29.087270','41','C To C (Cabel)',1,'[{\"added\": {}}]',25,1),(66,'2026-01-06 09:51:41.314377','42','USB To C (Cabel)',1,'[{\"added\": {}}]',25,1),(67,'2026-01-06 09:52:08.200350','43','Silicon (Watch Belt)',1,'[{\"added\": {}}]',25,1),(68,'2026-01-06 09:52:14.175244','44','Loop (Watch Belt)',1,'[{\"added\": {}}]',25,1),(69,'2026-01-06 09:52:26.823839','45','Welcrow (Watch Belt)',1,'[{\"added\": {}}]',25,1),(70,'2026-01-06 09:52:42.393559','46','Leather (Watch Belt)',1,'[{\"added\": {}}]',25,1),(71,'2026-01-06 09:52:49.689638','47','Chain (Watch Belt)',1,'[{\"added\": {}}]',25,1),(72,'2026-01-06 09:53:00.898800','48','Magnetic Silicon (Watch Belt)',1,'[{\"added\": {}}]',25,1),(73,'2026-01-06 09:53:52.057548','49','Magnetic Chain (Watch Belt)',1,'[{\"added\": {}}]',25,1),(74,'2026-01-06 09:54:02.871840','50','Ceramic (Watch Belt)',1,'[{\"added\": {}}]',25,1),(75,'2026-01-06 09:54:32.493383','51','Normal (Camera Ring)',1,'[{\"added\": {}}]',25,1),(76,'2026-01-06 09:54:40.212842','52','Diamond (Camera Ring)',1,'[{\"added\": {}}]',25,1),(77,'2026-01-06 09:54:46.666975','53','Football (Camera Ring)',1,'[{\"added\": {}}]',25,1),(78,'2026-01-06 09:54:59.564783','54','Wired (Pencil)',1,'[{\"added\": {}}]',25,1),(79,'2026-01-06 09:55:05.245892','55','Wireless (Pencil)',1,'[{\"added\": {}}]',25,1),(80,'2026-01-06 09:55:54.893999','56','Wired (Keyboard)',1,'[{\"added\": {}}]',25,1),(81,'2026-01-06 09:56:00.664988','57','Wireless (Keyboard)',1,'[{\"added\": {}}]',25,1),(82,'2026-01-06 09:56:16.436623','58','Leather Wallet (Magsafe Accesories)',1,'[{\"added\": {}}]',25,1),(83,'2026-01-06 09:56:29.376291','59','Pop Socket (Magsafe Accesories)',1,'[{\"added\": {}}]',25,1),(84,'2026-01-06 09:56:39.046964','60','Rings (Magsafe Accesories)',1,'[{\"added\": {}}]',25,1),(85,'2026-01-06 10:03:16.606725','2','ROYAL AKBAR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Longitude\"]}}]',7,1),(86,'2026-01-06 10:06:01.812562','2','ROYAL AKBAR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(87,'2026-01-06 10:21:38.035245','11','SAHNAWAZ MISTRY',3,'',9,1),(88,'2026-01-06 10:21:38.035245','10','PATHAN SAKIB KHAN',3,'',9,1),(89,'2026-01-06 10:21:38.035245','9','HASAN SHAIKH',3,'',9,1),(90,'2026-01-06 10:21:38.035245','8','SHAIKH MASOOM ALI ',3,'',9,1),(91,'2026-01-06 10:21:38.035245','7','AMAN KHALIANI',3,'',9,1),(92,'2026-01-06 10:21:38.035245','6','AFFAN SHAIKH',3,'',9,1),(93,'2026-01-06 10:21:38.035245','5','SAIYED RUSHAN',3,'',9,1),(94,'2026-01-06 10:21:38.035245','4','ADNAN WARSI .',3,'',9,1),(95,'2026-01-06 10:21:38.035245','3','FAIZAN SHAIKH',3,'',9,1),(96,'2026-01-06 10:21:38.035245','2','NIZAM KHAN',3,'',9,1),(97,'2026-01-06 10:21:38.036242','1','ASAD SHAIKH ',3,'',9,1),(98,'2026-01-08 10:22:26.907413','7','asd',3,'',29,1),(99,'2026-01-08 10:22:26.907444','6','Printer',3,'',29,1),(100,'2026-01-08 10:22:26.907457','5','Tranparent',3,'',29,1),(101,'2026-01-08 10:22:26.907467','4','TP',3,'',29,1),(102,'2026-01-08 10:22:26.907477','3','Transparent',3,'',29,1),(103,'2026-01-08 10:22:26.907487','2','Transparent',3,'',29,1),(104,'2026-01-08 10:22:26.907499','1','TPU',3,'',29,1),(105,'2026-01-08 10:50:22.913206','22','8504',3,'',28,1),(106,'2026-01-08 10:50:31.872434','21','8504',2,'[]',28,1),(107,'2026-01-08 11:59:00.029561','11','Cable',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',18,1),(108,'2026-01-08 12:03:31.734132','11','Samsung C To C 1.8Mtr',2,'[{\"changed\": {\"fields\": [\"Category\"]}}]',29,1),(109,'2026-01-08 12:03:42.668435','10','Samsung C To C Cable 1 Mtr',2,'[{\"changed\": {\"fields\": [\"Category\"]}}]',29,1),(110,'2026-01-08 12:03:48.728843','10','Samsung C To C Cable 1 Mtr',2,'[]',29,1),(111,'2026-01-08 12:18:38.170696','9','Samsung 25W Doc',2,'[{\"changed\": {\"fields\": [\"Category\"]}}]',29,1),(112,'2026-01-08 12:21:42.295496','11','Samsung C To C 1.8Mtr',2,'[{\"changed\": {\"fields\": [\"Category\"]}}]',29,1),(113,'2026-01-08 12:21:55.899588','10','Samsung C To C Cable 1 Mtr',2,'[{\"changed\": {\"fields\": [\"Category\"]}}]',29,1),(114,'2026-01-08 12:26:37.763831','11','Samsung C To C 1.8Mtr',2,'[{\"changed\": {\"fields\": [\"Subcategory\", \"Brand\"]}}]',29,1),(115,'2026-01-08 12:28:12.158591','11','Samsung C To C 1.8Mtr',3,'',29,1),(116,'2026-01-08 12:28:12.158648','10','Samsung C To C Cable 1 Mtr',3,'',29,1),(117,'2026-01-08 12:28:26.637867','13','Apple 30W Doc',2,'[{\"changed\": {\"fields\": [\"Category\"]}}]',29,1),(118,'2026-01-08 12:33:53.663102','14','Samsung C to C 1.8Mtr',2,'[{\"changed\": {\"name\": \"quantity\", \"object\": \"Samsung C to C 1.8Mtr - JAMALPUR\", \"fields\": [\"Barcode\"]}}]',29,1),(119,'2026-01-08 12:35:18.628124','14','Samsung C to C 1.8Mtr',2,'[{\"added\": {\"name\": \"serial number\", \"object\": \"Samsung C to C 1.8Mtr - R3V2LZ30VQKRT3\"}}]',29,1),(120,'2026-01-08 12:35:28.579379','14','Samsung C to C 1.8Mtr',2,'[{\"changed\": {\"name\": \"quantity\", \"object\": \"Samsung C to C 1.8Mtr - JAMALPUR\", \"fields\": [\"Qty\"]}}]',29,1),(121,'2026-01-08 12:39:11.266466','15','Samsung C to C 1Mtr',2,'[{\"changed\": {\"name\": \"quantity\", \"object\": \"Samsung C to C 1Mtr - JAMALPUR\", \"fields\": [\"Barcode\"]}}]',29,1),(122,'2026-01-08 12:49:16.427132','8','Apple 20W Doc',2,'[{\"changed\": {\"fields\": [\"Category\"]}}]',29,1),(123,'2026-01-08 13:25:58.324255','21','JT301 Type C',3,'',29,1),(124,'2026-01-08 13:30:45.984808','23','JT301 USB To C',2,'[{\"changed\": {\"name\": \"quantity\", \"object\": \"JT301 USB To C - JAMALPUR\", \"fields\": [\"Barcode\"]}}]',29,1),(125,'2026-01-08 13:31:54.708191','18','B11 C To C 65W 2Mtr',2,'[{\"changed\": {\"fields\": [\"Subcategory\"]}}]',29,1),(126,'2026-01-08 13:32:22.891906','15','Samsung C to C 1Mtr',2,'[{\"changed\": {\"fields\": [\"Subcategory\"]}}]',29,1),(127,'2026-01-08 13:32:43.615795','14','Samsung C to C 1.8Mtr',2,'[{\"changed\": {\"fields\": [\"Subcategory\"]}}]',29,1),(128,'2026-01-08 13:32:54.088436','18','B11 C To C 65W 2Mtr',2,'[]',29,1),(129,'2026-01-08 13:57:39.060521','16','Apple 35W Adapter',2,'[{\"added\": {\"name\": \"serial number\", \"object\": \"Apple 35W Adapter - C4H512001Q71VHJAV\"}}]',29,1),(130,'2026-01-08 13:58:12.576507','16','Apple 35W Adapter',2,'[{\"changed\": {\"name\": \"quantity\", \"object\": \"Apple 35W Adapter - JAMALPUR\", \"fields\": [\"Qty\"]}}]',29,1),(131,'2026-01-09 11:35:30.836307','24','SHAIKH ADNAN - 2026-01-09',2,'[{\"changed\": {\"fields\": [\"Login time\"]}}]',10,1),(132,'2026-01-09 11:37:09.806223','24','SHAIKH ADNAN - 2026-01-09',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',10,1),(133,'2026-01-10 07:09:21.562438','3','SARKHEJ (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(134,'2026-01-10 08:15:04.939331','37','SHAIKH ADNAN - 2026-01-10',2,'[{\"changed\": {\"fields\": [\"Login time\", \"Login image\", \"Status\"]}}]',10,1),(135,'2026-01-10 08:15:20.382875','24','SHAIKH ADNAN - 2026-01-09',2,'[{\"changed\": {\"fields\": [\"Login time\", \"Logout time\", \"Status\"]}}]',10,1),(136,'2026-01-10 08:15:29.679468','24','SHAIKH ADNAN - 2026-01-09',2,'[{\"changed\": {\"fields\": [\"Total hours\"]}}]',10,1),(137,'2026-01-10 08:15:40.122016','24','SHAIKH ADNAN - 2026-01-09',2,'[]',10,1),(138,'2026-01-10 08:17:35.705186','2','ROYAL AKBAR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(139,'2026-01-10 08:22:32.922368','3','SARKHEJ (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(140,'2026-01-11 11:51:51.006685','2','ROYAL AKBAR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(141,'2026-01-11 12:00:19.308991','2','ROYAL AKBAR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(142,'2026-01-11 13:48:51.663181','17','8849422705 (employee) - ROYAL AKBAR',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',37,1),(143,'2026-01-11 13:49:49.840439','17','8849422705 (employee) - ROYAL AKBAR',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',37,1),(144,'2026-01-11 13:56:33.860083','17','8849422705 (employee) - ROYAL AKBAR',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',37,1),(145,'2026-01-11 13:57:08.584047','19','9316125344 (employee) - SARKHEJ',2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',37,1),(146,'2026-01-12 12:03:52.615436','1','JAMALPUR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(147,'2026-01-12 19:02:55.057382','1','JAMALPUR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(148,'2026-01-12 19:07:45.388567','1','JAMALPUR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(149,'2026-01-12 19:25:56.026219','57','SAHNAWAZ MISTRY - 2026-01-12',3,'',10,1),(150,'2026-01-12 19:26:30.871618','1','JAMALPUR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(151,'2026-01-16 11:21:45.519953','1','JAMALPUR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(152,'2026-01-16 11:52:10.039073','1','JAMALPUR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(153,'2026-01-16 11:52:45.439874','1','JAMALPUR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(154,'2026-01-16 11:53:31.825246','1','JAMALPUR (GOLDFIRE)',2,'[{\"changed\": {\"fields\": [\"Latitude\", \"Longitude\"]}}]',7,1),(155,'2026-01-16 11:53:59.905689','107','ADNAN WARSI . - 2026-01-16',2,'[{\"changed\": {\"fields\": [\"Login time\", \"Login image\", \"Status\"]}}]',10,1),(156,'2026-01-16 11:55:44.510353','107','ADNAN WARSI . - 2026-01-16',2,'[{\"changed\": {\"fields\": [\"Logout time\", \"Logout image\"]}}]',10,1),(157,'2026-01-21 11:29:18.957914','76','JTP-A13',2,'[{\"changed\": {\"name\": \"quantity\", \"object\": \"JTP-A13 - JAMALPUR GROUND\", \"fields\": [\"Barcode\"]}}]',29,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (37,'accounts','user'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(7,'company','branch'),(6,'company','company'),(4,'contenttypes','contenttype'),(10,'employee','attendance'),(9,'employee','employee'),(11,'employee','leave'),(12,'employee','leaveswaprequest'),(14,'employee','monthlyleaveitem'),(13,'employee','monthlyleaverequest'),(15,'employee','paidleaverequest'),(8,'employee','role'),(16,'employee','salary'),(17,'employee','salescommission'),(47,'pos','bill'),(48,'pos','billitem'),(38,'pos','customer'),(39,'pos','payment'),(40,'pos','producttransfer'),(41,'pos','replacementbill'),(42,'pos','replacementitem'),(43,'pos','replacementpayment'),(44,'pos','replacementrefund'),(45,'pos','returnbill'),(46,'pos','returnitem'),(27,'product','brand'),(18,'product','category'),(19,'product','commission'),(28,'product','hsn'),(20,'product','model'),(29,'product','product'),(21,'product','quantity'),(22,'product','rack'),(23,'product','serialnumber'),(24,'product','subbrand'),(25,'product','subcategory'),(26,'product','type'),(5,'sessions','session'),(30,'task','task'),(32,'task','taskimage'),(31,'task','tasksubmission'),(33,'vendor','purchase'),(35,'vendor','purchasereceipt'),(34,'vendor','vendor'),(36,'vendor','vendorreturnmonthly');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'company','0001_initial','2026-01-05 19:19:08.939233'),(2,'contenttypes','0001_initial','2026-01-05 19:19:09.095492'),(3,'contenttypes','0002_remove_content_type_name','2026-01-05 19:19:09.298613'),(4,'auth','0001_initial','2026-01-05 19:19:10.189235'),(5,'auth','0002_alter_permission_name_max_length','2026-01-05 19:19:10.392363'),(6,'auth','0003_alter_user_email_max_length','2026-01-05 19:19:10.408066'),(7,'auth','0004_alter_user_username_opts','2026-01-05 19:19:10.439243'),(8,'auth','0005_alter_user_last_login_null','2026-01-05 19:19:10.454867'),(9,'auth','0006_require_contenttypes_0002','2026-01-05 19:19:10.454867'),(10,'auth','0007_alter_validators_add_error_messages','2026-01-05 19:19:10.486113'),(11,'auth','0008_alter_user_username_max_length','2026-01-05 19:19:10.501748'),(12,'auth','0009_alter_user_last_name_max_length','2026-01-05 19:19:10.517366'),(13,'auth','0010_alter_group_name_max_length','2026-01-05 19:19:10.564256'),(14,'auth','0011_update_proxy_permissions','2026-01-05 19:19:10.595497'),(15,'auth','0012_alter_user_first_name_max_length','2026-01-05 19:19:10.611115'),(16,'accounts','0001_initial','2026-01-05 19:19:11.642362'),(17,'admin','0001_initial','2026-01-05 19:19:11.986109'),(18,'admin','0002_logentry_remove_auto_add','2026-01-05 19:19:12.017365'),(19,'admin','0003_logentry_add_action_flag_choices','2026-01-05 19:19:12.064239'),(20,'employee','0001_initial','2026-01-05 19:19:15.111115'),(21,'product','0001_initial','2026-01-05 19:19:16.501737'),(22,'pos','0001_initial','2026-01-05 19:19:17.204864'),(23,'pos','0002_initial','2026-01-05 19:19:22.346009'),(24,'vendor','0001_initial','2026-01-05 19:19:23.455382'),(25,'product','0002_initial','2026-01-05 19:19:26.830389'),(26,'sessions','0001_initial','2026-01-05 19:19:26.908519'),(27,'task','0001_initial','2026-01-05 19:19:27.877255'),(28,'company','0002_branch_lattitude_branch_longitude','2026-01-06 07:24:24.244860'),(29,'company','0003_alter_branch_lattitude_alter_branch_longitude','2026-01-06 07:51:31.184680'),(30,'company','0004_alter_branch_lattitude_alter_branch_longitude','2026-01-06 07:54:41.278918'),(31,'company','0005_rename_lattitude_branch_latitude','2026-01-06 07:57:02.484311'),(32,'company','0006_alter_branch_latitude_alter_branch_longitude','2026-01-06 08:17:29.063027'),(33,'employee','0002_alter_employee_working_hours','2026-01-06 10:21:53.227496');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('045h1zhqeyw5b5tup4il832xiny63zqm','.eJxVjEEOwiAQAP_C2RCW2AU8evcNZGEXqRqalPZk_Lsh6UGvM5N5q0j7VuPeZY0zq4uyRp1-YaL8lDYMP6jdF52Xtq1z0iPRh-36trC8rkf7N6jU6_iCOPJUhGySgKEIJ0tecEI0yOJSYGvFARQ_ATC4sw3oMRGTAZ_V5wsmbzhr:1vepts:gfmyZ2vy_awxjfUZx7kV0D9Dml4AqFBmpJbBBZmn8Vg','2026-01-25 07:30:12.681961'),('0bpdytrq635g17z6a8wqrwjmw6pm0yxn','.eJxVjDsOAiEUAO9CbQifx8_Sfs9AgAeyaiBZdivj3Q3JFtrOTOZNfDj26o-RN78iuRJhyeUXxpCeuU2Dj9Dunabe9m2NdCb0tIMuHfPrdrZ_gxpGnV-RLThwAjk4jCkaA4JpBZIZQMWj5lrxIiyiVLIUk1DIAjzmohK3jHy-3xA3Sw:1vfNI7:DrOgAUhqRmDl0DRNsjzGARMC4kPJTHXjn1aKpetXb0c','2026-01-26 19:09:27.409232'),('0hy1nevi1zqc6m3qlq7rx52uxhcsp43y','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vd1RW:mXVEebm5amWzzWvQSkXijMt7NSLWaeTCKL_U1Nn_sOE','2026-01-20 07:25:26.836021'),('10zj461snynwo7unju18ezo1vji5j9fc','.eJxVjEEOwiAQRe_C2pBCYUCX7nsGAjODVA0kpV0Z765NutDtf-_9lwhxW0vYOi9hJnERSpx-txTxwXUHdI_11iS2ui5zkrsiD9rl1Iif18P9Oyixl28NqEknA2gpO_COUSFnlUYYICk_MPFIlKy2NsPZOMzKRAbrPTECZ_H-AP3AONQ:1vdbFT:d4rDVV7iR80-O0gohYfelwpg0rA1L7Te4MaIUQh8jck','2026-01-21 21:39:23.509783'),('11oeebb0twpg0itnr4va7h4bjb0nsv4u','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vd7ll:OCVy0D8M_8x-E7iEmc1xo6wV_6vVarZj8Bxyd6ypnS4','2026-01-20 14:10:45.743449'),('15envcnvr0guzry4yr6n1lgttf0iaxnc','.eJxVjEEOwiAQRe_C2pBCYUCX7nsGAjODVA0kpV0Z765NutDtf-_9lwhxW0vYOi9hJnERSpx-txTxwXUHdI_11iS2ui5zkrsiD9rl1Iif18P9Oyixl28NqEknA2gpO_COUSFnlUYYICk_MPFIlKy2NsPZOMzKRAbrPTECZ_H-AP3AONQ:1vfM1s:hWtN8e8dQkDbM-wBh6L-7uCz1ipaxaRtc0yhFo3EuNA','2026-01-26 17:48:36.644854'),('1c75tntrstfn32ezj3njzs8mipn55q1p','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vd2Tl:RZJKOgnyR-AOhzbILgpDBFaz8-M15c3jqRZ54VnwcV4','2026-01-20 08:31:49.766734'),('1ds4klx9a4i295h5waagf63xrqmbqkf1','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vevbe:jLvWcIXS5YebEfGCuWUidMPrJpwVjQRmiYXD82-lGiY','2026-01-25 13:35:46.114506'),('1m9r07cb14x7jl4c7lb5d263nfackdwv','.eJxVjDsOwjAQBe_iGlnrbzAlfc5g7ca7JIBsKZ8KcXeIlALaNzPvpTJu65i3hec8FXVRDtTpdyQcHlx3Uu5Yb00Pra7zRHpX9EEX3bfCz-vh_h2MuIzfegjRQuIg5JLxwXBKEjsCYW87HyShMyUSeWHCzrpoDZAIFrJg4Czq_QH_mTgt:1vhLxz:n_jzUt9xcywg8aHLJX-_tpNqSbwGG-IEUydSMMbOkxY','2026-02-01 06:08:51.513545'),('1ub27rfxnz6n6h9q288nwpisahx2zotg','.eJxVjEEOwiAQAP_C2RCW2AU8evcNZGEXqRqalPZk_Lsh6UGvM5N5q0j7VuPeZY0zq4uyRp1-YaL8lDYMP6jdF52Xtq1z0iPRh-36trC8rkf7N6jU6_iCOPJUhGySgKEIJ0tecEI0yOJSYGvFARQ_ATC4sw3oMRGTAZ_V5wsmbzhr:1vepte:wnddSCmSk6-DIF2WpCJExq7hrkQSl82fFNl2y4P4Isg','2026-01-25 07:29:58.324244'),('1vv9qzyp2kzeks4ue2bfek4mupqy4bxf','.eJxVjMsOwiAQRf-FtSE8ygAu3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmEtjpd0wxP6jtBO-x3TrPva3LnPiu8IMOfu1Iz8vh_h3UOOq3tpmk01GSyN6DLyJPNinrjNPekk65ONIClEEAQu0VyQKIairJkTCCvT8BSTfx:1vd8Zo:MvQYBletv8sXyc9eoFsZi0AJEg69MZKVvf-1pQIMBwU','2026-01-20 15:02:28.369999'),('2bcy1gv6p3fzjnr6c9x7kjlhbrlcxy6v','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vd1U1:ic24WWvoQa1-Lzjyd1wXo_fjLL3nHhsg5XAiV6pAndQ','2026-01-20 07:28:01.639247'),('2uwrosz2ho4maryu9a1x62e7yh6bq1yr','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vdbQ8:KBCrkRZL2L6xNFmGvcbzu8MpI7EYablZpTB6bIqhTU0','2026-01-21 21:50:24.518263'),('3frszllqfsw1wz56l7vojkdzvu3c1rjt','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vdmIB:0hewqg-FWeqa1Cmz4Kps_UDv4vV-R67TqQuef9-KUxY','2026-01-22 09:26:55.685870'),('3x16lx49c3fxt0t03avug4ismz32ku2r','.eJxVjEEOwiAQRe_C2pBCYUCX7nsGAjODVA0kpV0Z765NutDtf-_9lwhxW0vYOi9hJnERSpx-txTxwXUHdI_11iS2ui5zkrsiD9rl1Iif18P9Oyixl28NqEknA2gpO_COUSFnlUYYICk_MPFIlKy2NsPZOMzKRAbrPTECZ_H-AP3AONQ:1vdbr6:LwnwQsrUgMgUCGn_1HN6sKxuLp9WDbDfBzMm1qv5klM','2026-01-21 22:18:16.138143'),('4fte5r4zl8hm8o0aqrkur3ex1gasrsbz','.eJxVjEEOwiAQAP_C2RCW2AU8evcNZGEXqRqalPZk_Lsh6UGvM5N5q0j7VuPeZY0zq4uyRp1-YaL8lDYMP6jdF52Xtq1z0iPRh-36trC8rkf7N6jU6_iCOPJUhGySgKEIJ0tecEI0yOJSYGvFARQ_ATC4sw3oMRGTAZ_V5wsmbzhr:1vepz6:qk11Ri1E4A7CwWnIRXlLMXieqaRofLRFNxEJBDBCTzU','2026-01-25 07:35:36.295295'),('4pj79x081jy8f9d5oji5h9q1zlg7784u','.eJxVjEEOwiAQAP_C2RCW2AU8evcNZGEXqRqalPZk_Lsh6UGvM5N5q0j7VuPeZY0zq4uyRp1-YaL8lDYMP6jdF52Xtq1z0iPRh-36trC8rkf7N6jU6_iCOPJUhGySgKEIJ0tecEI0yOJSYGvFARQ_ATC4sw3oMRGTAZ_V5wsmbzhr:1veptn:xu61WqnOoUHBhHs-Eoaj-tx6ZoeaTFjw1c4IpJabimg','2026-01-25 07:30:07.191704'),('4xscb63043ginru1e8fgo47hr6jxcmd3','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vd9Lm:C4CXvM-l0UtKa9VOkHKpKdIO5kv3GY0zgR0mLPZXAQ8','2026-01-20 15:52:02.989389'),('56y56segrf5y2zshbaiw27q2e2dlnsml','.eJxVjDsOwjAQBe_iGln-LXEo6XMGy95d4wCypTipEHeHSCmgfTPzXiLEbS1h67yEmcRFmFGcfscU8cF1J3SP9dYktrouc5K7Ig_a5dSIn9fD_TsosZdvbR2RBoY8oPOok4KRtCKNPisPFhSp7NElOiODtgYQBq2MNRGZrUfx_gAHUDf2:1veAld:oH_ejIhXOWxfKbCwAP9q7irbBLGGlB4liAj04VThz14','2026-01-23 11:34:57.613410'),('60wf6llyxw2qazy7aq6zxv1kwad2ns41','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vdmI0:WMNaQ4kKQEpiRYGiZr-lZE-rlabz2m49MkxkumheU8U','2026-01-22 09:26:44.630818'),('65y3mzw13e96sv4u5ea13s0h1xr1m7cs','.eJxVjDsOwjAQBe_iGln-LXEo6XMGy95d4wCypTipEHeHSCmgfTPzXiLEbS1h67yEmcRFmFGcfscU8cF1J3SP9dYktrouc5K7Ig_a5dSIn9fD_TsosZdvbR2RBoY8oPOok4KRtCKNPisPFhSp7NElOiODtgYQBq2MNRGZrUfx_gAHUDf2:1veXbh:ZJJp-LxnexNSd1J-EJ4p0Y9tvWky7IxrhYlBzcwlUgA','2026-01-24 11:58:13.020040'),('6khxm9hwmbqr3n30vfpq9z3k1wkpy7ha','.eJxVjDsOwjAQBe_iGln-LXEo6XMGy95d4wCypTipEHeHSCmgfTPzXiLEbS1h67yEmcRFmFGcfscU8cF1J3SP9dYktrouc5K7Ig_a5dSIn9fD_TsosZdvbR2RBoY8oPOok4KRtCKNPisPFhSp7NElOiODtgYQBq2MNRGZrUfx_gAHUDf2:1veTEW:QeD2pPZRrzHtEZig8JxxtXAKR-ZwiA7d6zd86M-jBpU','2026-01-24 07:18:00.327056'),('6qhrukyytlq0z7a8pb71a8dbvlunnly7','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vdbOf:Q1bmAL2jg2Bz6V6ykWjtKZwmJtXZ-7O1EIrE3Bj3_mk','2026-01-21 21:48:53.448064'),('6spqwnpsautprjp1agvcznsi2gf832fc','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vd1IB:f4teFkTNElkPrdrjZgt8p_zRUCIvBRhXy286FmnFleM','2026-01-20 07:15:47.368687'),('71z3ja7q7axcltflvhcgjrryztmc9jz0','.eJxVjDsOwjAQBe_iGlm2s5vFlPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqL0CROv6Pn8Eh1J_HO9dZkaHVdZi93RR60y6nF9Lwe7t9B4V6-tQ9EyoLNORN6S4Rs4mgIUlaGtLWcBg-kPZrRIAfAAYyKCuA8IKIW7w_16DbE:1vdk42:wNZldEgr44X1Ck3bpp9UqGFAG1TwXy4lc9A2On2qY9E','2026-01-22 07:04:10.033996'),('7ilbffd1mqgugmeppuyddpfx57acw2b7','.eJxVjMsOwiAQRf-FtSE8ygAu3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmEtjpd0wxP6jtBO-x3TrPva3LnPiu8IMOfu1Iz8vh_h3UOOq3tpmk01GSyN6DLyJPNinrjNPekk65ONIClEEAQu0VyQKIairJkTCCvT8BSTfx:1vdbKe:9_1wpW-xnISAh2Y2NlJqVi2FFjIIfXI0soSrgqkNcAQ','2026-01-21 21:44:44.418169'),('7plzwlfsgxb5tbbq1fnin1iw1kjfdsra','.eJxVjMsOwiAQRf-FtSE8ygAu3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmEtjpd0wxP6jtBO-x3TrPva3LnPiu8IMOfu1Iz8vh_h3UOOq3tpmk01GSyN6DLyJPNinrjNPekk65ONIClEEAQu0VyQKIairJkTCCvT8BSTfx:1vd9QF:apZp1YoFTuW127A7HubxnuFX1LgFS5Gyot__HK5WSnE','2026-01-20 15:56:39.866938'),('7rnd4kzrxn0284wc7s0xc2j5w5ilvcxk','.eJxVjDsOwjAQRO_iGlnB_6Wk5wzWrtfGAeRIcVIh7k4ipYBuNO_NvEXEdalx7XmOI4uLUEqcfkvC9MxtJ_zAdp9kmtoyjyR3RR60y9vE-XU93L-Dir1ua1ApDYDERVEqllh77YLdomXmgtYCIDhmb8kE1EaBpoTow9kNBkB8vjYXOKw:1vesX0:w3iVDLRWQsMWLJmpZ3j0hr2bw9NfHVECQ_-ILoA4Qic','2026-01-25 10:18:46.195289'),('7wvcmwekvh359ab910doz2pg5h04uqrk','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vepor:dOe_aX8ucwYNpUle_2tmtXGLviBTT4NSxEQtKJ4HnpM','2026-01-25 07:25:01.460886'),('7zzr5iofct3md6a2hw1i2d31uuqcc1h5','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vd8Dy:mV6F1m8L9ZV5ar_GEZQ_fhhMPbTuD4Zsy7Y9igV9X60','2026-01-20 14:39:54.174926'),('8iawbnwmwze0xlt8qjvmpsa7lw0mmjvr','.eJxVjMsOwiAQRf-FtSE8ygAu3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmEtjpd0wxP6jtBO-x3TrPva3LnPiu8IMOfu1Iz8vh_h3UOOq3tpmk01GSyN6DLyJPNinrjNPekk65ONIClEEAQu0VyQKIairJkTCCvT8BSTfx:1vdA0f:XEaBkDPO32nraNfc3TWeZ4J6CCV2OSEBjNTnZNLR_Vo','2026-01-20 16:34:17.144524'),('8iq2u3gecmkmt5gcubf86vqfhqe0dsf0','.eJxVjEEOwiAQAP_C2RCW2AU8evcNZGEXqRqalPZk_Lsh6UGvM5N5q0j7VuPeZY0zq4uyRp1-YaL8lDYMP6jdF52Xtq1z0iPRh-36trC8rkf7N6jU6_iCOPJUhGySgKEIJ0tecEI0yOJSYGvFARQ_ATC4sw3oMRGTAZ_V5wsmbzhr:1vgiHn:k5Qki-7YxqziGDFvRRwnfk2OKahzDMyaTRVy__RSwpE','2026-01-30 11:46:39.859012'),('8m44mzkzuoweqnef52w2ubw10ye4n1dl','.eJxVjEEOwiAQRe_C2pDBFMq4dO8ZyAwDUjWQlHZlvLtt0oVu_3vvv1WgdSlh7WkOk6iLMqM6_Y5M8ZnqTuRB9d50bHWZJ9a7og_a9a1Jel0P9--gUC9bDczsz2QRrHFZJCcZYjSAGRxats4DD5JGoUgoEdDAJiFKHhiT9erzBSwiOTM:1vevt8:lS9vK92J50JbmN88JjC_XibPgNUwxpxGA0-SS_VKA1k','2026-01-25 13:53:50.473514'),('8mh06nwymjbj85oxgtuxx1i25mf8llj9','.eJxVjDsOwjAQBe_iGlnrbzAlfc5g7ca7JIBsKZ8KcXeIlALaNzPvpTJu65i3hec8FXVRDtTpdyQcHlx3Uu5Yb00Pra7zRHpX9EEX3bfCz-vh_h2MuIzfegjRQuIg5JLxwXBKEjsCYW87HyShMyUSeWHCzrpoDZAIFrJg4Czq_QH_mTgt:1venp3:kRQhRZv4wOcn6DCvAKPIYbrqIfuKWKxxEUAYg3qOINY','2026-01-25 05:17:05.921101'),('8otrg3arvvgcuxipkea0lyg7c1mfji9i','.eJxVjMEOwiAQRP-FsyF0u62LR-9-AwF2K1UDSWlPxn-XJj3o7WXmzbyV89ua3FZlcTOriwJUp98w-PiUvDf88PledCx5Xeagd0UfbdW3wvK6Hu7fQfI1tbWIgCUykQfANjsbw1PX0DRCwJEYJPaWEG2IYKDrpR-44YREMqrPF_8QN5o:1vh3q9:HfZ43nShPveewi9j4H183iGhRO8T3kRSNnCWPY-VVRE','2026-01-31 10:47:33.306640'),('9o057pff74akwk9fqedkh8oxwf54svnz','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vd2Yd:FH_qsMilDHEEjPake-KF5WxzDSQT8nYeUB9xl41QopA','2026-01-20 08:36:51.051018'),('a6dgu845upgwt2vhzsccgi9vp9tmksbu','.eJxVjEEOwiAQRe_C2pBCYUCX7nsGAjODVA0kpV0Z765NutDtf-_9lwhxW0vYOi9hJnERSpx-txTxwXUHdI_11iS2ui5zkrsiD9rl1Iif18P9Oyixl28NqEknA2gpO_COUSFnlUYYICk_MPFIlKy2NsPZOMzKRAbrPTECZ_H-AP3AONQ:1vcq7v:N1m3euo7XcrEWsS3D-oKzqhH9QF46fvt3W45Xx_Z2fM','2026-01-19 19:20:27.601483'),('ae5f32skkgkje2br823edgwt6xop353c','.eJxVjEEOwiAQRe_C2pBCYUCX7nsGAjODVA0kpV0Z765NutDtf-_9lwhxW0vYOi9hJnERSpx-txTxwXUHdI_11iS2ui5zkrsiD9rl1Iif18P9Oyixl28NqEknA2gpO_COUSFnlUYYICk_MPFIlKy2NsPZOMzKRAbrPTECZ_H-AP3AONQ:1vfN7Y:xw_1ORuTCrbfJprV49d8RHYWlioVnBWd7fsG9enGxzA','2026-01-26 18:58:32.592792'),('ccs7664ono8tym2nvtrmk5k1unkrve72','.eJxVjDsOwjAQBe_iGln-LXEo6XMGy95d4wCypTipEHeHSCmgfTPzXiLEbS1h67yEmcRFmFGcfscU8cF1J3SP9dYktrouc5K7Ig_a5dSIn9fD_TsosZdvbR2RBoY8oPOok4KRtCKNPisPFhSp7NElOiODtgYQBq2MNRGZrUfx_gAHUDf2:1vfwbt:YtHrt-gbIh9TPMAhMLMw_kHLxpI3X8aHktlz3yAbyoM','2026-01-28 08:52:13.250553'),('cty7daaqfo42c18c4tdduchgsuqw5s5l','.eJxVjEEOwiAQRe_C2hCGEWhduu8ZyDCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-juIiwInT7xiIH6nuJN6p3prkVtdlDnJX5EG7nFpMz-vh_h0U6uVba6UsOZWQsuGcjWI9EA4YABJEayPjGci6MYLSRCY7DoyEWRvkUSvx_gAI2jgQ:1vevoU:1sSCAuwq9dQmW-E6vGmUY2JofUym9dO5BSlZSluzQHM','2026-01-25 13:49:02.170185'),('d2iy08a8u8q181clchygmmntby9x3q5m','.eJxVjEEOwiAQRe_C2pBCYUCX7nsGAjODVA0kpV0Z765NutDtf-_9lwhxW0vYOi9hJnERSpx-txTxwXUHdI_11iS2ui5zkrsiD9rl1Iif18P9Oyixl28NqEknA2gpO_COUSFnlUYYICk_MPFIlKy2NsPZOMzKRAbrPTECZ_H-AP3AONQ:1vdnag:43fROHaItgpFkY0ss0srYOxF6xO3qcHnCb2_kOOfinY','2026-01-22 10:50:06.739999'),('dpu06e8xzdfxrhsvbu8adglmalw3rtqr','.eJxVjDsOwjAQBe_iGlnxdy1Kes5grddrHEC2FCcV4u4QKQW0b2beS0Tc1hq3wUucszgLFcTpd0xID247yXdsty6pt3WZk9wVedAhrz3z83K4fwcVR_3WRiUDBTxpJpgmZ5SCQOwDgEum2KAyoi6KXbHkQVuk5EiD5hRKNijeH_kFODU:1vjBQ5:V7Q5xZP3VB7urxvtEAMchanM3lWcK-qELrGa0_orIVU','2026-02-06 07:17:25.565718'),('du01xvloonniuodgt5u13i26mvnn0w2b','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1veSj2:PwoW1jQd35JRR50ozV7h0tlPh-Lchw01hDbKH2oX6n0','2026-01-24 06:45:28.700780'),('e1d0cxkiz0pyiqgp2zpoqzshjnpl1k3l','.eJxVjDsOwjAQBe_iGlnrbzAlfc5g7ca7JIBsKZ8KcXeIlALaNzPvpTJu65i3hec8FXVRDtTpdyQcHlx3Uu5Yb00Pra7zRHpX9EEX3bfCz-vh_h2MuIzfegjRQuIg5JLxwXBKEjsCYW87HyShMyUSeWHCzrpoDZAIFrJg4Czq_QH_mTgt:1vfgHu:2HI06AZmJeR3DzYu7ktxTjJEochgprqJOG785cN_AVc','2026-01-27 15:26:30.730236'),('ewfm36tpuolxdg5y5m4xir4meygpf5p9','.eJxVjMsOwiAQRf-FtSE8ygAu3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmEtjpd0wxP6jtBO-x3TrPva3LnPiu8IMOfu1Iz8vh_h3UOOq3tpmk01GSyN6DLyJPNinrjNPekk65ONIClEEAQu0VyQKIairJkTCCvT8BSTfx:1vd5u4:wnipL1LJ_c1yUr1cbgNH5mhS6XgMUX2IPr1XjDGhUek','2026-01-20 12:11:12.497747'),('ey69414c22xrsnw6f2vj24w5otp08qzs','.eJxVjEEOwiAQRe_C2pBCYUCX7nsGAjODVA0kpV0Z765NutDtf-_9lwhxW0vYOi9hJnERSpx-txTxwXUHdI_11iS2ui5zkrsiD9rl1Iif18P9Oyixl28NqEknA2gpO_COUSFnlUYYICk_MPFIlKy2NsPZOMzKRAbrPTECZ_H-AP3AONQ:1vd1my:GfeVmoA1KI5IT9KtlrfUSh2Rf6g6B5utFhJSFfRU61U','2026-01-20 07:47:36.005787'),('fn4cqd6ivwfpdy5lgyi7tg1hk85mvuuf','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vd3vN:jUfObJogvorjhP6WsvWX5zPghq8q9Pk6L6HqbL0y1C0','2026-01-20 10:04:25.122763'),('g9kgo8ed9eqgfuytchxog1obxthkykfy','.eJxVjDsOwjAQBe_iGln-LXEo6XMGy95d4wCypTipEHeHSCmgfTPzXiLEbS1h67yEmcRFmFGcfscU8cF1J3SP9dYktrouc5K7Ig_a5dSIn9fD_TsosZdvbR2RBoY8oPOok4KRtCKNPisPFhSp7NElOiODtgYQBq2MNRGZrUfx_gAHUDf2:1vesi0:DnoYjXUlsP8OpzmNb7j9moJ52ufdK9TNNT08RuzxAjw','2026-01-25 10:30:08.887910'),('gnhfvoo5zhu5azyw3zenc42qonjvra08','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vdnXl:1Ba_6ljSmhmfBebe5lgNJWcX_KDe5SRAhaYuQSaTNkU','2026-01-22 10:47:05.254623'),('goj2smtuvf5dlotnuxirpwfswvrtez2c','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1viXbQ:sH5_piCHM261HUq3AKoeJMgSypnAh7wE7sl4jplO7n4','2026-02-04 12:46:28.409619'),('gpked6x93pyb2nawnt984vcqgbx4svmn','.eJxVjDsOwjAQBe_iGlm2s5vFlPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqL0CROv6Pn8Eh1J_HO9dZkaHVdZi93RR60y6nF9Lwe7t9B4V6-tQ9EyoLNORN6S4Rs4mgIUlaGtLWcBg-kPZrRIAfAAYyKCuA8IKIW7w_16DbE:1venli:1Lz1MUJto9SFcxrCFvuwg90eFjs0Au0WpSTpEw_llWg','2026-01-25 05:13:38.801123'),('gtqa6bclpww8c5q8djqwdxhlyhwzj2f9','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vd2Oc:tF9nr4RvF4PWudghwMo5zyfL1TJSnoynYI_JE_wVb-Y','2026-01-20 08:26:30.102780'),('hhu8yg0hdeadq7a4t3ume8f0q18t0vht','.eJxVjEEOwiAQRe_C2pBCYUCX7nsGAjODVA0kpV0Z765NutDtf-_9lwhxW0vYOi9hJnERSpx-txTxwXUHdI_11iS2ui5zkrsiD9rl1Iif18P9Oyixl28NqEknA2gpO_COUSFnlUYYICk_MPFIlKy2NsPZOMzKRAbrPTECZ_H-AP3AONQ:1vfZ96:V0yd2C-WbfF4qsyn94WZY9zlkUjYqYyCSHsTSEOuZlM','2026-01-27 07:48:56.948376'),('hxmnh07mwr74m6uahudgawwz6gcdpeek','.eJxVjMsOwiAUBf-FtSGFFAGX7v0GcrkPqRpISrtq_Hdt0oVuz8ycTSVYl5LWznOaSF2U8er0O2bAJ9ed0APqvWlsdZmnrHdFH7TrWyN-XQ_376BAL9865hi8oMHoTBwIEAQ42-BQHEkemQACi2D0djhbCo4yjs5RGNmCR_X-AEk6Ocs:1vgfhO:cqJBeglwcMRijVjYH8QOKvLz_OIUUkMXCKMx-7mVScA','2026-01-30 09:00:54.944458'),('ijnii328848e6wkeq0d6bw007p52wy17','.eJxVjMsOwiAQRf-FtSE8ygAu3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmEtjpd0wxP6jtBO-x3TrPva3LnPiu8IMOfu1Iz8vh_h3UOOq3tpmk01GSyN6DLyJPNinrjNPekk65ONIClEEAQu0VyQKIairJkTCCvT8BSTfx:1vd6wd:cI2NAwQt4BXjh8RhKSrntrExTIr4X6nTz05DNYDnm7Q','2026-01-20 13:17:55.728027'),('isg4ctzkwp39utvez13umt8613esow4p','.eJxVjDsOwjAQBe_iGlnxdy1Kes5grddrHEC2FCcV4u4QKQW0b2beS0Tc1hq3wUucszgLFcTpd0xID247yXdsty6pt3WZk9wVedAhrz3z83K4fwcVR_3WRiUDBTxpJpgmZ5SCQOwDgEum2KAyoi6KXbHkQVuk5EiD5hRKNijeH_kFODU:1vh2uR:D_wuRF1uYutH1Y8nW8d6KYRcDcN3JPPGDXbrcc6-Z_k','2026-01-31 09:47:55.997897'),('j8v3zhffccuz3mud6z1mo3wmydoxrxwt','.eJxVjEEOwiAQRe_C2hAGOlRcuu8ZyACDVA0kpV0Z765NutDtf-_9l_C0rcVvnRc_J3ER4MTpdwwUH1x3ku5Ub03GVtdlDnJX5EG7nFri5_Vw_w4K9fKtHTPnoM_ZOYhAxkRWI0ZkHFxQJhACKqssEWXIY1acAeyAmNhobZR4fwAiVjgn:1vepzf:0ziGEKFh6A6XAzVKM42JsK4KPe7R7pCwN7Di5hi8oe0','2026-01-25 07:36:11.632618'),('jb44q210v8qew1ww6se3kb70nwvl1uil','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vhBay:yJUGsUL3celRwvIa5JHVvfvuUzgrebu6vxAYU6i589g','2026-01-31 19:04:24.482546'),('jkw6ccv2zsvgz0glaq6xn5l2qdvcyh9o','.eJxVjMEOwiAQRP-FsyGwBWk9evcbyMKyUjWQlPZk_Hdp0oMe582beQuP25r91tLiZxIXAVqcfmHA-Exlb-iB5V5lrGVd5iB3RR5tk7dK6XU93L-DjC339YAaHQw4TsRgTY-KnCNkSAhInCwp5zqjGFM0jgwPGiyrc1ATjyw-Xx7dOOc:1veq0C:I_SmJ7znIo8cUCJrcHWmGK8tO7EEbeJFrT2x8QO6LnE','2026-01-25 07:36:44.190707'),('k6w62ye0j5bpz9flbnwrt4w42ug8nf92','.eJxVjDsOwjAQBe_iGln-LXEo6XMGy95d4wCypTipEHeHSCmgfTPzXiLEbS1h67yEmcRFmFGcfscU8cF1J3SP9dYktrouc5K7Ig_a5dSIn9fD_TsosZdvbR2RBoY8oPOok4KRtCKNPisPFhSp7NElOiODtgYQBq2MNRGZrUfx_gAHUDf2:1vfyT4:4RtXFzqxUfekQ6y6gq1HbdNuq9jFYPmW5Jf1t52B6iE','2026-01-28 10:51:14.032803'),('l5ji3kpdhf99if6laekmc1n2szvdcq9n','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vdbSV:aJNgkDApUqdIr8zMvtaPWZRv2Ggp3S9dT2TNrKVSjzI','2026-01-21 21:52:51.500223'),('lqhrzp77ezd0cz2pdmqs07ghi7n2ninr','.eJxVjDsOwjAQBe_iGlnrbzAlfc5g7ca7JIBsKZ8KcXeIlALaNzPvpTJu65i3hec8FXVRDtTpdyQcHlx3Uu5Yb00Pra7zRHpX9EEX3bfCz-vh_h2MuIzfegjRQuIg5JLxwXBKEjsCYW87HyShMyUSeWHCzrpoDZAIFrJg4Czq_QH_mTgt:1vhBXE:f91NA4pJiVu1Z5Ubb-rZ8O-RroHap_huUADusya3Wyc','2026-01-31 19:00:32.745373'),('ls737iabs15is5uui72d000kqvatl10i','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vdkyn:sbanQuzzmfEKu0GSN_FLPiKynDkaeiU-wn0ANPkfaY8','2026-01-22 08:02:49.437291'),('lx262mjib7cgj9e9yt0xcri8z1mesxys','.eJxVjMsOwiAUBf-FtSGFFAGX7v0GcrkPqRpISrtq_Hdt0oVuz8ycTSVYl5LWznOaSF2U8er0O2bAJ9ed0APqvWlsdZmnrHdFH7TrWyN-XQ_376BAL9865hi8oMHoTBwIEAQ42-BQHEkemQACi2D0djhbCo4yjs5RGNmCR_X-AEk6Ocs:1vfJfu:OTYnw-v3V4JjYO_cAcRxAqrUAdZZJYPZSLfzbAG20p8','2026-01-26 15:17:46.380827'),('m48cim7xnunxpngfy2glwhfoqorjb1m8','.eJxVjDsOwjAQBe_iGln-LXEo6XMGy95d4wCypTipEHeHSCmgfTPzXiLEbS1h67yEmcRFmFGcfscU8cF1J3SP9dYktrouc5K7Ig_a5dSIn9fD_TsosZdvbR2RBoY8oPOok4KRtCKNPisPFhSp7NElOiODtgYQBq2MNRGZrUfx_gAHUDf2:1vhLw1:wvqba01lJSQ-2ZVlHjqGenpBZUvPwaR8YY7UDQhbTRI','2026-02-01 06:06:49.363409'),('m5yt20xz51bfx4o41f4wbvbbjko5gnaf','.eJxVjEEOwiAQAP_C2RCW2AU8evcNZGEXqRqalPZk_Lsh6UGvM5N5q0j7VuPeZY0zq4uyRp1-YaL8lDYMP6jdF52Xtq1z0iPRh-36trC8rkf7N6jU6_iCOPJUhGySgKEIJ0tecEI0yOJSYGvFARQ_ATC4sw3oMRGTAZ_V5wsmbzhr:1veptW:49TjKi0rwYBezT8jMCvIo117Hk8rBeico0rTGp1pADc','2026-01-25 07:29:50.050690'),('m7vwj1pkla7q0kzwt46s7m4w6skrbt7c','.eJxVjEEOwiAQAP_C2RCW2AU8evcNZGEXqRqalPZk_Lsh6UGvM5N5q0j7VuPeZY0zq4uyRp1-YaL8lDYMP6jdF52Xtq1z0iPRh-36trC8rkf7N6jU6_iCOPJUhGySgKEIJ0tecEI0yOJSYGvFARQ_ATC4sw3oMRGTAZ_V5wsmbzhr:1vepze:fWLc8mFS9QwEKesChSYThywshmJFaOc268hKRDY4cUI','2026-01-25 07:36:10.273683'),('mbgh4gsabhgsvlyqyh3sh9sxtawqi3v9','.eJxVjDsOwjAQBe_iGlnxdy1Kes5grddrHEC2FCcV4u4QKQW0b2beS0Tc1hq3wUucszgLFcTpd0xID247yXdsty6pt3WZk9wVedAhrz3z83K4fwcVR_3WRiUDBTxpJpgmZ5SCQOwDgEum2KAyoi6KXbHkQVuk5EiD5hRKNijeH_kFODU:1viTQx:zhHoFlYdu_FzOxwaPsTsvdPoZDjFoYjrYbVLJW2XDD0','2026-02-04 08:19:23.838953'),('mchifhszsmbc9q4okoervjo8yvle6g0a','.eJxVjEEOwiAQAP_C2RCW2AU8evcNZGEXqRqalPZk_Lsh6UGvM5N5q0j7VuPeZY0zq4uyRp1-YaL8lDYMP6jdF52Xtq1z0iPRh-36trC8rkf7N6jU6_iCOPJUhGySgKEIJ0tecEI0yOJSYGvFARQ_ATC4sw3oMRGTAZ_V5wsmbzhr:1veptb:9Uw6jSz3R2CWGoE3afw72ITKkyLC9bRCYFidUE8OYP4','2026-01-25 07:29:55.482434'),('mwj1ier1e92kd9j0socul5r3nvhwfcdw','.eJxVjDsOwjAQBe_iGln-LXEo6XMGy95d4wCypTipEHeHSCmgfTPzXiLEbS1h67yEmcRFmFGcfscU8cF1J3SP9dYktrouc5K7Ig_a5dSIn9fD_TsosZdvbR2RBoY8oPOok4KRtCKNPisPFhSp7NElOiODtgYQBq2MNRGZrUfx_gAHUDf2:1vfgCq:GZlRmTKzXtMyGXb3fM2wfeJcS-f11vOf2e43O-i4_t4','2026-01-27 15:21:16.574106'),('n0komulxfmy5lwxj1q80hvy7lawk4fxm','.eJxVjMsOwiAQRf-FtSE8ygAu3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmEtjpd0wxP6jtBO-x3TrPva3LnPiu8IMOfu1Iz8vh_h3UOOq3tpmk01GSyN6DLyJPNinrjNPekk65ONIClEEAQu0VyQKIairJkTCCvT8BSTfx:1vd9Co:jt0Ueezq-md_twhOaUwxngQhctQxkaI6gA-ybBcbyxQ','2026-01-20 15:42:46.297617'),('no5dbz22i4f4z6sq5jxnojgo37dsmi11','.eJxVjDsOwjAQBe_iGlnrbzAlfc5g7ca7JIBsKZ8KcXeIlALaNzPvpTJu65i3hec8FXVRDtTpdyQcHlx3Uu5Yb00Pra7zRHpX9EEX3bfCz-vh_h2MuIzfegjRQuIg5JLxwXBKEjsCYW87HyShMyUSeWHCzrpoDZAIFrJg4Czq_QH_mTgt:1vdkza:KrdmEKCf-iq88SwFkC3ZN79LtAhK0TuvC_iMlaOSZB4','2026-01-22 08:03:38.360573'),('o72y7rwo5mli6r5myzh04kh7h8wmt7g3','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vfgKy:m2e4KOFfJeeYdfUHCLcx3E7cS4kGEc8Q-MHX88HMsOo','2026-01-27 15:29:40.311944'),('o9y21stacltlrtb6krmgz89cdrvfac0f','.eJxVjEEOwiAQAP_C2RCW2AU8evcNZGEXqRqalPZk_Lsh6UGvM5N5q0j7VuPeZY0zq4uyRp1-YaL8lDYMP6jdF52Xtq1z0iPRh-36trC8rkf7N6jU6_iCOPJUhGySgKEIJ0tecEI0yOJSYGvFARQ_ATC4sw3oMRGTAZ_V5wsmbzhr:1veptf:LDVSqW5aYGUyftFZZyote_GcWMbKo30S5jSZw2sbvWs','2026-01-25 07:29:59.470751'),('p1cuj6rpm82133o2cpvm4668qb3etxe6','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vdA5N:PitgA2s7L4nEnHd5MCGMvA1N-lQNZdLwwSCXM0imm64','2026-01-20 16:39:09.459158'),('pan1ltckmgiihipiltw229z99by2av7t','.eJxVjEEOwiAQAP_C2RCW2AU8evcNZGEXqRqalPZk_Lsh6UGvM5N5q0j7VuPeZY0zq4uyRp1-YaL8lDYMP6jdF52Xtq1z0iPRh-36trC8rkf7N6jU6_iCOPJUhGySgKEIJ0tecEI0yOJSYGvFARQ_ATC4sw3oMRGTAZ_V5wsmbzhr:1vgiPy:bPxZijMBXZh0xVqfhjZbimggB7aFcOzop6VPcF9da7E','2026-01-30 11:55:06.165841'),('pjdat7xwvstvuihfqdmvpxt3x3462p70','.eJxVjDsOwjAQBe_iGln-LXEo6XMGy95d4wCypTipEHeHSCmgfTPzXiLEbS1h67yEmcRFmFGcfscU8cF1J3SP9dYktrouc5K7Ig_a5dSIn9fD_TsosZdvbR2RBoY8oPOok4KRtCKNPisPFhSp7NElOiODtgYQBq2MNRGZrUfx_gAHUDf2:1veSgC:MHA9xdbezxaqG7Ab7zxmcr_7j_PtOiK-aUe2Rvn-3VE','2026-01-24 06:42:32.234733'),('pls0tx71sri407hmrdr5cf5yhdnt9rfv','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vepo3:6bqzhvS5xb4hFdJEtgxM-FqAwnuwDO6-Tg7nd1cp2Wo','2026-01-25 07:24:11.861936'),('pnmlnh6telzta5mqpa06q4asj0nwuqcr','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vepnp:g2vXLqPhpwu57MBklyDCuDuHliWYSWg9fHtx_ZoXDmo','2026-01-25 07:23:57.323424'),('q246bd0pfllj8o07drjo7cjunaun2sck','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vd3re:MtNYv29n0DXdgdKZmWJI0m-gciq1cCl_oCy7APhMuRM','2026-01-20 10:00:34.131897'),('q4nmzydtwt6d49g4hm75jlsax4fc844f','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vd8aH:dl9XZJoFaB3R9CSY8T1diKZejf7dXvETDtPWAStA31c','2026-01-20 15:02:57.474520'),('qq31r4c3rlp6qoysed9qu9ybqw0x9jh9','.eJxVjDsOwjAQBe_iGlnrbzAlfc5g7ca7JIBsKZ8KcXeIlALaNzPvpTJu65i3hec8FXVRDtTpdyQcHlx3Uu5Yb00Pra7zRHpX9EEX3bfCz-vh_h2MuIzfegjRQuIg5JLxwXBKEjsCYW87HyShMyUSeWHCzrpoDZAIFrJg4Czq_QH_mTgt:1vfwgz:Wy3_kDefoc9Jg37J4d7EZF5lLsaRcTcgNlbavopeXa8','2026-01-28 08:57:29.912698'),('r02vhxyko1c5zfh1hn7auz9g3uyy5tby','.eJxVjEEOwiAQAP_C2RCW2AU8evcNZGEXqRqalPZk_Lsh6UGvM5N5q0j7VuPeZY0zq4uyRp1-YaL8lDYMP6jdF52Xtq1z0iPRh-36trC8rkf7N6jU6_iCOPJUhGySgKEIJ0tecEI0yOJSYGvFARQ_ATC4sw3oMRGTAZ_V5wsmbzhr:1vepta:NO99CSaZ1tSYcT9gj-QlsJGaUvEFSLvrzMr80W752FA','2026-01-25 07:29:54.127815'),('r998q83fcpr0asn6840rsocr8x5cu8hr','.eJxVjEEOgjAQRe_StWlaoHTq0j1nIDPTqaCmTSisjHcXEha6_e-9_1Yjbus0blWWcY7qqhqvLr8jIT8lHyQ-MN-L5pLXZSZ9KPqkVQ8lyut2un8HE9Zpr70VtowhoUvGsyPoCbgRgmACUgSTLLumbQF6cGR304D0bZfAo-9Afb4hqjgj:1vevRh:7Wcumrr2zKXoB4U438z2P2fn7-_yHHgPTJce9dKOOn8','2026-01-25 13:25:29.155032'),('rgm7gm90ucrwivudzxo2vhchtsfcq3a7','.eJxVjMsOwiAQRf-FtSE8ygAu3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmEtjpd0wxP6jtBO-x3TrPva3LnPiu8IMOfu1Iz8vh_h3UOOq3tpmk01GSyN6DLyJPNinrjNPekk65ONIClEEAQu0VyQKIairJkTCCvT8BSTfx:1vdbL3:W5V7hkabllRaSwyIjDL_ciXiTdOFZoeExASDkbjI6Oo','2026-01-21 21:45:09.050845'),('rva8fxbe4ckkn1miuw4r70yz63oahops','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vd5hl:mw26Hd62T7ASMBsP47IQ_RADdHZLsH6lUTk3GKOGvpM','2026-01-20 11:58:29.182434'),('smdcvd435djt6tmam11buz20d7dzb9u6','.eJxVjMsOwiAQRf-FtSE8ygAu3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmEtjpd0wxP6jtBO-x3TrPva3LnPiu8IMOfu1Iz8vh_h3UOOq3tpmk01GSyN6DLyJPNinrjNPekk65ONIClEEAQu0VyQKIairJkTCCvT8BSTfx:1vdAbm:31BOr21CuWm-v2dz53tTGbrgvxzwkJ1T-KFEaGpPqSY','2026-01-20 17:12:38.833971'),('stl06l17pnr15w6oeo4vkobxb61y8v39','.eJxVjDsOwjAQBe_iGlm2s5vFlPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqL0CROv6Pn8Eh1J_HO9dZkaHVdZi93RR60y6nF9Lwe7t9B4V6-tQ9EyoLNORN6S4Rs4mgIUlaGtLWcBg-kPZrRIAfAAYyKCuA8IKIW7w_16DbE:1vevbO:JCQAX1zj6pQsdLINIeLGjsNm_jN9mphiSL2aXIHrp9Y','2026-01-25 13:35:30.232799'),('syx3p23tqnmqjk6mt2l0j23j43sqbvsm','.eJxVjEEOwiAQRe_C2hCGEWhduu8ZyDCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-juIiwInT7xiIH6nuJN6p3prkVtdlDnJX5EG7nFpMz-vh_h0U6uVba6UsOZWQsuGcjWI9EA4YABJEayPjGci6MYLSRCY7DoyEWRvkUSvx_gAI2jgQ:1vevo0:84sORj0yCQ9G8QtZVCADb58NaDjSCOStdDlkZtxy7Ww','2026-01-25 13:48:32.806757'),('tfw79kbd5v2wcqhrpbuzzrm4w6le4bzl','.eJxVjEEOwiAQRe_C2pBCYUCX7nsGAjODVA0kpV0Z765NutDtf-_9lwhxW0vYOi9hJnERSpx-txTxwXUHdI_11iS2ui5zkrsiD9rl1Iif18P9Oyixl28NqEknA2gpO_COUSFnlUYYICk_MPFIlKy2NsPZOMzKRAbrPTECZ_H-AP3AONQ:1vgiLQ:kgVa1JaOd0i6bPaj4V09pNj_DCwvj3dXlfYjtELZZcE','2026-01-30 11:50:24.185740'),('ti9lm1ch4l2mm20a69recykk4ptxcib1','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vdAVX:M4I80QTItfL8uTVq8ni7takR2hui4SsRZDY5xaBL97Y','2026-01-20 17:06:11.210481'),('ttak18dq69scunlp40eedoy5oxvsxl8k','.eJxVjDsOwjAQBe_iGlm2s94NlPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLMChOv6Pn8Eh1J_HO9dZkaHVdZi93RR60y6nF9Lwe7t9B4V6-NVgPicBng6OGmJEIiNQA-WwzBp01ZZ8UDMYSWRwRdKRBsVEhMBGJ9wfoLjb9:1vesWp:qsnq80GxRty9Hmnc-40yGxbHWuPj3atenFPsj5Mvn3o','2026-01-25 10:18:35.971993'),('tvzm8hs01qjfb6q1tqzfwkaz6jcvm5ez','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vfyG6:CDn0xyjMgEQdjO-3DzuTO8zU0NvSaZPje8FNbT8VO3s','2026-01-28 10:37:50.202961'),('u1iuhd7e7696mmh1oelb2vgeac8rw6xe','.eJxVjEEOwiAQAP_C2RCW2AU8evcNZGEXqRqalPZk_Lsh6UGvM5N5q0j7VuPeZY0zq4uyRp1-YaL8lDYMP6jdF52Xtq1z0iPRh-36trC8rkf7N6jU6_iCOPJUhGySgKEIJ0tecEI0yOJSYGvFARQ_ATC4sw3oMRGTAZ_V5wsmbzhr:1vgiPf:YgtlDh9yJLWgFvSMEaC0qO9Ka2a30Aou-ndaN8xtjeA','2026-01-30 11:54:47.552821'),('u4b7bxx4hkuxpniq20zzxt54urgbisl7','.eJxVjMEOwiAQRP-FsyGwBWk9evcbyMKyUjWQlPZk_Hdp0oMe582beQuP25r91tLiZxIXAVqcfmHA-Exlb-iB5V5lrGVd5iB3RR5tk7dK6XU93L-DjC339YAaHQw4TsRgTY-KnCNkSAhInCwp5zqjGFM0jgwPGiyrc1ATjyw-Xx7dOOc:1vepvU:vhiVfRLuHA3GI30rVpKTKEp2kxV5a-NkPOT3XaPLLAA','2026-01-25 07:31:52.121631'),('ukuh71thnb9qurpjui1hij65zzzoakm6','.eJxVjEEOgjAQRe_StWlaoHTq0j1nIDPTqaCmTSisjHcXEha6_e-9_1Yjbus0blWWcY7qqhqvLr8jIT8lHyQ-MN-L5pLXZSZ9KPqkVQ8lyut2un8HE9Zpr70VtowhoUvGsyPoCbgRgmACUgSTLLumbQF6cGR304D0bZfAo-9Afb4hqjgj:1vevSi:XTusfsu6WpRYvCJ6Iz7wIBKoHJPy4jDpC8YZOoTDtA8','2026-01-25 13:26:32.553714'),('uqcphshktlr4sq70ait6avkgezy3zqbo','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vd9bb:EatLG8gokBuZh3_i2L2ZCilFnU65W5Y1sVfWtKlbMIQ','2026-01-20 16:08:23.216697'),('v9b9uf6zazit7jxoke6rnkp4iig46y0o','.eJxVjMsOwiAQRf-FtSE8ygAu3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmEtjpd0wxP6jtBO-x3TrPva3LnPiu8IMOfu1Iz8vh_h3UOOq3tpmk01GSyN6DLyJPNinrjNPekk65ONIClEEAQu0VyQKIairJkTCCvT8BSTfx:1vdZ6M:N6DKsR9l449NYafNZedGsqnWsiAIpSWAcB-AMnvaQ5Y','2026-01-21 19:21:50.629804'),('vjyf6vgoxqubizocc70idsj3nk57lpnf','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vdbLl:DfefVOWAeVwU8JQkkt-Nxf2JtGdEGXd_cvwqtzX0kAI','2026-01-21 21:45:53.374952'),('vlagwsqzuwpsjph1f4qzi7c0p7l8ek1d','.eJxVjDsOwjAQBe_iGlnrbzAlfc5g7ca7JIBsKZ8KcXeIlALaNzPvpTJu65i3hec8FXVRDtTpdyQcHlx3Uu5Yb00Pra7zRHpX9EEX3bfCz-vh_h2MuIzfegjRQuIg5JLxwXBKEjsCYW87HyShMyUSeWHCzrpoDZAIFrJg4Czq_QH_mTgt:1vdnNU:7VlSu3d6Qf3KRNBnbntjkM5PbQQdR7auTsyzmy5QcDo','2026-01-22 10:36:28.555808'),('vp0bltkfpvii5u5rvops3aypzv4vhojt','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vd59X:OMu6dGvXBu-m8M9cxYHViUkHZVENkIydqaKyl4aUGNc','2026-01-20 11:23:07.476498'),('vrhq668oz6vphqkvoc77ddeszv4fbdzw','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vevom:yPtpqheXSRFQv8WEsFHROxoiGmBA_nC03bn9AG1KYQ8','2026-01-25 13:49:20.157469'),('wb1q2pj1d3rdqrmdme1mg9rhy0mzccfb','.eJxVjMEOwiAQRP-FsyGwBWk9evcbyMKyUjWQlPZk_Hdp0oMe582beQuP25r91tLiZxIXAVqcfmHA-Exlb-iB5V5lrGVd5iB3RR5tk7dK6XU93L-DjC339YAaHQw4TsRgTY-KnCNkSAhInCwp5zqjGFM0jgwPGiyrc1ATjyw-Xx7dOOc:1vepz2:sD0eJt3aHZ4YcgQOySO8mFBYOd-NgklJ5COn3wVW34M','2026-01-25 07:35:32.292072'),('wch0xyi8lj3qdmpamc2accpmadcqmoyv','.eJxVjEEOwiAQAP_C2RCW2AU8evcNZGEXqRqalPZk_Lsh6UGvM5N5q0j7VuPeZY0zq4uyRp1-YaL8lDYMP6jdF52Xtq1z0iPRh-36trC8rkf7N6jU6_iCOPJUhGySgKEIJ0tecEI0yOJSYGvFARQ_ATC4sw3oMRGTAZ_V5wsmbzhr:1veptd:0_Tfv3qZwJMVS6cKWdESelp1Guz5CwmAMnGes8SLUJU','2026-01-25 07:29:57.475215'),('wgdzmt7y8cikeakp4o5d2hxnjwxb63vv','.eJxVjDsOwjAQBe_iGlm2s5vFlPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqL0CROv6Pn8Eh1J_HO9dZkaHVdZi93RR60y6nF9Lwe7t9B4V6-tQ9EyoLNORN6S4Rs4mgIUlaGtLWcBg-kPZrRIAfAAYyKCuA8IKIW7w_16DbE:1venn9:kdvoOvuw-ANk5-aZrK8r9UcodLW4lfeF0BCyHfZwKGg','2026-01-25 05:15:07.559018'),('womhoiupfm4kbtcz2b72z2gpkppxf4di','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vesfm:nXdUaSICqiA7DPEeSOVl591pJTF2KpCCv84Ajhq__-k','2026-01-25 10:27:50.018967'),('wshvib919o2zbb63nkxr7w3ingiwc3tq','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vd9eO:F9KB9mx0uvjWTkgJ1o9pFHoX_Cjnh_kPtT5aJwL-XzQ','2026-01-20 16:11:16.992633'),('x2d8fnrf5dpy3d4wnjp38wikuvlbnndx','.eJxVjDsOwjAQBe_iGln-LXEo6XMGy95d4wCypTipEHeHSCmgfTPzXiLEbS1h67yEmcRFmFGcfscU8cF1J3SP9dYktrouc5K7Ig_a5dSIn9fD_TsosZdvbR2RBoY8oPOok4KRtCKNPisPFhSp7NElOiODtgYQBq2MNRGZrUfx_gAHUDf2:1veAlB:Q-KymT08r310m9tebr2e2iVnw-p5J95_Bh-HrU1sSjc','2026-01-23 11:34:29.835121'),('x49sgub1t7vdxzlpfq7iysdli3fro8zq','.eJxVjEEOwiAQRe_C2pCREXBcuu8ZyHQAqRpISrsy3l2bdKHb_977LxV4XUpYe5rDFNVFGasOv-PI8kh1I_HO9da0tLrM06g3Re-066HF9Lzu7t9B4V6-tUNImYWtPxN5ypFRHFoH5P0pURbMhHKMHsCAWAFkQrCWiQ2D8-r9AQKRN38:1veqNV:77jO4zJF2bMe-KFAeIfWDI5vMNNHrvQvb6tWAvaOa_E','2026-01-25 08:00:49.064849'),('x6ay1fo1j5qhi372cerj3k8y1w87n4v4','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vd6xq:o2sVyVW_cCoGZsoRVW87MiP2zzahlBn09fl6omc9zoM','2026-01-20 13:19:10.566744'),('xqbrm6kr184u1aruc5p763zfuu23s26x','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vd2RB:645pkWjI_DpnS-S20miSTUJYkEqv3jSDl0BaspFCp5s','2026-01-20 08:29:09.660064'),('xthj8ioapt049mo0x28wsd014ahqw7tt','.eJxVjEEOwiAQRe_C2pBCYUCX7nsGAjODVA0kpV0Z765NutDtf-_9lwhxW0vYOi9hJnERSpx-txTxwXUHdI_11iS2ui5zkrsiD9rl1Iif18P9Oyixl28NqEknA2gpO_COUSFnlUYYICk_MPFIlKy2NsPZOMzKRAbrPTECZ_H-AP3AONQ:1vi6ou:0sE7YNMsszwvDVsW3ivWU9QQt7r67PR6MISBxYPVmiA','2026-02-03 08:10:36.256353'),('y6rg2pn2fnvp7ing8l8wzzmznyyptn3u','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vhLrD:U3YmpBHntJ2WLe_wIHF5XB76c9t3odaT1_xz0MsmZAM','2026-02-01 06:01:51.241241'),('yhx8ple2t03b4vdqa53y772nnetgiaj8','.eJxVjMsOwiAQRf-FtSE8ygAu3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmEtjpd0wxP6jtBO-x3TrPva3LnPiu8IMOfu1Iz8vh_h3UOOq3tpmk01GSyN6DLyJPNinrjNPekk65ONIClEEAQu0VyQKIairJkTCCvT8BSTfx:1vd9hw:6t0oeZToU2j_ua-oXVGNZ_nWrHtAVY_Ir73XKc43Ho0','2026-01-20 16:14:56.537409'),('yjeeif51rou7qpank1lr4y6rwoxs9a26','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vdbMM:CrWzmZBxr6FAG7vq8u8FObTkXEjRZ8IoMxsB6UMRQ_s','2026-01-21 21:46:30.616696'),('ylj5pd99l7kilvi41ksql3dw694dhpem','.eJxVjEEOwiAQRe_C2hCEAYtL956BDDNTqRpISrsy3l2bdKHb_977L5VwXUpau8xpYnVW1qnD75iRHlI3wnest6ap1WWest4UvdOur43ledndv4OCvXzrzJbAUDwBeszBZQ-RXbRWhEc4BhASICBvwAVDg6ALBCEyII5iBvX-ABg1OI4:1vfG6q:k7RgTYtvK6Svn6hVQGqkzwAQErzANLcwZpipE2xB8k8','2026-01-26 11:29:20.600377'),('yly5jcnx2rd4jwd8mbc0rmuks5hw7xqq','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vi6p9:6gyMfqxEceNFD36t_1AZyWMbr2-mgDUsxPDq8NKMeuU','2026-02-03 08:10:51.821503'),('yr355im8paqxjl5186pqbctvo1mzl9z3','.eJxVjMsOwiAQRf-FtSE8ygAu3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmEtjpd0wxP6jtBO-x3TrPva3LnPiu8IMOfu1Iz8vh_h3UOOq3tpmk01GSyN6DLyJPNinrjNPekk65ONIClEEAQu0VyQKIairJkTCCvT8BSTfx:1vd5jA:x_uLD4OJvT6L-ZCjZGqc1fcvazRmRyE9vctFq-TVnW8','2026-01-20 11:59:56.725113'),('zcvq3whs683a9fafndm5o7bche4j5wz3','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vd3qm:LCYchoy3ZccsUh5VU0-t9xYvKCyXHTdKa_gV1kB2J2k','2026-01-20 09:59:40.688175'),('zdwg69yxtw6o1ei3okk85mudno6d8hmw','.eJxVjMsOwiAQRf-FtSE8ygAu3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmEtjpd0wxP6jtBO-x3TrPva3LnPiu8IMOfu1Iz8vh_h3UOOq3tpmk01GSyN6DLyJPNinrjNPekk65ONIClEEAQu0VyQKIairJkTCCvT8BSTfx:1vd8Al:JZ24weHK__P6-5WKk4r0MdCWr06-qaWvmR5CdyZjvs0','2026-01-20 14:36:35.833240'),('zfujmzenwu7jmv5ho238x7xiruhowtu1','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vdn7g:ajhJmlbGuoDLNEqDCvVw1_WQYwKxbVuiggMQsPTyqRo','2026-01-22 10:20:08.044011'),('znphc1si5tsdo9l86d4c70gi893ta0e4','.eJxVjDsOwjAQBe_iGln-LXEo6XMGy95d4wCypTipEHeHSCmgfTPzXiLEbS1h67yEmcRFmFGcfscU8cF1J3SP9dYktrouc5K7Ig_a5dSIn9fD_TsosZdvbR2RBoY8oPOok4KRtCKNPisPFhSp7NElOiODtgYQBq2MNRGZrUfx_gAHUDf2:1veAl5:j2P-bfxfsAFlBjOl6HAVcuPVVfGlL_9qNt097awo4j8','2026-01-23 11:34:23.171320'),('zrzq4bg60juspr3r8bcjdwigd0782jkt','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vd6oh:aUYnVm_-U99eSeUJcwFY9uOmFUbs_Mzlmwq4LDqfucc','2026-01-20 13:09:43.686580'),('ztog55b405u1eluruwdxvyii5maeod6j','.eJxVjDsOwjAQBe_iGlm2s94NlPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLMChOv6Pn8Eh1J_HO9dZkaHVdZi93RR60y6nF9Lwe7t9B4V6-NVgPicBng6OGmJEIiNQA-WwzBp01ZZ8UDMYSWRwRdKRBsVEhMBGJ9wfoLjb9:1veu2T:ZM5yI7ssP010tjVi7af6YotI0IotlPa2Jo_mY6XG8Rs','2026-01-25 11:55:21.446204'),('zv7927scc85v910ym6qc3orxtq7ptzbz','.eJxVjMsOwiAQRf-FtSED5VFcuvcbyDBMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxZnMYjT75aQHlx3kO9Yb01Sq-syJ7kr8qBdXlvm5-Vw_w4K9vKtJw1JJYPgFTFqMNok8ENAY6bRATEHReSdzypYC54gh8yORqvtkAKL9wfY1zeZ:1vd2N4:DhFwVLGkq_2d-vQou7Wcjz6f6BIYKxpkgEcx9Gq-Bss','2026-01-20 08:24:54.989615'),('zv971xne5yqvgov0912l37zyjce6pwxo','.eJxVjEEOwiAQRe_C2hBgCoJL9z1DM8wMUjVtUtqV8e7apAvd_vfef6kBt7UOW5NlGFldlFOn3y0jPWTaAd9xus2a5mldxqx3RR-06X5meV4P9--gYqvfOhTHhn22TLkkSYas-A4KEgOcbZSUC1DIpusAnSCnQOBSNFJ8kOjV-wMLDTiX:1vd4UA:mBKLW8slLSHWO9QgeQgg1Yqtc21jUr0P0UvkKGmrCx0','2026-01-20 10:40:22.867329');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_attendance`
--

DROP TABLE IF EXISTS `employee_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_attendance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `login_time` datetime(6) DEFAULT NULL,
  `logout_time` datetime(6) DEFAULT NULL,
  `login_image` varchar(100) DEFAULT NULL,
  `logout_image` varchar(100) DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `overtime_hours` decimal(5,2) DEFAULT NULL,
  `break_hours` decimal(5,2) DEFAULT NULL,
  `total_hours` decimal(5,2) DEFAULT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `employee_attendance_employee_id_d9440ea4_fk_employee_employee_id` (`employee_id`),
  CONSTRAINT `employee_attendance_employee_id_d9440ea4_fk_employee_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee_employee` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=203 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_attendance`
--

LOCK TABLES `employee_attendance` WRITE;
/*!40000 ALTER TABLE `employee_attendance` DISABLE KEYS */;
INSERT INTO `employee_attendance` VALUES (12,NULL,NULL,'','','absent','2026-01-09',NULL,0.00,NULL,25),(13,NULL,NULL,'','','absent','2026-01-09',NULL,0.00,NULL,26),(14,NULL,NULL,'','','absent','2026-01-09',NULL,0.00,NULL,27),(15,NULL,NULL,'','','absent','2026-01-09',NULL,0.00,NULL,28),(16,NULL,NULL,'','','absent','2026-01-09',NULL,0.00,NULL,29),(17,NULL,NULL,'','','absent','2026-01-09',NULL,0.00,NULL,30),(18,NULL,NULL,'','','absent','2026-01-09',NULL,0.00,NULL,31),(19,NULL,NULL,'','','absent','2026-01-09',NULL,0.00,NULL,32),(20,NULL,NULL,'','','absent','2026-01-09',NULL,0.00,NULL,33),(21,NULL,NULL,'','','absent','2026-01-09',NULL,0.00,NULL,34),(22,NULL,NULL,'','','absent','2026-01-09',NULL,0.00,NULL,35),(23,NULL,NULL,'','','absent','2026-01-09',NULL,0.00,NULL,36),(24,NULL,NULL,'','','absent','2026-01-09',0.00,0.00,0.00,37),(25,NULL,NULL,'','','absent','2026-01-10',NULL,0.00,NULL,25),(26,NULL,NULL,'','','absent','2026-01-10',NULL,0.00,NULL,26),(27,NULL,NULL,'','','absent','2026-01-10',NULL,0.00,NULL,27),(28,NULL,NULL,'','','absent','2026-01-10',NULL,0.00,NULL,28),(29,NULL,NULL,'','','absent','2026-01-10',NULL,0.00,NULL,29),(30,NULL,NULL,'','','absent','2026-01-10',NULL,0.00,NULL,30),(31,NULL,NULL,'','','absent','2026-01-10',NULL,0.00,NULL,31),(32,NULL,NULL,'','','absent','2026-01-10',NULL,0.00,NULL,32),(33,NULL,NULL,'','','absent','2026-01-10',NULL,0.00,NULL,33),(34,NULL,NULL,'','','absent','2026-01-10',NULL,0.00,NULL,34),(35,NULL,NULL,'','','absent','2026-01-10',NULL,0.00,NULL,35),(36,NULL,NULL,'','','absent','2026-01-10',NULL,0.00,NULL,36),(37,NULL,NULL,'','','absent','2026-01-10',NULL,0.00,NULL,37),(38,'2026-01-11 07:36:39.491886',NULL,'attendance/login/checkin_1768116998676.jpg','','present','2026-01-11',NULL,0.00,NULL,27),(39,'2026-01-11 10:32:00.000000','2026-01-11 15:30:00.000000','attendance/login/checkin_1768127527136.jpg','','present','2026-01-11',0.00,0.00,4.97,37),(40,'2026-01-11 12:00:34.922699',NULL,'attendance/login/checkin_1768132834797.jpg','','present','2026-01-11',NULL,0.00,NULL,34),(41,'2026-01-11 12:01:06.635198','2026-01-11 17:35:45.409578','attendance/login/checkin_1768132865472.jpg','attendance/logout/checkout_1768152944239.jpg','present','2026-01-11',0.00,0.00,5.58,30),(42,'2026-01-11 17:36:00.436357','2026-01-11 17:36:15.657301','attendance/login/checkin_1768152959823.jpg','attendance/logout/checkout_1768152975479.jpg','present','2026-01-11',0.00,0.00,0.00,25),(43,NULL,NULL,'','','absent','2026-01-11',NULL,0.00,NULL,26),(44,NULL,NULL,'','','absent','2026-01-11',NULL,0.00,NULL,28),(45,NULL,NULL,'','','absent','2026-01-11',NULL,0.00,NULL,29),(46,NULL,NULL,'','','absent','2026-01-11',NULL,0.00,NULL,31),(47,NULL,NULL,'','','absent','2026-01-11',NULL,0.00,NULL,32),(48,NULL,NULL,'','','absent','2026-01-11',NULL,0.00,NULL,33),(49,NULL,NULL,'','','absent','2026-01-11',NULL,0.00,NULL,35),(50,NULL,NULL,'','','absent','2026-01-11',NULL,0.00,NULL,36),(51,'2026-01-12 05:37:23.971527',NULL,'attendance/login/checkin_1768196243802.jpg','','present','2026-01-12',NULL,0.00,NULL,34),(52,'2026-01-12 07:13:43.599806',NULL,'attendance/login/checkin_1768202022504.jpg','','present','2026-01-12',NULL,0.00,NULL,30),(53,'2026-01-12 07:23:31.016272',NULL,'attendance/login/checkin_1768202609811.jpg','','present','2026-01-12',NULL,0.00,NULL,27),(54,'2026-01-12 08:15:26.950192',NULL,'attendance/login/checkin_1768205725680.jpg','','present','2026-01-12',NULL,0.00,NULL,37),(55,'2026-01-12 09:36:20.679609',NULL,'attendance/login/checkin_1768210580503.jpg','','present','2026-01-12',NULL,0.00,NULL,25),(56,'2026-01-12 11:29:56.103883',NULL,'attendance/login/checkin_1768217394561.jpg','','present','2026-01-12',NULL,0.00,NULL,31),(58,NULL,NULL,'','','absent','2026-01-12',NULL,0.00,NULL,26),(59,NULL,NULL,'','','absent','2026-01-12',NULL,0.00,NULL,28),(60,NULL,NULL,'','','absent','2026-01-12',NULL,0.00,NULL,29),(61,NULL,NULL,'','','absent','2026-01-12',NULL,0.00,NULL,32),(62,NULL,NULL,'','','absent','2026-01-12',NULL,0.00,NULL,33),(63,NULL,NULL,'','','absent','2026-01-12',NULL,0.00,NULL,35),(64,NULL,NULL,'','','absent','2026-01-12',NULL,0.00,NULL,36),(65,'2026-01-13 05:46:33.333724',NULL,'attendance/login/checkin_1768283193196.jpg','','present','2026-01-13',NULL,0.00,NULL,34),(66,'2026-01-13 06:33:20.378731',NULL,'attendance/login/checkin_1768285999369.jpg','','present','2026-01-13',NULL,0.00,NULL,27),(67,'2026-01-13 07:22:18.957304','2026-01-13 17:37:19.011798','attendance/login/checkin_1768288937815.jpg','attendance/logout/checkout_1768325837828.jpg','present','2026-01-13',0.25,0.00,10.25,30),(68,NULL,NULL,'','','present','2026-01-13',NULL,0.00,NULL,37),(69,'2026-01-13 08:07:49.725090',NULL,'attendance/login/checkin_1768291668462.jpg','','present','2026-01-13',NULL,0.00,NULL,31),(70,NULL,NULL,'','','absent','2026-01-13',NULL,0.00,NULL,25),(71,NULL,NULL,'','','absent','2026-01-13',NULL,0.00,NULL,26),(72,NULL,NULL,'','','absent','2026-01-13',NULL,0.00,NULL,28),(73,NULL,NULL,'','','absent','2026-01-13',NULL,0.00,NULL,29),(74,NULL,NULL,'','','absent','2026-01-13',NULL,0.00,NULL,32),(75,NULL,NULL,'','','absent','2026-01-13',NULL,0.00,NULL,33),(76,NULL,NULL,'','','absent','2026-01-13',NULL,0.00,NULL,35),(77,NULL,NULL,'','','absent','2026-01-13',NULL,0.00,NULL,36),(78,'2026-01-14 07:54:27.639804','2026-01-14 16:47:49.203994','attendance/login/checkin_1768377266174.jpg','attendance/logout/checkout_1768409267724.jpg','present','2026-01-14',0.00,0.00,8.89,31),(79,NULL,NULL,'','','absent','2026-01-14',NULL,0.00,NULL,25),(80,NULL,NULL,'','','absent','2026-01-14',NULL,0.00,NULL,26),(81,NULL,NULL,'','','absent','2026-01-14',NULL,0.00,NULL,27),(82,NULL,NULL,'','','absent','2026-01-14',NULL,0.00,NULL,28),(83,NULL,NULL,'','','absent','2026-01-14',NULL,0.00,NULL,29),(84,NULL,NULL,'','','absent','2026-01-14',NULL,0.00,NULL,30),(85,NULL,NULL,'','','absent','2026-01-14',NULL,0.00,NULL,32),(86,NULL,NULL,'','','absent','2026-01-14',NULL,0.00,NULL,33),(87,NULL,NULL,'','','absent','2026-01-14',NULL,0.00,NULL,34),(88,NULL,NULL,'','','absent','2026-01-14',NULL,0.00,NULL,35),(89,NULL,NULL,'','','absent','2026-01-14',NULL,0.00,NULL,36),(90,NULL,NULL,'','','absent','2026-01-14',NULL,0.00,NULL,37),(91,'2026-01-15 07:09:05.357891',NULL,'attendance/login/checkin_1768460943919.jpg','','present','2026-01-15',NULL,0.00,NULL,27),(92,'2026-01-15 09:33:13.405034',NULL,'attendance/login/checkin_1768469591904.jpg','','present','2026-01-15',NULL,0.00,NULL,31),(93,NULL,NULL,'','','absent','2026-01-15',NULL,0.00,NULL,25),(94,NULL,NULL,'','','absent','2026-01-15',NULL,0.00,NULL,26),(95,NULL,NULL,'','','absent','2026-01-15',NULL,0.00,NULL,28),(96,NULL,NULL,'','','absent','2026-01-15',NULL,0.00,NULL,29),(97,NULL,NULL,'','','absent','2026-01-15',NULL,0.00,NULL,30),(98,NULL,NULL,'','','absent','2026-01-15',NULL,0.00,NULL,32),(99,NULL,NULL,'','','absent','2026-01-15',NULL,0.00,NULL,33),(100,NULL,NULL,'','','absent','2026-01-15',NULL,0.00,NULL,34),(101,NULL,NULL,'','','absent','2026-01-15',NULL,0.00,NULL,35),(102,NULL,NULL,'','','absent','2026-01-15',NULL,0.00,NULL,36),(103,NULL,NULL,'','','absent','2026-01-15',NULL,0.00,NULL,37),(104,'2026-01-16 09:03:46.474638',NULL,'attendance/login/checkin_1768554225180.jpg','','present','2026-01-16',NULL,0.00,NULL,37),(105,'2026-01-16 09:03:47.266099',NULL,'attendance/login/checkin_1768554225535.jpg','','present','2026-01-16',NULL,0.00,NULL,27),(106,'2026-01-16 09:24:43.591568',NULL,'attendance/login/checkin_1768555483413.jpg','','present','2026-01-16',NULL,0.00,NULL,25),(107,'2026-01-16 11:54:14.000000','2026-01-16 11:56:11.991308','attendance/login/checkin_1768564453294.jpg','attendance/logout/checkout_1768564571234.jpg','present','2026-01-16',0.00,0.00,0.03,28),(108,'2026-01-16 11:55:03.669173',NULL,'attendance/login/checkin_1768564503197.jpg','','present','2026-01-16',NULL,0.00,NULL,35),(109,NULL,NULL,'','','absent','2026-01-16',NULL,0.00,NULL,26),(110,NULL,NULL,'','','absent','2026-01-16',NULL,0.00,NULL,29),(111,NULL,NULL,'','','absent','2026-01-16',NULL,0.00,NULL,30),(112,NULL,NULL,'','','absent','2026-01-16',NULL,0.00,NULL,31),(113,NULL,NULL,'','','absent','2026-01-16',NULL,0.00,NULL,32),(114,NULL,NULL,'','','absent','2026-01-16',NULL,0.00,NULL,33),(115,NULL,NULL,'','','absent','2026-01-16',NULL,0.00,NULL,34),(116,NULL,NULL,'','','absent','2026-01-16',NULL,0.00,NULL,36),(117,'2026-01-17 05:52:15.534806',NULL,'attendance/login/checkin_1768629135366.jpg','','present','2026-01-17',NULL,0.00,NULL,34),(118,'2026-01-17 07:00:08.009635',NULL,'attendance/login/checkin_1768633206468.jpg','','present','2026-01-17',NULL,0.00,NULL,27),(119,'2026-01-17 07:16:51.236323','2026-01-17 17:33:37.470290','attendance/login/checkin_1768634210449.jpg','attendance/logout/checkout_1768671216714.jpg','present','2026-01-17',0.28,0.00,10.28,30),(120,'2026-01-17 07:20:05.533645','2026-01-17 17:27:30.369568','attendance/login/checkin_1768634404528.jpg','attendance/logout/checkout_1768670849243.jpg','present','2026-01-17',0.12,0.00,10.12,37),(121,'2026-01-17 07:48:36.537629',NULL,'attendance/login/checkin_1768636115824.jpg','','present','2026-01-17',NULL,0.00,NULL,25),(122,'2026-01-17 09:28:45.153443',NULL,'attendance/login/checkin_1768642123021.jpg','','present','2026-01-17',NULL,0.00,NULL,35),(123,'2026-01-17 09:43:27.768599',NULL,'attendance/login/checkin_1768643006334.jpg','','present','2026-01-17',NULL,0.00,NULL,31),(124,'2026-01-17 10:06:31.597957',NULL,'attendance/login/checkin_1768644390720.jpg','','present','2026-01-17',NULL,0.00,NULL,28),(125,'2026-01-17 10:24:07.907330',NULL,'attendance/login/checkin_1768645447707.jpg','','present','2026-01-17',NULL,0.00,NULL,33),(126,NULL,NULL,'','','absent','2026-01-17',NULL,0.00,NULL,26),(127,NULL,NULL,'','','absent','2026-01-17',NULL,0.00,NULL,29),(128,NULL,NULL,'','','absent','2026-01-17',NULL,0.00,NULL,32),(129,NULL,NULL,'','','absent','2026-01-17',NULL,0.00,NULL,36),(130,'2026-01-18 05:59:32.254752',NULL,'attendance/login/checkin_1768715972119.jpg','','present','2026-01-18',NULL,0.00,NULL,34),(131,'2026-01-18 06:53:14.722797',NULL,'attendance/login/checkin_1768719193498.jpg','','present','2026-01-18',NULL,0.00,NULL,27),(132,'2026-01-18 07:00:53.225106','2026-01-18 17:36:17.745950','attendance/login/checkin_1768719652095.jpg','attendance/logout/checkout_1768757776535.jpg','present','2026-01-18',0.59,0.00,10.59,37),(133,'2026-01-18 07:23:32.098762',NULL,'attendance/login/checkin_1768721012424.jpg','','present','2026-01-18',NULL,0.00,NULL,26),(134,'2026-01-18 08:03:53.096025',NULL,'attendance/login/checkin_1768723431726.jpg','','present','2026-01-18',NULL,0.00,NULL,31),(135,'2026-01-18 09:49:40.375989',NULL,'attendance/login/checkin_1768729778998.jpg','','present','2026-01-18',NULL,0.00,NULL,35),(136,NULL,NULL,'','','absent','2026-01-18',NULL,0.00,NULL,25),(137,NULL,NULL,'','','absent','2026-01-18',NULL,0.00,NULL,28),(138,NULL,NULL,'','','absent','2026-01-18',NULL,0.00,NULL,29),(139,NULL,NULL,'','','absent','2026-01-18',NULL,0.00,NULL,30),(140,NULL,NULL,'','','absent','2026-01-18',NULL,0.00,NULL,32),(141,NULL,NULL,'','','absent','2026-01-18',NULL,0.00,NULL,33),(142,NULL,NULL,'','','absent','2026-01-18',NULL,0.00,NULL,36),(143,'2026-01-19 05:42:58.304839','2026-01-19 16:09:16.563396','attendance/login/checkin_1768801378183.jpg','attendance/logout/checkout_1768838956417.jpg','present','2026-01-19',0.44,0.00,10.44,29),(144,'2026-01-19 05:48:02.843332',NULL,'attendance/login/checkin_1768801682714.jpg','','present','2026-01-19',NULL,0.00,NULL,34),(145,'2026-01-19 07:00:34.977613',NULL,'attendance/login/checkin_1768806034066.jpg','','present','2026-01-19',NULL,0.00,NULL,27),(146,'2026-01-19 07:10:10.501957','2026-01-19 17:46:26.506875','attendance/login/checkin_1768806609711.jpg','attendance/logout/checkout_1768844785608.jpg','present','2026-01-19',0.60,0.00,10.60,30),(147,'2026-01-19 07:12:00.962675','2026-01-19 17:45:00.545455','attendance/login/checkin_1768806721174.jpg','attendance/logout/checkout_1768844700777.jpg','present','2026-01-19',0.55,0.00,10.55,26),(148,'2026-01-19 07:12:06.666996','2026-01-19 17:39:16.667305','attendance/login/checkin_1768806725767.jpg','attendance/logout/checkout_1768844345630.jpg','present','2026-01-19',0.45,0.00,10.45,37),(149,'2026-01-19 07:15:35.269544',NULL,'attendance/login/checkin_1768806934887.jpg','','present','2026-01-19',NULL,0.00,NULL,35),(150,'2026-01-19 07:15:49.709444','2026-01-19 17:40:53.925594','attendance/login/checkin_1768806949255.jpg','attendance/logout/checkout_1768844453657.jpg','present','2026-01-19',0.42,0.00,10.42,32),(151,'2026-01-19 09:02:57.800825','2026-01-19 17:44:53.338177','attendance/login/checkin_1768813377688.jpg','attendance/logout/checkout_1768844693158.jpg','present','2026-01-19',0.00,0.00,8.70,25),(152,'2026-01-19 14:59:02.019257',NULL,'attendance/login/checkin_1768834740475.jpg','','present','2026-01-19',NULL,0.00,NULL,31),(153,NULL,NULL,'','','absent','2026-01-19',NULL,0.00,NULL,28),(154,NULL,NULL,'','','absent','2026-01-19',NULL,0.00,NULL,33),(155,NULL,NULL,'','','absent','2026-01-19',NULL,0.00,NULL,36),(156,'2026-01-20 05:25:01.037547','2026-01-20 17:48:08.044571','attendance/login/checkin_1768886699901.jpg','attendance/logout/checkout_1768931287103.jpg','present','2026-01-20',2.39,0.00,12.39,29),(157,'2026-01-20 05:37:02.431713','2026-01-20 17:38:37.634461','attendance/login/checkin_1768887421544.jpg','attendance/logout/checkout_1768930717247.jpg','present','2026-01-20',2.03,0.00,12.03,32),(158,'2026-01-20 06:58:28.776303',NULL,'attendance/login/checkin_1768892308215.jpg','','present','2026-01-20',NULL,0.00,NULL,27),(159,'2026-01-20 07:52:38.695586','2026-01-20 17:56:19.255790','attendance/login/checkin_1768895558266.jpg','attendance/logout/checkout_1768931778878.jpg','present','2026-01-20',0.06,0.00,10.06,25),(160,'2026-01-20 17:33:14.447401',NULL,'attendance/login/checkin_1768930393077.jpg','','present','2026-01-20',NULL,0.00,NULL,31),(161,NULL,NULL,'','','absent','2026-01-20',NULL,0.00,NULL,26),(162,NULL,NULL,'','','absent','2026-01-20',NULL,0.00,NULL,28),(163,NULL,NULL,'','','absent','2026-01-20',NULL,0.00,NULL,30),(164,NULL,NULL,'','','absent','2026-01-20',NULL,0.00,NULL,33),(165,NULL,NULL,'','','absent','2026-01-20',NULL,0.00,NULL,34),(166,NULL,NULL,'','','absent','2026-01-20',NULL,0.00,NULL,35),(167,NULL,NULL,'','','absent','2026-01-20',NULL,0.00,NULL,36),(168,NULL,NULL,'','','absent','2026-01-20',NULL,0.00,NULL,37),(169,'2026-01-21 05:06:15.125779','2026-01-21 14:43:48.011787','attendance/login/checkin_1768971973627.jpg','attendance/logout/checkout_1769006627582.jpg','present','2026-01-21',0.00,0.00,9.63,32),(170,'2026-01-21 06:00:35.456156','2026-01-21 16:27:42.426961','attendance/login/checkin_1768975235247.jpg','attendance/logout/checkout_1769012861830.jpg','present','2026-01-21',0.45,0.00,10.45,29),(171,'2026-01-21 06:59:37.890369',NULL,'attendance/login/checkin_1768978776440.jpg','','present','2026-01-21',NULL,0.00,NULL,31),(172,'2026-01-21 07:20:03.985903','2026-01-21 17:34:44.295889','attendance/login/checkin_1768979994549.jpg','attendance/logout/checkout_1769016876341.jpg','present','2026-01-21',0.24,0.00,10.24,37),(173,'2026-01-21 08:19:30.014542',NULL,'attendance/login/checkin_1768983569882.jpg','','present','2026-01-21',NULL,0.00,NULL,34),(174,'2026-01-21 08:19:41.344666',NULL,'attendance/login/checkin_1768983580445.jpg','','present','2026-01-21',NULL,0.00,NULL,30),(175,'2026-01-21 08:21:52.306715',NULL,'attendance/login/checkin_1768983711568.jpg','','present','2026-01-21',NULL,0.00,NULL,26),(176,'2026-01-21 08:37:53.616780',NULL,'attendance/login/checkin_1768984673512.jpg','','present','2026-01-21',NULL,0.00,NULL,25),(177,'2026-01-21 10:05:44.758993',NULL,'attendance/login/checkin_1768989943662.jpg','','present','2026-01-21',NULL,0.00,NULL,35),(178,NULL,NULL,'','','absent','2026-01-21',NULL,0.00,NULL,27),(179,NULL,NULL,'','','absent','2026-01-21',NULL,0.00,NULL,28),(180,NULL,NULL,'','','absent','2026-01-21',NULL,0.00,NULL,33),(181,NULL,NULL,'','','absent','2026-01-21',NULL,0.00,NULL,36),(182,'2026-01-22 05:03:49.909567','2026-01-22 15:33:47.626481','attendance/login/checkin_1769058229621.jpg','attendance/logout/checkout_1769096027241.jpg','present','2026-01-22',0.50,0.00,10.50,32),(183,'2026-01-22 05:56:56.878363',NULL,'attendance/login/checkin_1769061416676.jpg','','present','2026-01-22',NULL,0.00,NULL,34),(184,'2026-01-22 06:56:03.875764',NULL,'attendance/login/checkin_1769064962999.jpg','','present','2026-01-22',NULL,0.00,NULL,27),(185,'2026-01-22 07:24:23.853459','2026-01-22 17:34:10.226399','attendance/login/checkin_1769066662921.jpg','attendance/logout/checkout_1769103249496.jpg','present','2026-01-22',0.16,0.00,10.16,30),(186,'2026-01-22 07:28:09.407268','2026-01-22 17:33:46.295380','attendance/login/checkin_1769066887579.jpg','attendance/logout/checkout_1769103224369.jpg','present','2026-01-22',0.09,0.00,10.09,37),(187,'2026-01-22 07:38:00.167579',NULL,'attendance/login/checkin_1769067479719.jpg','','present','2026-01-22',NULL,0.00,NULL,25),(188,'2026-01-22 10:40:28.684380',NULL,'attendance/login/checkin_1769078427262.jpg','','present','2026-01-22',NULL,0.00,NULL,35),(189,'2026-01-22 12:19:29.601536',NULL,'attendance/login/checkin_1769084368255.jpg','','present','2026-01-22',NULL,0.00,NULL,31),(190,NULL,NULL,'','','absent','2026-01-22',NULL,0.00,NULL,26),(191,NULL,NULL,'','','absent','2026-01-22',NULL,0.00,NULL,28),(192,NULL,NULL,'','','absent','2026-01-22',NULL,0.00,NULL,29),(193,NULL,NULL,'','','absent','2026-01-22',NULL,0.00,NULL,33),(194,NULL,NULL,'','','absent','2026-01-22',NULL,0.00,NULL,36),(195,'2026-01-23 05:10:13.598206',NULL,'attendance/login/checkin_1769145012457.jpg','','present','2026-01-23',NULL,0.00,NULL,32),(196,'2026-01-23 05:35:17.518384',NULL,'attendance/login/checkin_1769146516730.jpg','','present','2026-01-23',NULL,0.00,NULL,29),(197,'2026-01-23 05:52:12.869203',NULL,'attendance/login/checkin_1769147532751.jpg','','present','2026-01-23',NULL,0.00,NULL,34),(198,'2026-01-23 07:10:43.401462',NULL,'attendance/login/checkin_1769152242735.jpg','','present','2026-01-23',NULL,0.00,NULL,27),(199,'2026-01-23 07:17:50.844458',NULL,'attendance/login/checkin_1769152670991.jpg','','present','2026-01-23',NULL,0.00,NULL,26),(200,'2026-01-23 07:22:10.588026',NULL,'attendance/login/checkin_1769152929691.jpg','','present','2026-01-23',NULL,0.00,NULL,30),(201,'2026-01-23 07:42:54.351019',NULL,'attendance/login/checkin_1769154173055.jpg','','present','2026-01-23',NULL,0.00,NULL,37),(202,'2026-01-23 09:11:55.789057',NULL,'attendance/login/checkin_1769159515326.jpg','','present','2026-01-23',NULL,0.00,NULL,35);
/*!40000 ALTER TABLE `employee_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_employee`
--

DROP TABLE IF EXISTS `employee_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_employee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `phone` varchar(15) NOT NULL,
  `address` longtext,
  `emergency_contact` varchar(15) DEFAULT NULL,
  `joining_date` date NOT NULL,
  `base_salary` decimal(10,2) NOT NULL,
  `shift_in` time(6) DEFAULT NULL,
  `shift_out` time(6) DEFAULT NULL,
  `overtime_multiplier` decimal(4,2) NOT NULL,
  `working_hours` decimal(4,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `branch_id` bigint NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `role_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `employee_employee_branch_id_ceb1edd6_fk_company_branch_id` (`branch_id`),
  KEY `employee_employee_role_id_a4c099f1_fk_employee_role_id` (`role_id`),
  CONSTRAINT `employee_employee_branch_id_ceb1edd6_fk_company_branch_id` FOREIGN KEY (`branch_id`) REFERENCES `company_branch` (`id`),
  CONSTRAINT `employee_employee_role_id_a4c099f1_fk_employee_role_id` FOREIGN KEY (`role_id`) REFERENCES `employee_role` (`id`),
  CONSTRAINT `employee_employee_user_id_2dd26fdc_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_employee`
--

LOCK TABLES `employee_employee` WRITE;
/*!40000 ALTER TABLE `employee_employee` DISABLE KEYS */;
INSERT INTO `employee_employee` VALUES (25,'ASAD SHAIKH','SAHIKHASAD859@GMAIL.COM','8849422705','NEAR AHAD SPORTS CLUB','','2016-12-21',17000.00,'09:00:00.000000','18:00:00.000000',1.00,10.00,'active','2026-01-08 07:02:40.373685',2,17,3),(26,'NIZAM KHAN','NK6356014@GMAIL.COM','7862903286','FATEHVADI JUHAPURA',NULL,'2025-08-05',10000.00,'13:00:00.000000','23:00:00.000000',1.00,10.00,'active','2026-01-08 07:02:40.711850',2,18,2),(27,'FAIZAN SHAIKH','FS2277837@GMAIL,COM','9316125344','FATEHVADI JUHAPURA',NULL,'2019-06-12',12000.00,'12:00:00.000000','23:00:00.000000',1.00,11.00,'active','2026-01-08 07:02:40.990968',3,19,3),(28,'ADNAN WARSI .','ADNANWARSI5507@GMAIL.COM','7433995507','RONAK PARK JUHAPURA',NULL,'2021-11-12',13000.00,'22:30:00.000000','21:00:00.000000',1.00,10.00,'active','2026-01-08 07:02:41.235386',1,20,2),(29,'SAIYED RUSHAN','SAIYEDRUSHAN476@GMAIL.COM','9106604285','JAMALPUR',NULL,'2024-10-10',10000.00,'22:30:00.000000','21:00:00.000000',1.00,10.00,'active','2026-01-08 07:02:41.483568',1,21,2),(30,'AFFAN SHAIKH','AFVANSHAIKH55@GMAIL.COM','9998738361','DANILIMDA',NULL,'2024-11-22',10000.00,'13:00:00.000000','23:00:00.000000',1.00,10.00,'active','2026-01-08 07:02:41.817792',2,22,2),(31,'AMAN KHALIANI','AMANKHALANI786@GMAIL.COM','9104260308','NA',NULL,'2025-11-01',8000.00,'15:30:00.000000','23:00:00.000000',1.00,10.00,'active','2026-01-08 07:02:42.106869',3,23,2),(32,'SHAIKH MASOOM ALI ','SHAIKHMASOOMALI2@GMAIL,COM','8141505049','JAMALPUR',NULL,'2022-01-01',10000.00,'13:00:00.000000','23:00:00.000000',1.00,10.00,'active','2026-01-08 07:02:42.367254',1,24,2),(33,'HASAN SHAIKH','HASANSHAIKH7668@GMAIL.COM','6351951725','JUHAPURA',NULL,'2023-07-01',11000.00,'13:00:00.000000','23:00:00.000000',1.00,10.00,'active','2026-01-08 07:02:42.619617',1,25,2),(34,'PATHAN SAKIB KHAN','PATHANSAKIBKHAN@GMAIL.COM','8200159741','FATEHVADI',NULL,'2021-02-15',15000.00,'22:30:00.000000','21:00:00.000000',1.00,10.00,'active','2026-01-08 07:02:42.884957',2,26,2),(35,'AAKIB SHAIKH','SHAIKH.AK1999@GMAIL.COM','9664551270','FATEHVADI',NULL,'2014-03-11',17000.00,'13:30:00.000000','23:00:00.000000',1.00,9.00,'active','2026-01-08 07:02:43.151372',1,27,3),(36,'SAHNAWAZ MISTRY','SC8160608529@GMAIL.COM','816068529','CHIPAVADI',NULL,'2017-07-24',15000.00,'13:00:00.000000','23:00:00.000000',1.00,10.00,'active','2026-01-08 07:02:43.411623',1,28,3),(37,'SHAIKH ADNAN','MINIG9898@GMAIL.COM','9824041586','DANILIMDA',NULL,'2025-12-31',8000.00,'13:00:00.000000','23:00:00.000000',1.00,10.00,'active','2026-01-08 07:02:43.671286',3,29,2);
/*!40000 ALTER TABLE `employee_employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_leave`
--

DROP TABLE IF EXISTS `employee_leave`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_leave` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `leave_date` date NOT NULL,
  `notes` longtext,
  `created_at` datetime(6) NOT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `employee_leave_employee_id_60d928f8_fk_employee_employee_id` (`employee_id`),
  CONSTRAINT `employee_leave_employee_id_60d928f8_fk_employee_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_leave`
--

LOCK TABLES `employee_leave` WRITE;
/*!40000 ALTER TABLE `employee_leave` DISABLE KEYS */;
/*!40000 ALTER TABLE `employee_leave` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_leaveswaprequest`
--

DROP TABLE IF EXISTS `employee_leaveswaprequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_leaveswaprequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `from_employee_id` bigint NOT NULL,
  `from_leave_id` bigint NOT NULL,
  `to_employee_id` bigint NOT NULL,
  `to_leave_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `employee_leaveswapre_from_employee_id_6e7eeeea_fk_employee_` (`from_employee_id`),
  KEY `employee_leaveswapre_from_leave_id_9e6f97f6_fk_employee_` (`from_leave_id`),
  KEY `employee_leaveswapre_to_employee_id_deb2461a_fk_employee_` (`to_employee_id`),
  KEY `employee_leaveswapre_to_leave_id_f04a6b68_fk_employee_` (`to_leave_id`),
  CONSTRAINT `employee_leaveswapre_from_employee_id_6e7eeeea_fk_employee_` FOREIGN KEY (`from_employee_id`) REFERENCES `employee_employee` (`id`),
  CONSTRAINT `employee_leaveswapre_from_leave_id_9e6f97f6_fk_employee_` FOREIGN KEY (`from_leave_id`) REFERENCES `employee_leave` (`id`),
  CONSTRAINT `employee_leaveswapre_to_employee_id_deb2461a_fk_employee_` FOREIGN KEY (`to_employee_id`) REFERENCES `employee_employee` (`id`),
  CONSTRAINT `employee_leaveswapre_to_leave_id_f04a6b68_fk_employee_` FOREIGN KEY (`to_leave_id`) REFERENCES `employee_leave` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_leaveswaprequest`
--

LOCK TABLES `employee_leaveswaprequest` WRITE;
/*!40000 ALTER TABLE `employee_leaveswaprequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `employee_leaveswaprequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_monthlyleaveitem`
--

DROP TABLE IF EXISTS `employee_monthlyleaveitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_monthlyleaveitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `leave_date` date NOT NULL,
  `status` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` bigint DEFAULT NULL,
  `request_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_leave_date_per_request` (`request_id`,`leave_date`),
  KEY `employee_monthlyleav_approved_by_id_01a37c02_fk_accounts_` (`approved_by_id`),
  CONSTRAINT `employee_monthlyleav_approved_by_id_01a37c02_fk_accounts_` FOREIGN KEY (`approved_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `employee_monthlyleav_request_id_75cb80af_fk_employee_` FOREIGN KEY (`request_id`) REFERENCES `employee_monthlyleaverequest` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_monthlyleaveitem`
--

LOCK TABLES `employee_monthlyleaveitem` WRITE;
/*!40000 ALTER TABLE `employee_monthlyleaveitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `employee_monthlyleaveitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_monthlyleaverequest`
--

DROP TABLE IF EXISTS `employee_monthlyleaverequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_monthlyleaverequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `aggregate_status` varchar(20) NOT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `employee_monthlyleav_employee_id_7e969dfe_fk_employee_` (`employee_id`),
  CONSTRAINT `employee_monthlyleav_employee_id_7e969dfe_fk_employee_` FOREIGN KEY (`employee_id`) REFERENCES `employee_employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_monthlyleaverequest`
--

LOCK TABLES `employee_monthlyleaverequest` WRITE;
/*!40000 ALTER TABLE `employee_monthlyleaverequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `employee_monthlyleaverequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_paidleaverequest`
--

DROP TABLE IF EXISTS `employee_paidleaverequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_paidleaverequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `leave_date` date NOT NULL,
  `replace_with_date` date DEFAULT NULL,
  `reason` longtext,
  `status` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` bigint DEFAULT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_employee_paid_leave_request` (`employee_id`,`leave_date`),
  KEY `employee_paidleavere_approved_by_id_fbe1b152_fk_accounts_` (`approved_by_id`),
  CONSTRAINT `employee_paidleavere_approved_by_id_fbe1b152_fk_accounts_` FOREIGN KEY (`approved_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `employee_paidleavere_employee_id_822e1368_fk_employee_` FOREIGN KEY (`employee_id`) REFERENCES `employee_employee` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_paidleaverequest`
--

LOCK TABLES `employee_paidleaverequest` WRITE;
/*!40000 ALTER TABLE `employee_paidleaverequest` DISABLE KEYS */;
INSERT INTO `employee_paidleaverequest` VALUES (1,'2026-01-11','2026-01-11',NULL,'pending','2026-01-11 08:07:05.132617','2026-01-11 08:07:05.132641',NULL,33),(2,'2026-01-11','2026-01-11',NULL,'pending','2026-01-11 10:32:13.819812','2026-01-11 10:32:13.819829',NULL,37),(3,'2026-01-12','2026-01-12',NULL,'pending','2026-01-12 10:07:28.594925','2026-01-12 10:07:28.594954',NULL,35),(4,'2026-01-17','2026-01-17',NULL,'pending','2026-01-17 09:31:08.366991','2026-01-17 09:31:08.367010',NULL,35);
/*!40000 ALTER TABLE `employee_paidleaverequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_role`
--

DROP TABLE IF EXISTS `employee_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_role`
--

LOCK TABLES `employee_role` WRITE;
/*!40000 ALTER TABLE `employee_role` DISABLE KEYS */;
INSERT INTO `employee_role` VALUES (1,'POS'),(2,'Sales Executive'),(3,'Manager'),(4,'Team Lead');
/*!40000 ALTER TABLE `employee_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_salary`
--

DROP TABLE IF EXISTS `employee_salary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_salary` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `month` smallint unsigned NOT NULL,
  `year` smallint unsigned NOT NULL,
  `base_salary` decimal(10,2) NOT NULL,
  `overtime_salary` decimal(10,2) NOT NULL,
  `commission` decimal(10,2) NOT NULL,
  `deduction` decimal(10,2) NOT NULL,
  `paid_amount` decimal(10,2) DEFAULT NULL,
  `status` varchar(15) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `paid_at` date DEFAULT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_salary_employee_id_month_year_8bb5f689_uniq` (`employee_id`,`month`,`year`),
  CONSTRAINT `employee_salary_employee_id_f96fd344_fk_employee_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee_employee` (`id`),
  CONSTRAINT `employee_salary_chk_1` CHECK ((`month` >= 0)),
  CONSTRAINT `employee_salary_chk_2` CHECK ((`year` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_salary`
--

LOCK TABLES `employee_salary` WRITE;
/*!40000 ALTER TABLE `employee_salary` DISABLE KEYS */;
INSERT INTO `employee_salary` VALUES (16,1,2026,1645.17,3.29,0.00,619.68,0.00,'pending','2026-01-09 15:00:40.879561',NULL,25),(17,1,2026,322.58,17.74,0.00,0.00,0.00,'pending','2026-01-09 15:00:40.891264',NULL,26),(18,1,2026,0.00,0.00,0.00,0.00,0.00,'pending','2026-01-09 15:00:40.904403',NULL,27),(19,1,2026,838.70,0.00,0.00,837.04,0.00,'pending','2026-01-09 15:00:40.914848',NULL,28),(20,1,2026,967.74,105.81,0.00,0.00,0.00,'pending','2026-01-09 15:00:40.926824',NULL,29),(21,1,2026,6774.18,273.22,0.00,142.58,0.00,'pending','2026-01-09 15:00:40.935054',NULL,30),(22,1,2026,258.06,0.00,0.00,28.65,0.00,'pending','2026-01-09 15:00:40.945933',NULL,31),(23,1,2026,1290.32,95.16,0.00,11.94,0.00,'pending','2026-01-09 15:00:40.956419',NULL,32),(24,1,2026,0.00,0.00,0.00,0.00,0.00,'pending','2026-01-09 15:00:40.967658',NULL,33),(25,1,2026,3870.96,61.44,0.00,0.00,0.00,'pending','2026-01-09 15:00:40.976573',NULL,34),(26,1,2026,0.00,0.00,0.00,0.00,0.00,'pending','2026-01-09 15:00:40.986247',NULL,35),(27,1,2026,0.00,0.00,0.00,0.00,0.00,'pending','2026-01-09 15:00:40.994517',NULL,36),(28,1,2026,4903.14,38.45,0.00,370.05,0.00,'pending','2026-01-09 15:00:41.003517',NULL,37);
/*!40000 ALTER TABLE `employee_salary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_salescommission`
--

DROP TABLE IF EXISTS `employee_salescommission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_salescommission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `month` varchar(7) NOT NULL,
  `total_sales` decimal(15,2) NOT NULL,
  `total_commission` decimal(15,2) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `salesperson_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_salescommission_salesperson_id_month_145d0f07_uniq` (`salesperson_id`,`month`),
  CONSTRAINT `employee_salescommis_salesperson_id_0c184115_fk_employee_` FOREIGN KEY (`salesperson_id`) REFERENCES `employee_employee` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_salescommission`
--

LOCK TABLES `employee_salescommission` WRITE;
/*!40000 ALTER TABLE `employee_salescommission` DISABLE KEYS */;
INSERT INTO `employee_salescommission` VALUES (16,'2026-01',0.00,0.00,'2026-01-09 15:00:40.886626',25),(17,'2026-01',0.00,0.00,'2026-01-09 15:00:40.898642',26),(18,'2026-01',0.00,0.00,'2026-01-09 15:00:40.909605',27),(19,'2026-01',0.00,0.00,'2026-01-09 15:00:40.920032',28),(20,'2026-01',0.00,0.00,'2026-01-09 15:00:40.931180',29),(21,'2026-01',0.00,0.00,'2026-01-09 15:00:40.939514',30),(22,'2026-01',0.00,0.00,'2026-01-09 15:00:40.950377',31),(23,'2026-01',0.00,0.00,'2026-01-09 15:00:40.962026',32),(24,'2026-01',0.00,0.00,'2026-01-09 15:00:40.972376',33),(25,'2026-01',0.00,0.00,'2026-01-09 15:00:40.981919',34),(26,'2026-01',0.00,0.00,'2026-01-09 15:00:40.990306',35),(27,'2026-01',0.00,0.00,'2026-01-09 15:00:40.999461',36),(28,'2026-01',0.00,0.00,'2026-01-09 15:00:41.007929',37);
/*!40000 ALTER TABLE `employee_salescommission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_bill`
--

DROP TABLE IF EXISTS `pos_bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pos_bill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bill_number` varchar(50) DEFAULT NULL,
  `bill_name` varchar(150) DEFAULT NULL,
  `date` datetime(6) NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `total_discount` decimal(12,2) NOT NULL,
  `total_taxable_value` decimal(12,2) DEFAULT NULL,
  `final_amount` decimal(12,2) NOT NULL,
  `is_gst` tinyint(1) NOT NULL,
  `total_cgst` decimal(12,2) DEFAULT NULL,
  `total_sgst` decimal(12,2) DEFAULT NULL,
  `total_igst` decimal(12,2) DEFAULT NULL,
  `branch_id` bigint NOT NULL,
  `customer_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pos_bill_branch_id_256f3799_fk_company_branch_id` (`branch_id`),
  KEY `pos_bill_customer_id_9b1cc583_fk_pos_customer_id` (`customer_id`),
  CONSTRAINT `pos_bill_branch_id_256f3799_fk_company_branch_id` FOREIGN KEY (`branch_id`) REFERENCES `company_branch` (`id`),
  CONSTRAINT `pos_bill_customer_id_9b1cc583_fk_pos_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `pos_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_bill`
--

LOCK TABLES `pos_bill` WRITE;
/*!40000 ALTER TABLE `pos_bill` DISABLE KEYS */;
/*!40000 ALTER TABLE `pos_bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_billitem`
--

DROP TABLE IF EXISTS `pos_billitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pos_billitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `qty` int unsigned NOT NULL,
  `price` decimal(12,2) NOT NULL,
  `discount_type` varchar(10) DEFAULT NULL,
  `discount_value` decimal(12,2) NOT NULL,
  `final_amount` decimal(12,2) NOT NULL,
  `cgst_percent` decimal(5,2) NOT NULL,
  `sgst_percent` decimal(5,2) NOT NULL,
  `igst_percent` decimal(5,2) NOT NULL,
  `taxable_value` decimal(12,2) NOT NULL,
  `cgst_amount` decimal(12,2) NOT NULL,
  `sgst_amount` decimal(12,2) NOT NULL,
  `igst_amount` decimal(12,2) NOT NULL,
  `total` decimal(12,2) NOT NULL,
  `serial_number` varchar(100) DEFAULT NULL,
  `is_returned` tinyint(1) NOT NULL,
  `bill_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `salesperson_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pos_billitem_bill_id_472456ae_fk_pos_bill_id` (`bill_id`),
  KEY `pos_billitem_product_id_ecde2098_fk_product_product_id` (`product_id`),
  KEY `pos_billitem_salesperson_id_8be80e4b_fk_employee_employee_id` (`salesperson_id`),
  CONSTRAINT `pos_billitem_bill_id_472456ae_fk_pos_bill_id` FOREIGN KEY (`bill_id`) REFERENCES `pos_bill` (`id`),
  CONSTRAINT `pos_billitem_product_id_ecde2098_fk_product_product_id` FOREIGN KEY (`product_id`) REFERENCES `product_product` (`id`),
  CONSTRAINT `pos_billitem_salesperson_id_8be80e4b_fk_employee_employee_id` FOREIGN KEY (`salesperson_id`) REFERENCES `employee_employee` (`id`),
  CONSTRAINT `pos_billitem_chk_1` CHECK ((`qty` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_billitem`
--

LOCK TABLES `pos_billitem` WRITE;
/*!40000 ALTER TABLE `pos_billitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `pos_billitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_customer`
--

DROP TABLE IF EXISTS `pos_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pos_customer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `due_amount` decimal(12,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_customer`
--

LOCK TABLES `pos_customer` WRITE;
/*!40000 ALTER TABLE `pos_customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `pos_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_payment`
--

DROP TABLE IF EXISTS `pos_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pos_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_method` varchar(15) NOT NULL,
  `cash_amount` decimal(12,2) DEFAULT NULL,
  `upi_amount` decimal(12,2) DEFAULT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `payment_date` datetime(6) NOT NULL,
  `bill_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pos_payment_bill_id_6efec208_fk_pos_bill_id` (`bill_id`),
  CONSTRAINT `pos_payment_bill_id_6efec208_fk_pos_bill_id` FOREIGN KEY (`bill_id`) REFERENCES `pos_bill` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_payment`
--

LOCK TABLES `pos_payment` WRITE;
/*!40000 ALTER TABLE `pos_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `pos_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_producttransfer`
--

DROP TABLE IF EXISTS `pos_producttransfer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pos_producttransfer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `notes` longtext,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `from_branch_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `to_branch_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pos_producttransfer_from_branch_id_477d6a14_fk_company_branch_id` (`from_branch_id`),
  KEY `pos_producttransfer_product_id_2a2e2d4c_fk_product_product_id` (`product_id`),
  KEY `pos_producttransfer_to_branch_id_9f810c98_fk_company_branch_id` (`to_branch_id`),
  CONSTRAINT `pos_producttransfer_from_branch_id_477d6a14_fk_company_branch_id` FOREIGN KEY (`from_branch_id`) REFERENCES `company_branch` (`id`),
  CONSTRAINT `pos_producttransfer_product_id_2a2e2d4c_fk_product_product_id` FOREIGN KEY (`product_id`) REFERENCES `product_product` (`id`),
  CONSTRAINT `pos_producttransfer_to_branch_id_9f810c98_fk_company_branch_id` FOREIGN KEY (`to_branch_id`) REFERENCES `company_branch` (`id`),
  CONSTRAINT `pos_producttransfer_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_producttransfer`
--

LOCK TABLES `pos_producttransfer` WRITE;
/*!40000 ALTER TABLE `pos_producttransfer` DISABLE KEYS */;
/*!40000 ALTER TABLE `pos_producttransfer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_replacementbill`
--

DROP TABLE IF EXISTS `pos_replacementbill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pos_replacementbill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `replacement_type` varchar(20) NOT NULL,
  `return_destination` varchar(10) NOT NULL,
  `old_total_amount` decimal(12,2) NOT NULL,
  `new_total_amount` decimal(12,2) NOT NULL,
  `difference_amount` decimal(12,2) NOT NULL,
  `notes` longtext,
  `created_at` datetime(6) NOT NULL,
  `bill_id` bigint NOT NULL,
  `branch_id` bigint NOT NULL,
  `customer_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pos_replacementbill_bill_id_b205d0e1_fk_pos_bill_id` (`bill_id`),
  KEY `pos_replacementbill_branch_id_8b9df99d_fk_company_branch_id` (`branch_id`),
  KEY `pos_replacementbill_customer_id_adfaa17f_fk_pos_customer_id` (`customer_id`),
  CONSTRAINT `pos_replacementbill_bill_id_b205d0e1_fk_pos_bill_id` FOREIGN KEY (`bill_id`) REFERENCES `pos_bill` (`id`),
  CONSTRAINT `pos_replacementbill_branch_id_8b9df99d_fk_company_branch_id` FOREIGN KEY (`branch_id`) REFERENCES `company_branch` (`id`),
  CONSTRAINT `pos_replacementbill_customer_id_adfaa17f_fk_pos_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `pos_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_replacementbill`
--

LOCK TABLES `pos_replacementbill` WRITE;
/*!40000 ALTER TABLE `pos_replacementbill` DISABLE KEYS */;
/*!40000 ALTER TABLE `pos_replacementbill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_replacementitem`
--

DROP TABLE IF EXISTS `pos_replacementitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pos_replacementitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `qty` int unsigned NOT NULL,
  `old_price` decimal(12,2) NOT NULL,
  `new_price` decimal(12,2) NOT NULL,
  `old_serial_number` varchar(100) DEFAULT NULL,
  `new_serial_number` varchar(100) DEFAULT NULL,
  `new_product_id` bigint NOT NULL,
  `old_bill_item_id` bigint DEFAULT NULL,
  `old_product_id` bigint NOT NULL,
  `replacement_bill_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pos_replacementitem_new_product_id_da94f477_fk_product_p` (`new_product_id`),
  KEY `pos_replacementitem_old_bill_item_id_5122fbc7_fk_pos_billitem_id` (`old_bill_item_id`),
  KEY `pos_replacementitem_old_product_id_a2a339b9_fk_product_p` (`old_product_id`),
  KEY `pos_replacementitem_replacement_bill_id_0d1df5b5_fk_pos_repla` (`replacement_bill_id`),
  CONSTRAINT `pos_replacementitem_new_product_id_da94f477_fk_product_p` FOREIGN KEY (`new_product_id`) REFERENCES `product_product` (`id`),
  CONSTRAINT `pos_replacementitem_old_bill_item_id_5122fbc7_fk_pos_billitem_id` FOREIGN KEY (`old_bill_item_id`) REFERENCES `pos_billitem` (`id`),
  CONSTRAINT `pos_replacementitem_old_product_id_a2a339b9_fk_product_p` FOREIGN KEY (`old_product_id`) REFERENCES `product_product` (`id`),
  CONSTRAINT `pos_replacementitem_replacement_bill_id_0d1df5b5_fk_pos_repla` FOREIGN KEY (`replacement_bill_id`) REFERENCES `pos_replacementbill` (`id`),
  CONSTRAINT `pos_replacementitem_chk_1` CHECK ((`qty` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_replacementitem`
--

LOCK TABLES `pos_replacementitem` WRITE;
/*!40000 ALTER TABLE `pos_replacementitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `pos_replacementitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_replacementpayment`
--

DROP TABLE IF EXISTS `pos_replacementpayment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pos_replacementpayment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_method` varchar(10) NOT NULL,
  `cash_amount` decimal(12,2) NOT NULL,
  `upi_amount` decimal(12,2) NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `replacement_bill_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pos_replacementpayme_replacement_bill_id_b10ca649_fk_pos_repla` (`replacement_bill_id`),
  CONSTRAINT `pos_replacementpayme_replacement_bill_id_b10ca649_fk_pos_repla` FOREIGN KEY (`replacement_bill_id`) REFERENCES `pos_replacementbill` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_replacementpayment`
--

LOCK TABLES `pos_replacementpayment` WRITE;
/*!40000 ALTER TABLE `pos_replacementpayment` DISABLE KEYS */;
/*!40000 ALTER TABLE `pos_replacementpayment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_replacementrefund`
--

DROP TABLE IF EXISTS `pos_replacementrefund`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pos_replacementrefund` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `refund_method` varchar(10) NOT NULL,
  `cash_amount` decimal(12,2) NOT NULL,
  `upi_amount` decimal(12,2) NOT NULL,
  `total_refund` decimal(12,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `replacement_bill_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pos_replacementrefun_replacement_bill_id_9af3310b_fk_pos_repla` (`replacement_bill_id`),
  CONSTRAINT `pos_replacementrefun_replacement_bill_id_9af3310b_fk_pos_repla` FOREIGN KEY (`replacement_bill_id`) REFERENCES `pos_replacementbill` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_replacementrefund`
--

LOCK TABLES `pos_replacementrefund` WRITE;
/*!40000 ALTER TABLE `pos_replacementrefund` DISABLE KEYS */;
/*!40000 ALTER TABLE `pos_replacementrefund` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_returnbill`
--

DROP TABLE IF EXISTS `pos_returnbill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pos_returnbill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `total_refund` decimal(12,2) NOT NULL,
  `refund_type` varchar(10) DEFAULT NULL,
  `cash_amount` decimal(12,2) DEFAULT NULL,
  `upi_amount` decimal(12,2) DEFAULT NULL,
  `return_destination` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `bill_id` bigint NOT NULL,
  `branch_id` bigint NOT NULL,
  `customer_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pos_returnbill_bill_id_f8b6ad81_fk_pos_bill_id` (`bill_id`),
  KEY `pos_returnbill_branch_id_3481f761_fk_company_branch_id` (`branch_id`),
  KEY `pos_returnbill_customer_id_8c02e8cc_fk_pos_customer_id` (`customer_id`),
  CONSTRAINT `pos_returnbill_bill_id_f8b6ad81_fk_pos_bill_id` FOREIGN KEY (`bill_id`) REFERENCES `pos_bill` (`id`),
  CONSTRAINT `pos_returnbill_branch_id_3481f761_fk_company_branch_id` FOREIGN KEY (`branch_id`) REFERENCES `company_branch` (`id`),
  CONSTRAINT `pos_returnbill_customer_id_8c02e8cc_fk_pos_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `pos_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_returnbill`
--

LOCK TABLES `pos_returnbill` WRITE;
/*!40000 ALTER TABLE `pos_returnbill` DISABLE KEYS */;
/*!40000 ALTER TABLE `pos_returnbill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_returnitem`
--

DROP TABLE IF EXISTS `pos_returnitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pos_returnitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `qty` int unsigned NOT NULL,
  `price` decimal(12,2) NOT NULL,
  `total_refund` decimal(12,2) NOT NULL,
  `original_bill_item_id` bigint DEFAULT NULL,
  `product_id` bigint NOT NULL,
  `return_bill_id` bigint NOT NULL,
  `salesperson_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pos_returnitem_original_bill_item_id_07c4c198_fk_pos_billitem_id` (`original_bill_item_id`),
  KEY `pos_returnitem_product_id_425854d8_fk_product_product_id` (`product_id`),
  KEY `pos_returnitem_return_bill_id_0a408327_fk_pos_returnbill_id` (`return_bill_id`),
  KEY `pos_returnitem_salesperson_id_27a4b1d1_fk_employee_employee_id` (`salesperson_id`),
  CONSTRAINT `pos_returnitem_original_bill_item_id_07c4c198_fk_pos_billitem_id` FOREIGN KEY (`original_bill_item_id`) REFERENCES `pos_billitem` (`id`),
  CONSTRAINT `pos_returnitem_product_id_425854d8_fk_product_product_id` FOREIGN KEY (`product_id`) REFERENCES `product_product` (`id`),
  CONSTRAINT `pos_returnitem_return_bill_id_0a408327_fk_pos_returnbill_id` FOREIGN KEY (`return_bill_id`) REFERENCES `pos_returnbill` (`id`),
  CONSTRAINT `pos_returnitem_salesperson_id_27a4b1d1_fk_employee_employee_id` FOREIGN KEY (`salesperson_id`) REFERENCES `employee_employee` (`id`),
  CONSTRAINT `pos_returnitem_chk_1` CHECK ((`qty` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_returnitem`
--

LOCK TABLES `pos_returnitem` WRITE;
/*!40000 ALTER TABLE `pos_returnitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `pos_returnitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_brand`
--

DROP TABLE IF EXISTS `product_brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_brand` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `category_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_brand_category_id_3ed64dd7_fk_product_category_id` (`category_id`),
  CONSTRAINT `product_brand_category_id_3ed64dd7_fk_product_category_id` FOREIGN KEY (`category_id`) REFERENCES `product_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=269 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_brand`
--

LOCK TABLES `product_brand` WRITE;
/*!40000 ALTER TABLE `product_brand` DISABLE KEYS */;
INSERT INTO `product_brand` VALUES (1,'APPLE','',1),(2,'SAMSUNG','',1),(3,'XUNDO','',1),(4,'KUVETE','',1),(5,'NJOYNY','',1),(6,'TECH21','',1),(7,'NILLKIN','',1),(8,'HAWOO','',1),(9,'TRENZO','',1),(10,'KDM','',1),(11,'UAG','',1),(12,'X LEVEL','',1),(13,'SPIGEN','',1),(14,'GEAR 4','',1),(15,'BLACK CASE','',1),(16,'POLOKA','',1),(17,'I CON','',1),(18,'G MASK','',1),(19,'KAJSA','',1),(20,'SPACE','',1),(21,'DOYARS','',1),(22,'PIBLUE','',1),(23,'SANTA BARBARA','',1),(24,'SWAROVSKI','',1),(25,'KAPA','',1),(26,'LITO','',1),(27,'GOLDFIRE','',2),(28,'MEIBO','',2),(29,'G RAINO','',2),(30,'NEW GLASS','',2),(31,'MY FLEX','',2),(32,'TREAMS','',2),(33,'I CON','',2),(34,'WOYPOKA','',2),(35,'OTEAR','',2),(36,'MIETUBL','',2),(37,'HAWOO','',2),(38,'BESTEE','',2),(39,'RAINBO','',2),(40,'ANANK','',2),(41,'BULEO','',2),(42,'APPLE','',3),(43,'SAMSUNG','',3),(44,'JTP','',3),(45,'GOLDFIRE','',3),(46,'LYNE','',3),(47,'BASEUS','',3),(48,'LITO','',3),(49,'XUNDO','',3),(50,'BULEO','',3),(51,'REMIX','',3),(52,'WOPOW','',3),(53,'RIVANO','',3),(54,'APPLE','',4),(55,'SAMSUNG','',4),(56,'JTP','',4),(57,'GOLDFIRE','',4),(58,'LUNE','',4),(59,'BASEUS','',4),(60,'LITO','',4),(61,'XUNDO','',4),(62,'BULEO','',4),(63,'REMIX','',4),(64,'WOPOW','',4),(65,'RIVANO','',4),(66,'APPLE','',5),(67,'SAMSUNG','',5),(68,'JTP','',5),(69,'GOLDFIRE','',5),(70,'LUNE','',5),(71,'BASEUS','',5),(72,'LITO','',5),(73,'XUNDO','',5),(74,'BULEO','',5),(75,'REMIX','',5),(76,'WOPOW','',5),(77,'RIVANO','',5),(78,'APPLE','',6),(79,'SAMSUNG','',6),(80,'JTP','',6),(81,'GOLDFIRE','',6),(82,'LYNE','',6),(83,'BASEUS','',6),(84,'LITO','',6),(85,'XUNDO','',6),(86,'BULEO','',6),(87,'REMIX','',6),(88,'WOPOW','',6),(89,'RIVANO','',6),(90,'APPLE','',7),(91,'SAMSUNG','',7),(92,'JTP','',7),(93,'GOLDFIRE','',7),(94,'LYNE','',7),(95,'BASEUS','',7),(96,'LITO','',7),(97,'XUNDO','',7),(98,'BULEO','',7),(99,'REMIX','',7),(100,'WOPOW','',7),(101,'RIVANO','',7),(102,'APPLE','',8),(103,'SAMSUNG','',8),(104,'JTP','',8),(105,'GOLDFIRE','',8),(106,'LUNE','',8),(107,'BASEUS','',8),(108,'LITO','',8),(109,'XUNDO','',8),(110,'BULEO','',8),(111,'REMIX','',8),(112,'WOPOW','',8),(113,'RIVANO','',8),(114,'APPLE','',9),(115,'SAMSUNG','',9),(116,'JTP','',9),(117,'GOLDFIRE','',9),(118,'LUNE','',9),(119,'BASEUS','',9),(120,'LITO','',9),(121,'XUNDO','',9),(122,'BULEO','',9),(123,'REMIX','',9),(124,'WOPOW','',9),(125,'RIVANO','',9),(126,'APPLE','',10),(127,'SAMSUNG','',10),(128,'JTP','',10),(129,'GOLDFIRE','',10),(130,'LUNE','',10),(131,'BASEUS','',10),(132,'LITO','',10),(133,'XUNDO','',10),(134,'BULEO','',10),(135,'REMIX','',10),(136,'WOPOW','',10),(137,'RIVANO','',10),(138,'APPLE','',11),(139,'SAMSUNG','',11),(140,'JTP','',11),(141,'GOLDFIRE','',11),(142,'LUNE','',11),(143,'BASEUS','',11),(144,'LITO','',11),(145,'XUNDO','',11),(146,'BULEO','',11),(147,'REMIX','',11),(148,'WOPOW','',11),(149,'RIVANO','',11),(150,'APPLE','',12),(151,'SAMSUNG','',12),(152,'JTP','',12),(153,'GOLDFIRE','',12),(154,'LUNE','',12),(155,'BASEUS','',12),(156,'LITO','',12),(157,'XUNDO','',12),(158,'BULEO','',12),(159,'REMIX','',12),(160,'WOPOW','',12),(161,'RIVANO','',12),(162,'APPLE','',13),(163,'SAMSUNG','',13),(164,'JTP','',13),(165,'GOLDFIRE','',13),(166,'LUNE','',13),(167,'BASEUS','',13),(168,'LITO','',13),(169,'XUNDO','',13),(170,'BULEO','',13),(171,'REMIX','',13),(172,'WOPOW','',13),(173,'RIVANO','',13),(174,'APPLE','',14),(175,'SAMSUNG','',14),(176,'JTP','',14),(177,'GOLDFIRE','',14),(178,'LUNE','',14),(179,'BASEUS','',14),(180,'LITO','',14),(181,'XUNDO','',14),(182,'BULEO','',14),(183,'REMIX','',14),(184,'WOPOW','',14),(185,'RIVANO','',14),(186,'APPLE','',15),(187,'SAMSUNG','',15),(188,'JTP','',15),(189,'GOLDFIRE','',15),(190,'LUNE','',15),(191,'BASEUS','',15),(192,'LITO','',15),(193,'XUNDO','',15),(194,'BULEO','',15),(195,'REMIX','',15),(196,'WOPOW','',15),(197,'RIVANO','',15),(198,'APPLE','',16),(199,'SAMSUNG','',16),(200,'JTP','',16),(201,'GOLDFIRE','',16),(202,'LUNE','',16),(203,'BASEUS','',16),(204,'LITO','',16),(205,'XUNDO','',16),(206,'BULEO','',16),(207,'REMIX','',16),(208,'WOPOW','',16),(209,'RIVANO','',16),(210,'APPLE','',17),(211,'SAMSUNG','',17),(212,'JTP','',17),(213,'GOLDFIRE','',17),(214,'LUNE','',17),(215,'BASEUS','',17),(216,'LITO','',17),(217,'XUNDO','',17),(218,'BULEO','',17),(219,'REMIX','',17),(220,'WOPOW','',17),(221,'RIVANO','',17),(222,'APPLE','',18),(223,'SAMSUNG','',18),(224,'JTP','',18),(225,'GOLDFIRE','',18),(226,'LUNE','',18),(227,'BASEUS','',18),(228,'LITO','',18),(229,'XUNDO','',18),(230,'BULEO','',18),(231,'REMIX','',18),(232,'WOPOW','',18),(233,'RIVANO','',18),(234,'APPLE','',19),(235,'SAMSUNG','',19),(236,'JTP','',19),(237,'GOLDFIRE','',19),(238,'LUNE','',19),(239,'BASEUS','',19),(240,'LITO','',19),(241,'XUNDO','',19),(242,'BULEO','',19),(243,'REMIX','',19),(244,'WOPOW','',19),(245,'RIVANO','',19),(246,'STUFFCOOL','',6),(247,'GOLDFIRE','',19),(248,'MFISH','',7),(249,'REMAX','',7),(250,'MAXCO','',7),(251,'TRANZO','',14),(252,'ONEPLUS','',3),(253,'SPIGEN','',19),(254,'NOISE','',13),(255,'BOAT','',5),(256,'REALME','',5),(257,'ONEPLUS','',5),(258,'BOAT','',3),(259,'OPPO','',11),(260,'REALME','',11),(261,'ONEPLUS','',11),(262,'MI','',11),(264,'MIETUBL','',4),(265,'U & I','',3),(266,'HUAHONG','',13),(267,'U & I','',5),(268,'GEAR FIT','',10);
/*!40000 ALTER TABLE `product_brand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_category`
--

DROP TABLE IF EXISTS `product_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `commission_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_category_commission_id_9002f114_fk_product_commission_id` (`commission_id`),
  CONSTRAINT `product_category_commission_id_9002f114_fk_product_commission_id` FOREIGN KEY (`commission_id`) REFERENCES `product_commission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_category`
--

LOCK TABLES `product_category` WRITE;
/*!40000 ALTER TABLE `product_category` DISABLE KEYS */;
INSERT INTO `product_category` VALUES (1,'Cover',2),(2,'Tuffun',1),(3,'Earphone',4),(4,'Headphone',4),(5,'Buds',4),(6,'Charger',1),(7,'Power Bank',4),(8,'Speaker',4),(9,'Lamination',3),(10,'Stand',1),(11,'Cable',1),(12,'Wireless Charger',4),(13,'Watch',4),(14,'Pencil',3),(15,'Keyboard',3),(16,'Camera Ring',1),(17,'Watch Belt',1),(18,'Water Pouch',4),(19,'Magsafe Accesories',3);
/*!40000 ALTER TABLE `product_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_commission`
--

DROP TABLE IF EXISTS `product_commission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_commission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `commission_type` varchar(20) NOT NULL,
  `commission_value` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_commission`
--

LOCK TABLES `product_commission` WRITE;
/*!40000 ALTER TABLE `product_commission` DISABLE KEYS */;
INSERT INTO `product_commission` VALUES (1,'2%','percentage',2.00),(2,'5%','percentage',5.00),(3,'3%','percentage',3.00),(4,'1%','percentage',1.00);
/*!40000 ALTER TABLE `product_commission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_hsn`
--

DROP TABLE IF EXISTS `product_hsn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_hsn` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(20) NOT NULL,
  `cgst` decimal(5,2) NOT NULL,
  `sgst` decimal(5,2) NOT NULL,
  `igst` decimal(5,2) NOT NULL,
  `description` longtext,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_hsn_category_id_43d734a9_fk_product_category_id` (`category_id`),
  CONSTRAINT `product_hsn_category_id_43d734a9_fk_product_category_id` FOREIGN KEY (`category_id`) REFERENCES `product_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_hsn`
--

LOCK TABLES `product_hsn` WRITE;
/*!40000 ALTER TABLE `product_hsn` DISABLE KEYS */;
INSERT INTO `product_hsn` VALUES (1,'4002',9.00,9.00,18.00,'Cover',1),(2,'7007',9.00,9.00,18.00,'Tuffun',2),(3,'8518',9.00,9.00,18.00,'Earphone',3),(4,'8518',9.00,9.00,18.00,'Headphone',4),(5,'8518',9.00,9.00,18.00,'buds',5),(6,'8504',9.00,9.00,18.00,'Charger',6),(7,'85044090',9.00,9.00,18.00,'Wireless Charger',12),(8,'8507',9.00,9.00,18.00,'Powerbank',7),(9,'851821',9.00,9.00,18.00,'Speaker',8),(10,'3920',9.00,9.00,18.00,'Lamination',9),(11,'8517',9.00,9.00,18.00,'Stand',10),(13,'8544',9.00,9.00,18.00,'Watch',13),(14,'9113',9.00,9.00,18.00,'Watch Belt',17),(15,'391990',9.00,9.00,18.00,'Camera Ring',16),(16,'4202',6.00,6.00,12.00,'Water Pouch',18),(17,'960990',6.00,6.00,12.00,'Pencil',14),(19,'92071000',9.00,9.00,18.00,'Keyboard',15),(20,'4202',6.00,6.00,12.00,'Magsafe Accesories',19);
/*!40000 ALTER TABLE `product_hsn` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_model`
--

DROP TABLE IF EXISTS `product_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_model` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `subbrand_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_model_subbrand_id_df0eec98_fk_product_subbrand_id` (`subbrand_id`),
  CONSTRAINT `product_model_subbrand_id_df0eec98_fk_product_subbrand_id` FOREIGN KEY (`subbrand_id`) REFERENCES `product_subbrand` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_model`
--

LOCK TABLES `product_model` WRITE;
/*!40000 ALTER TABLE `product_model` DISABLE KEYS */;
INSERT INTO `product_model` VALUES (1,'Iphone 17',1),(2,'161',2);
/*!40000 ALTER TABLE `product_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_product`
--

DROP TABLE IF EXISTS `product_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `purchase_price` decimal(10,2) NOT NULL,
  `selling_price` decimal(10,2) NOT NULL,
  `min_selling_price` decimal(10,2) NOT NULL,
  `commission_type` varchar(20) DEFAULT NULL,
  `commission_value` decimal(10,2) DEFAULT NULL,
  `min_qty_alert` int unsigned NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_warranty_item` tinyint(1) NOT NULL,
  `warranty_period` varchar(5) DEFAULT NULL,
  `brand_id` bigint DEFAULT NULL,
  `category_id` bigint DEFAULT NULL,
  `hsn_id` bigint DEFAULT NULL,
  `model_id` bigint DEFAULT NULL,
  `vendor_id` bigint DEFAULT NULL,
  `subbrand_id` bigint DEFAULT NULL,
  `subcategory_id` bigint DEFAULT NULL,
  `type_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_product_brand_id_fcf1b3f3_fk_product_brand_id` (`brand_id`),
  KEY `product_product_category_id_0c725779_fk_product_category_id` (`category_id`),
  KEY `product_product_hsn_id_d2d5eb1a_fk_product_hsn_id` (`hsn_id`),
  KEY `product_product_model_id_ce11c196_fk_product_model_id` (`model_id`),
  KEY `product_product_vendor_id_49ed2699_fk_vendor_vendor_id` (`vendor_id`),
  KEY `product_product_subbrand_id_4483cda8_fk_product_subbrand_id` (`subbrand_id`),
  KEY `product_product_subcategory_id_b98525d0_fk_product_s` (`subcategory_id`),
  KEY `product_product_type_id_db92a7b7_fk_product_type_id` (`type_id`),
  CONSTRAINT `product_product_brand_id_fcf1b3f3_fk_product_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `product_brand` (`id`),
  CONSTRAINT `product_product_category_id_0c725779_fk_product_category_id` FOREIGN KEY (`category_id`) REFERENCES `product_category` (`id`),
  CONSTRAINT `product_product_hsn_id_d2d5eb1a_fk_product_hsn_id` FOREIGN KEY (`hsn_id`) REFERENCES `product_hsn` (`id`),
  CONSTRAINT `product_product_model_id_ce11c196_fk_product_model_id` FOREIGN KEY (`model_id`) REFERENCES `product_model` (`id`),
  CONSTRAINT `product_product_subbrand_id_4483cda8_fk_product_subbrand_id` FOREIGN KEY (`subbrand_id`) REFERENCES `product_subbrand` (`id`),
  CONSTRAINT `product_product_subcategory_id_b98525d0_fk_product_s` FOREIGN KEY (`subcategory_id`) REFERENCES `product_subcategory` (`id`),
  CONSTRAINT `product_product_type_id_db92a7b7_fk_product_type_id` FOREIGN KEY (`type_id`) REFERENCES `product_type` (`id`),
  CONSTRAINT `product_product_vendor_id_49ed2699_fk_vendor_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendor_vendor` (`id`),
  CONSTRAINT `product_product_chk_1` CHECK ((`min_qty_alert` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=166 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_product`
--

LOCK TABLES `product_product` WRITE;
/*!40000 ALTER TABLE `product_product` DISABLE KEYS */;
INSERT INTO `product_product` VALUES (8,'Apple 20W Doc',630.00,2190.00,1400.00,'percentage',2.00,5,'active','2026-01-08 10:31:09.212798',1,'12',78,6,6,NULL,3,NULL,14,NULL),(9,'Samsung 25W Doc',380.00,1699.00,1000.00,'percentage',2.00,5,'active','2026-01-08 10:35:09.520143',1,'6',79,6,6,NULL,3,NULL,14,NULL),(12,'Samsung 45W Adapter',650.00,3499.00,1200.00,'percentage',2.00,5,'active','2026-01-08 11:01:36.693196',1,'6',79,6,6,NULL,3,NULL,14,NULL),(13,'Apple 30W Doc',1100.00,3800.00,2000.00,'percentage',1.00,2,'active','2026-01-08 11:12:52.935274',1,'12',78,6,6,NULL,3,NULL,14,NULL),(14,'Samsung C to C 1.8Mtr',220.00,1799.00,550.00,'percentage',2.00,5,'active','2026-01-08 12:33:16.816057',1,'6',139,11,6,NULL,3,NULL,41,NULL),(15,'Samsung C to C 1Mtr',190.00,599.00,450.00,'percentage',2.00,5,'active','2026-01-08 12:38:37.075997',1,'6',139,11,6,NULL,3,NULL,41,NULL),(16,'Apple 35W Adapter',1150.00,5800.00,3000.00,'percentage',2.00,2,'active','2026-01-08 13:05:30.449404',1,'12',78,6,6,NULL,3,NULL,14,NULL),(17,'Novus 25W',480.00,1200.00,800.00,'percentage',2.00,3,'active','2026-01-08 13:14:53.583083',1,'6',246,6,6,NULL,5,NULL,14,NULL),(18,'B11 C To C 65W 2Mtr',180.00,500.00,300.00,'percentage',2.00,3,'active','2026-01-08 13:17:46.207300',1,'6',140,11,6,NULL,1,NULL,41,NULL),(19,'JTP-CR-C18 25W',450.00,900.00,650.00,'percentage',2.00,3,'active','2026-01-08 13:20:30.801758',1,'6',80,6,6,NULL,1,NULL,14,NULL),(20,'JTP-CR-C2 160W',550.00,1199.00,900.00,'percentage',2.00,3,'active','2026-01-08 13:22:49.832756',1,'6',80,6,6,NULL,1,NULL,14,NULL),(22,'JT301 USB To Lightning',280.00,550.00,350.00,'percentage',2.00,5,'active','2026-01-08 13:28:28.748846',1,'6',80,6,6,NULL,1,NULL,14,NULL),(23,'JT301 USB To C',280.00,550.00,350.00,'percentage',2.00,3,'active','2026-01-08 13:30:07.254477',1,'6',80,6,6,NULL,1,NULL,14,NULL),(24,'JTP-CB66 2Mtr',250.00,550.00,350.00,'percentage',2.00,3,'active','2026-01-08 13:34:59.040120',1,'6',140,11,6,NULL,1,NULL,41,NULL),(25,'JTP-G1 60W Dual USB C',850.00,1500.00,1200.00,'percentage',2.00,3,'active','2026-01-08 13:39:47.704859',1,'6',80,6,6,NULL,1,NULL,16,NULL),(26,'4C pro 45W C To C',520.00,2499.00,800.00,'percentage',2.00,3,'active','2026-01-08 13:43:26.862039',1,'6',82,6,6,NULL,1,NULL,14,NULL),(27,'Neckband Rover 9',550.00,2499.00,750.00,'percentage',1.00,3,'active','2026-01-08 13:45:59.649620',1,'6',46,3,3,NULL,1,NULL,13,NULL),(28,'JTP-CB85',200.00,999.00,350.00,'percentage',2.00,3,'active','2026-01-08 13:48:08.739021',1,'6',140,11,6,NULL,1,NULL,40,NULL),(29,'22C 25W Adapter',330.00,1899.00,650.00,'percentage',2.00,2,'active','2026-01-08 13:50:40.091891',1,'6',82,6,6,NULL,1,NULL,14,NULL),(30,'LE11 Pro',1550.00,3000.00,1800.00,'percentage',1.00,1,'active','2026-01-08 13:52:57.417369',1,'3',60,4,3,NULL,NULL,NULL,61,NULL),(31,'LE11 Pro',1550.00,3000.00,1800.00,'percentage',1.00,1,'active','2026-01-08 13:53:04.043231',1,'3',60,4,3,NULL,NULL,NULL,61,NULL),(32,'LE02',1800.00,3000.00,2200.00,'percentage',1.00,1,'active','2026-01-08 13:55:12.042007',1,'3',60,4,3,NULL,1,NULL,61,NULL),(33,'Signal 7',70.00,150.00,100.00,'percentage',1.00,1,'active','2026-01-08 14:01:16.277067',0,NULL,46,3,3,NULL,1,NULL,10,NULL),(34,'JTP-OG3 45W',500.00,1000.00,850.00,'percentage',2.00,1,'active','2026-01-08 14:04:30.190022',0,NULL,80,6,6,NULL,1,NULL,14,NULL),(35,'LP09 15W',1680.00,3499.00,1850.00,'percentage',1.00,1,'active','2026-01-08 14:08:12.477750',1,'6',96,7,8,NULL,1,NULL,20,NULL),(36,'J007 22.5W',610.00,1250.00,1250.00,'percentage',1.00,1,'active','2026-01-08 14:10:57.487986',0,NULL,92,7,8,NULL,1,NULL,20,NULL),(37,'PB19 15W',1300.00,2499.00,1700.00,'percentage',1.00,1,'active','2026-01-08 14:12:54.689297',1,'6',92,7,8,NULL,1,NULL,20,NULL),(38,'PB14 22.5W',850.00,1499.00,999.00,'percentage',1.00,1,'active','2026-01-08 14:14:24.348328',1,'6',92,7,8,NULL,1,NULL,20,NULL),(39,'J002 22.5W',2100.00,3000.00,2500.00,'percentage',1.00,1,'active','2026-01-08 14:15:38.120964',1,'6',92,7,8,NULL,1,NULL,20,NULL),(40,'Fiber',100.00,300.00,200.00,'percentage',3.00,1,'active','2026-01-08 14:18:13.229984',0,NULL,237,19,16,NULL,1,NULL,62,NULL),(41,'JTP42 3 in 1',260.00,499.00,350.00,'percentage',2.00,1,'active','2026-01-08 14:19:48.383878',1,'6',80,6,6,NULL,1,NULL,16,NULL),(42,'JTP B30',55.00,199.00,99.00,'percentage',2.00,2,'active','2026-01-08 14:22:57.704919',1,'3',140,11,6,NULL,1,NULL,63,NULL),(43,'Power Bank 14pro 20000mah',1250.00,3999.00,1799.00,'percentage',1.00,1,'active','2026-01-08 14:28:02.324782',1,'6',94,7,8,NULL,1,NULL,19,NULL),(44,'M4 BIKE PHONE HOLDER',220.00,499.00,299.00,'percentage',2.00,1,'active','2026-01-08 14:31:32.300668',0,NULL,129,10,11,NULL,1,NULL,34,NULL),(45,'XDHO-050',1200.00,2499.00,1599.00,'percentage',3.00,1,'active','2026-01-08 14:34:04.145422',0,NULL,241,19,11,NULL,1,NULL,64,NULL),(46,'JTP-S9',120.00,299.00,199.00,'percentage',2.00,2,'active','2026-01-08 14:35:32.281641',0,NULL,128,10,11,NULL,1,NULL,33,NULL),(47,'J-1005 22.5W',1600.00,2499.00,1999.00,'percentage',1.00,1,'active','2026-01-08 14:40:59.413282',1,'6',92,7,8,NULL,1,NULL,20,NULL),(48,'MFISH- CIG 20W',1600.00,2499.00,1799.00,'percentage',1.00,1,'active','2026-01-08 14:44:52.489572',1,'6',248,7,8,NULL,1,NULL,20,NULL),(49,'JTP-107',280.00,599.00,349.00,'percentage',1.00,1,'active','2026-01-08 14:46:58.253314',0,NULL,44,3,3,NULL,1,NULL,10,NULL),(50,'XDOT-059',699.00,999.00,799.00,'percentage',3.00,1,'active','2026-01-08 14:48:32.650680',0,NULL,181,14,17,NULL,1,NULL,55,NULL),(51,'POWERBOX 12 PRO',680.00,2999.00,899.00,'percentage',1.00,1,'active','2026-01-08 14:50:38.916674',1,'6',94,7,8,NULL,1,NULL,19,NULL),(52,'JTP-A3',680.00,999.00,799.00,'percentage',2.00,1,'active','2026-01-08 14:55:22.632220',1,'6',80,6,6,NULL,1,NULL,18,NULL),(53,'JTP-J3610 32W',1050.00,1999.00,1399.00,'percentage',2.00,1,'active','2026-01-08 14:59:01.858383',1,'6',152,12,7,NULL,1,NULL,65,NULL),(54,'MP05',800.00,1499.00,1199.00,'percentage',1.00,1,'active','2026-01-08 15:01:17.336823',1,'3',249,7,8,NULL,1,NULL,20,NULL),(55,'LH01',900.00,1499.00,999.00,'percentage',3.00,1,'active','2026-01-08 15:02:58.301730',0,NULL,240,19,16,NULL,1,NULL,64,NULL),(56,'JT-80',650.00,1499.00,899.00,'percentage',2.00,1,'active','2026-01-08 15:06:56.824131',1,'6',80,6,6,NULL,1,NULL,14,NULL),(57,'MP39 20W',2700.00,3499.00,2999.00,'percentage',1.00,1,'active','2026-01-08 15:10:16.746499',1,'6',250,7,8,NULL,1,NULL,20,NULL),(58,'SP-01',800.00,1499.00,1099.00,'percentage',3.00,1,'active','2026-01-08 15:12:35.593190',0,NULL,251,14,17,NULL,1,NULL,55,NULL),(59,'ML03',300.00,899.00,4549.00,'percentage',2.00,1,'active','2026-01-08 15:15:02.218055',1,'6',148,11,6,NULL,1,NULL,39,NULL),(60,'B16',50.00,149.00,99.00,'percentage',2.00,1,'active','2026-01-08 15:16:51.847710',0,NULL,140,11,6,NULL,1,NULL,63,NULL),(61,'LE03',2600.00,3499.00,2899.00,'percentage',1.00,1,'active','2026-01-08 15:18:30.923435',1,'6',60,4,3,NULL,1,NULL,61,NULL),(62,'B110',280.00,999.00,399.00,'percentage',2.00,1,'active','2026-01-08 15:20:44.671294',1,'6',80,6,6,NULL,1,NULL,16,NULL),(63,'BULLET Z2 ANC',1500.00,2499.00,1699.00,'percentage',1.00,1,'active','2026-01-08 15:24:03.277934',1,'12',252,3,3,NULL,2,NULL,13,NULL),(64,'PPXJ20 22.5W',1900.00,3999.00,2299.00,'percentage',1.00,1,'active','2026-01-08 15:28:04.400763',1,'6',95,7,8,NULL,1,NULL,19,NULL),(65,'JTP-21',260.00,699.00,349.00,'percentage',2.00,1,'active','2026-01-08 15:29:34.653861',0,NULL,128,10,11,NULL,1,NULL,33,NULL),(66,'JT-109',220.00,499.00,299.00,'percentage',1.00,1,'active','2026-01-08 15:31:50.202030',0,NULL,44,3,3,NULL,1,NULL,10,NULL),(67,'MCO-013',250.00,499.00,349.00,'percentage',3.00,1,'active','2026-01-08 15:39:15.373379',0,NULL,237,19,16,NULL,1,NULL,64,NULL),(68,'A2',180.00,449.00,299.00,'percentage',2.00,1,'active','2026-01-08 15:40:52.014723',0,NULL,129,10,11,NULL,1,NULL,33,NULL),(69,'RN HO-17',80.00,199.00,149.00,'percentage',2.00,1,'active','2026-01-08 15:43:13.545118',0,NULL,137,10,11,NULL,1,NULL,32,NULL),(70,'JT-04',70.00,149.00,99.00,'percentage',2.00,1,'active','2026-01-08 15:44:25.937814',0,NULL,140,11,6,NULL,1,NULL,42,NULL),(71,'JT-52',150.00,349.00,249.00,'percentage',2.00,1,'active','2026-01-08 15:49:20.415405',0,NULL,140,11,6,NULL,1,NULL,66,NULL),(72,'JT-51',60.00,149.00,99.00,'percentage',2.00,2,'active','2026-01-08 15:50:32.352548',0,NULL,140,11,6,NULL,1,NULL,67,NULL),(73,'J2214 65 FAST CHARGING',1050.00,1999.00,1499.00,'percentage',2.00,1,'active','2026-01-17 11:09:44.654838',1,'6',80,6,6,NULL,1,NULL,14,NULL),(74,'4',400.00,799.00,649.00,'percentage',2.00,5,'active','2026-01-17 11:12:59.815613',1,'6',80,6,6,NULL,1,NULL,14,NULL),(75,'JTP301 MICRO',300.00,550.00,450.00,'percentage',2.00,3,'active','2026-01-17 11:22:53.687205',1,'6',80,6,6,NULL,1,NULL,14,NULL),(76,'JTP-A13',210.00,799.00,599.00,'percentage',2.00,3,'active','2026-01-17 11:25:42.139502',1,'6',80,6,6,NULL,1,NULL,14,NULL),(77,'JTP-CB38',180.00,699.00,599.00,'percentage',2.00,1,'active','2026-01-17 11:29:48.951767',1,'6',140,11,6,NULL,1,NULL,41,NULL),(78,'JTP-CR-C1 120 W FLASH CHARGE',500.00,1299.00,999.00,'percentage',2.00,1,'active','2026-01-17 11:36:58.934517',1,'6',80,6,6,NULL,1,NULL,14,NULL),(79,'JTP-CB143 4 IN 1 CABLE',380.00,799.00,549.00,'percentage',2.00,1,'active','2026-01-17 12:05:23.771465',1,'6',140,11,6,NULL,1,NULL,40,NULL),(80,'LP08',1650.00,2499.00,1950.00,'percentage',1.00,1,'active','2026-01-17 12:26:08.175052',1,'6',96,7,8,NULL,1,NULL,20,NULL),(81,'J2208 WIRELESS CHARGER',550.00,1299.00,850.00,'percentage',2.00,2,'active','2026-01-17 12:27:48.661772',1,'6',80,6,7,NULL,1,NULL,17,NULL),(82,'RN- CH-68 45W CHARGER',330.00,799.00,449.00,'percentage',2.00,2,'active','2026-01-17 12:29:50.252824',1,'6',89,6,6,NULL,1,NULL,14,NULL),(83,'JTP-A17 45W CHARGER',330.00,699.00,549.00,'percentage',2.00,1,'active','2026-01-17 12:37:14.316310',1,'6',80,6,6,NULL,1,NULL,14,NULL),(84,'JTP-A17 45W CHARGER',330.00,699.00,549.00,'percentage',2.00,1,'active','2026-01-17 12:37:30.535095',1,'6',80,6,6,NULL,1,NULL,14,NULL),(85,'JTP-A17 45W CHARGER',330.00,699.00,549.00,'percentage',2.00,1,'active','2026-01-17 12:37:37.356204',0,NULL,80,6,6,NULL,1,NULL,14,NULL),(86,'B13 MUKTIFUNCTIONL FILL LIGHT',400.00,999.00,550.00,'percentage',3.00,2,'active','2026-01-17 13:09:29.701871',0,NULL,237,19,16,NULL,NULL,NULL,68,NULL),(87,'JTP-PH-01 MAGNATIC STAND',320.00,999.00,499.00,'percentage',2.00,2,'active','2026-01-17 13:12:10.381667',0,NULL,128,10,11,NULL,1,NULL,33,NULL),(88,'CREW NOISEFIT',1050.00,4999.00,1399.00,'percentage',1.00,1,'active','2026-01-17 13:16:22.331035',1,'12',254,13,13,NULL,2,NULL,NULL,NULL),(89,'CREW NOISEFIT',1050.00,4999.00,1399.00,'percentage',1.00,1,'active','2026-01-17 13:16:35.230208',1,'12',254,13,13,NULL,2,NULL,NULL,NULL),(90,'AIRPODS 2',550.00,1299.00,850.00,'percentage',1.00,2,'active','2026-01-17 13:19:46.332573',0,NULL,69,5,3,NULL,1,NULL,NULL,NULL),(91,'AIRPODS PRO 2',450.00,999.00,750.00,'percentage',1.00,1,'active','2026-01-17 13:22:36.956957',0,NULL,69,5,3,NULL,1,NULL,NULL,NULL),(92,'AIRPODS 3 PRO',480.00,1399.00,700.00,'percentage',0.00,1,'active','2026-01-17 13:24:17.057295',0,NULL,69,5,2,NULL,1,NULL,NULL,NULL),(93,'GEN 9 SMART WATVH',650.00,1399.00,900.00,'percentage',1.00,1,'active','2026-01-17 13:27:43.509981',0,NULL,165,13,13,NULL,1,NULL,NULL,NULL),(94,'JTP-X3',400.00,999.00,600.00,'percentage',2.00,1,'active','2026-01-17 13:30:07.543293',1,'6',104,8,9,NULL,1,NULL,22,NULL),(95,'AIRDOPS 115',480.00,2999.00,650.00,'percentage',1.00,2,'active','2026-01-17 13:34:58.431989',1,'12',255,5,3,NULL,2,NULL,NULL,NULL),(96,'REALME BUDS T110',820.00,2999.00,1000.00,'percentage',1.00,2,'active','2026-01-17 13:37:25.719342',1,'12',256,5,3,NULL,2,NULL,NULL,NULL),(97,'BUDS 3R',1450.00,1999.00,1550.00,'percentage',1.00,2,'active','2026-01-17 13:45:17.387237',1,'12',257,5,3,NULL,2,NULL,NULL,NULL),(98,'AIRDOPS LOOP `',1350.00,7990.00,1600.00,'percentage',1.00,1,'active','2026-01-17 13:47:57.454780',1,'12',255,5,3,NULL,2,NULL,NULL,NULL),(99,'ROCKERZ 109',570.00,2490.00,1600.00,'percentage',1.00,1,'active','2026-01-17 13:52:12.617456',1,'12',258,3,3,NULL,2,NULL,13,NULL),(100,'RN BT-72',550.00,1299.00,650.00,'percentage',1.00,1,'active','2026-01-17 13:56:56.920904',1,'6',53,3,3,NULL,1,NULL,13,NULL),(101,'RN BT-13A',280.00,799.00,450.00,'percentage',1.00,1,'active','2026-01-17 13:58:05.922627',1,'6',53,3,3,NULL,1,NULL,13,NULL),(102,'DL129 USB TO TYPE C',160.00,849.00,220.00,'percentage',2.00,2,'active','2026-01-17 14:03:30.940971',1,'6',259,11,6,NULL,2,NULL,42,NULL),(103,'USB TO TYPE C CABLE',160.00,899.00,250.00,'percentage',2.00,2,'active','2026-01-17 14:06:21.365949',1,'6',260,11,6,NULL,NULL,NULL,42,NULL),(104,'USB TO TYPE C CABLE',160.00,849.00,250.00,'percentage',2.00,2,'active','2026-01-17 14:10:55.939541',1,'6',261,11,6,NULL,2,NULL,42,NULL),(105,'USB TYPE C CABLE',145.00,699.00,200.00,'percentage',2.00,2,'active','2026-01-17 14:29:34.408915',1,'6',262,11,6,NULL,2,NULL,42,NULL),(106,'MAGNATIC FAST CHARGER TO USB-C',900.00,2900.00,1800.00,'percentage',2.00,2,'active','2026-01-17 14:39:50.448437',1,'12',138,11,6,NULL,2,NULL,70,NULL),(107,'JTP-PH3',120.00,299.00,150.00,'percentage',2.00,2,'active','2026-01-17 14:47:46.752119',0,NULL,128,10,11,NULL,1,NULL,32,NULL),(108,'JTP A7 50W CHARGER',430.00,999.00,750.00,'percentage',2.00,1,'active','2026-01-17 14:56:38.670740',1,'6',80,6,6,NULL,1,NULL,14,NULL),(109,'RN-HF-24',60.00,149.00,100.00,'percentage',1.00,5,'active','2026-01-19 13:58:21.409741',0,NULL,53,3,3,NULL,1,NULL,10,NULL),(110,'JTP-B16 USB TO LIGHTNING',55.00,149.00,100.00,'percentage',2.00,5,'active','2026-01-19 14:01:49.398402',0,NULL,140,11,6,NULL,1,NULL,63,NULL),(111,'JTP-CR-C12 USB C',120.00,299.00,250.00,'percentage',2.00,5,'active','2026-01-19 14:35:31.804926',1,'6',80,6,6,NULL,1,NULL,14,NULL),(112,'JTP-CR-C7 MICRO',120.00,249.00,299.00,'percentage',2.00,5,'active','2026-01-19 14:39:22.127400',1,'3',80,6,6,NULL,1,NULL,14,NULL),(113,'RN-CB-81',40.00,149.00,100.00,'percentage',2.00,5,'active','2026-01-19 14:43:02.419022',0,NULL,149,11,6,NULL,1,NULL,42,NULL),(114,'PHOTON 34',180.00,999.00,300.00,'percentage',1.00,3,'active','2026-01-19 14:49:31.145859',1,'6',46,3,3,NULL,1,NULL,10,NULL),(115,'PHOTON 4',65.00,599.00,150.00,'percentage',2.00,3,'active','2026-01-19 14:58:23.872875',0,NULL,46,3,3,NULL,1,NULL,10,NULL),(116,'PHOTON 5',85.00,399.00,200.00,'percentage',1.00,3,'active','2026-01-19 15:01:08.329854',0,NULL,46,3,3,NULL,1,NULL,10,NULL),(117,'SIGNAL 6',60.00,499.00,150.00,'percentage',1.00,2,'active','2026-01-21 11:07:13.977906',0,NULL,46,3,3,NULL,1,NULL,10,NULL),(118,'SIGNAL 7',60.00,499.00,150.00,'percentage',1.00,1,'active','2026-01-21 11:10:27.767510',0,NULL,46,3,3,NULL,1,NULL,10,NULL),(119,'JT-53 2M',75.00,499.00,200.00,'percentage',2.00,1,'active','2026-01-21 11:14:50.494321',0,NULL,140,11,NULL,NULL,1,NULL,67,NULL),(120,'MTB-BLHM03',1080.00,1999.00,1400.00,'percentage',1.00,1,'active','2026-01-21 12:56:35.307748',1,'6',264,4,3,NULL,1,NULL,61,NULL),(121,'ROVER 9',550.00,2499.00,750.00,'percentage',0.00,2,'active','2026-01-21 12:59:04.644914',1,'6',46,3,3,NULL,NULL,NULL,13,NULL),(122,'ROVER 12',320.00,1499.00,500.00,'percentage',2.00,1,'active','2026-01-21 13:06:44.509919',1,'6',46,3,3,NULL,1,NULL,13,NULL),(123,'UINB-8199',330.00,2999.00,550.00,'percentage',1.00,1,'active','2026-01-21 13:12:05.182343',1,'6',265,3,3,NULL,1,NULL,13,NULL),(124,'UI-8937`',180.00,699.00,400.00,'percentage',1.00,2,'active','2026-01-21 13:14:22.342900',1,'6',265,3,3,NULL,1,NULL,10,NULL),(125,'JTP-727',950.00,1999.00,1150.00,'percentage',1.00,1,'active','2026-01-21 14:15:11.119007',1,'6',92,7,8,NULL,1,NULL,19,NULL),(126,'ROVER 3 PRO',350.00,3499.00,550.00,'percentage',1.00,2,'active','2026-01-21 14:17:02.680898',1,'6',46,3,3,NULL,1,NULL,13,NULL),(127,'ULTRA 2',340.00,999.00,550.00,'percentage',1.00,1,'active','2026-01-21 14:21:25.938162',0,NULL,165,13,13,NULL,1,NULL,NULL,NULL),(128,'HK29 HERO',1850.00,3999.00,2100.00,'percentage',2.00,1,'active','2026-01-21 14:23:16.704294',0,NULL,266,13,13,NULL,1,NULL,NULL,NULL),(129,'HK28 ULTRA',1850.00,3999.00,2200.00,'percentage',1.00,1,'active','2026-01-21 14:24:10.142936',0,NULL,266,13,13,NULL,1,NULL,NULL,NULL),(130,'JTP-730',1550.00,2999.00,1800.00,'percentage',2.00,1,'active','2026-01-21 14:25:54.970473',1,'6',92,7,8,NULL,1,NULL,19,NULL),(131,'JTP-730',1550.00,2999.00,1800.00,'percentage',2.00,1,'active','2026-01-21 14:26:06.871784',1,'6',92,7,8,NULL,1,NULL,19,NULL),(132,'TWS-7227',530.00,3999.00,850.00,'percentage',1.00,1,'active','2026-01-21 14:27:39.727585',1,'6',267,5,3,NULL,1,NULL,NULL,NULL),(133,'TWS-7020',580.00,3499.00,750.00,'percentage',2.00,1,'active','2026-01-21 14:29:09.862262',1,'6',267,5,3,NULL,1,NULL,NULL,NULL),(134,'JTP-107',240.00,599.00,350.00,'percentage',1.00,1,'active','2026-01-21 14:30:48.639541',1,'6',44,3,3,NULL,1,NULL,10,NULL),(135,'UI-2565',185.00,999.00,300.00,'percentage',1.00,1,'active','2026-01-21 14:32:12.869153',0,NULL,265,3,3,NULL,1,NULL,10,NULL),(136,'JTP-CB58',180.00,599.00,300.00,'percentage',2.00,1,'active','2026-01-21 14:34:51.109123',0,NULL,140,11,NULL,NULL,1,NULL,66,NULL),(137,'JTP-CB57 2M',180.00,599.00,350.00,'percentage',2.00,1,'active','2026-01-21 14:36:25.085117',0,NULL,140,11,NULL,NULL,1,NULL,39,NULL),(138,'TWS-5445',650.00,2499.00,1200.00,'percentage',1.00,1,'active','2026-01-21 14:40:11.879924',1,'6',267,5,3,NULL,1,NULL,NULL,NULL),(139,'JTP-CB38',280.00,599.00,400.00,'percentage',2.00,2,'active','2026-01-21 14:41:22.582189',1,'6',140,11,6,NULL,1,NULL,41,NULL),(140,'M',400.00,799.00,650.00,'percentage',2.00,5,'active','2026-01-21 14:45:06.111004',1,'6',140,11,6,NULL,1,NULL,71,NULL),(141,'JTP-CB39',280.00,599.00,400.00,'percentage',2.00,2,'active','2026-01-21 14:50:42.320643',1,'6',140,11,6,NULL,1,NULL,39,NULL),(142,'JT-70 2M',400.00,799.00,650.00,'percentage',2.00,1,'active','2026-01-21 14:52:45.505468',1,'6',140,11,6,NULL,1,NULL,39,NULL),(143,'JT-65',120.00,499.00,300.00,'percentage',2.00,1,'active','2026-01-21 15:00:14.278781',1,'6',140,11,6,NULL,1,NULL,38,NULL),(144,'JTP-95',250.00,499.00,350.00,'percentage',2.00,1,'active','2026-01-21 15:04:24.690690',1,'6',140,11,6,NULL,1,NULL,39,NULL),(145,'J64',120.00,499.00,350.00,'percentage',2.00,1,'active','2026-01-21 15:07:13.900428',1,'6',140,11,6,NULL,1,NULL,63,NULL),(146,'JTP-B20',120.00,499.00,350.00,'percentage',2.00,1,'active','2026-01-21 15:08:44.807802',1,'6',140,11,6,NULL,1,NULL,42,NULL),(147,'JTP-B8',120.00,499.00,400.00,'percentage',2.00,1,'active','2026-01-21 15:10:47.370402',1,'6',140,11,6,NULL,1,NULL,42,NULL),(148,'RN CH-63',450.00,850.00,700.00,'percentage',2.00,2,'active','2026-01-21 15:43:57.631092',0,NULL,89,6,6,NULL,1,NULL,14,NULL),(149,'jtp-s3',350.00,749.00,500.00,'percentage',2.00,1,'active','2026-01-21 15:48:55.978166',0,NULL,128,10,11,NULL,1,NULL,33,NULL),(150,'MULTIFUNCTION PHOTO CLIP',180.00,399.00,250.00,'percentage',2.00,1,'active','2026-01-21 15:50:49.578121',0,NULL,129,10,11,NULL,1,NULL,36,NULL),(151,'JTP-OG2',350.00,799.00,550.00,'percentage',2.00,2,'active','2026-01-21 16:02:03.033975',1,'6',80,6,6,NULL,1,NULL,14,NULL),(152,'JTP-J012',700.00,1499.00,999.00,'percentage',1.00,1,'active','2026-01-21 16:03:47.641863',1,'6',92,7,8,NULL,1,NULL,20,NULL),(153,'JTP-CR-52',600.00,1199.00,999.00,'percentage',2.00,1,'active','2026-01-21 16:05:17.556339',1,'6',80,6,6,NULL,1,NULL,16,NULL),(154,'JTP-B105',350.00,899.00,600.00,'percentage',2.00,2,'active','2026-01-21 16:06:52.407673',1,'6',80,6,6,NULL,1,NULL,16,NULL),(155,'RN-CR-05',200.00,499.00,350.00,'percentage',2.00,1,'active','2026-01-21 16:13:38.862392',0,NULL,89,6,6,NULL,1,NULL,16,NULL),(156,'RN CR-10',200.00,449.00,300.00,'percentage',2.00,1,'active','2026-01-21 16:14:51.559922',0,NULL,89,6,6,NULL,1,NULL,16,NULL),(157,'RN BT-74',450.00,999.00,650.00,'percentage',1.00,1,'active','2026-01-22 08:36:05.504684',1,'6',53,3,3,NULL,1,NULL,13,NULL),(158,'BIKE PHONE HOLDER',120.00,399.00,250.00,'percentage',2.00,1,'active','2026-01-22 08:37:51.046157',0,NULL,129,10,11,NULL,1,NULL,34,NULL),(159,'JTP-A28 POER BANK CABLE',110.00,349.00,200.00,'percentage',2.00,1,'active','2026-01-22 08:40:31.897382',1,'6',140,11,6,NULL,1,NULL,39,NULL),(160,'JTP-CR-Y5 MAGNATIC CAR HOLDER',650.00,1299.00,950.00,'percentage',2.00,1,'active','2026-01-22 08:53:19.496157',1,'6',80,6,7,NULL,1,NULL,17,NULL),(161,'JTP-718',950.00,1699.00,1300.00,'percentage',1.00,1,'active','2026-01-22 08:59:08.163982',1,'6',92,7,8,NULL,1,NULL,19,NULL),(162,'RN CB-48',90.00,299.00,150.00,'percentage',2.00,1,'active','2026-01-22 09:37:30.810188',0,NULL,149,11,6,NULL,1,NULL,41,NULL),(163,'MP-6',1500.00,3999.00,2100.00,'percentage',1.00,1,'active','2026-01-22 12:17:53.174263',1,'6',99,7,8,NULL,1,NULL,20,NULL),(164,'45W POWER ADAPTER WITH CABLE',2000.00,3499.00,2900.00,'percentage',2.00,2,'active','2026-01-22 12:21:40.626960',1,'12',79,6,6,NULL,2,NULL,14,NULL),(165,'GF-7',200.00,599.00,350.00,'percentage',2.00,1,'active','2026-01-22 12:26:19.466952',0,NULL,268,10,11,NULL,1,NULL,33,NULL);
/*!40000 ALTER TABLE `product_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_quantity`
--

DROP TABLE IF EXISTS `product_quantity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_quantity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `qty` int unsigned NOT NULL,
  `barcode` longtext,
  `updated_at` datetime(6) NOT NULL,
  `branch_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `rack_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_quantity_branch_id_efc6aafc_fk_company_branch_id` (`branch_id`),
  KEY `product_quantity_product_id_6652a7d8_fk_product_product_id` (`product_id`),
  KEY `product_quantity_rack_id_8b366221_fk_product_rack_id` (`rack_id`),
  CONSTRAINT `product_quantity_branch_id_efc6aafc_fk_company_branch_id` FOREIGN KEY (`branch_id`) REFERENCES `company_branch` (`id`),
  CONSTRAINT `product_quantity_product_id_6652a7d8_fk_product_product_id` FOREIGN KEY (`product_id`) REFERENCES `product_product` (`id`),
  CONSTRAINT `product_quantity_rack_id_8b366221_fk_product_rack_id` FOREIGN KEY (`rack_id`) REFERENCES `product_rack` (`id`),
  CONSTRAINT `product_quantity_chk_1` CHECK ((`qty` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=199 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_quantity`
--

LOCK TABLES `product_quantity` WRITE;
/*!40000 ALTER TABLE `product_quantity` DISABLE KEYS */;
INSERT INTO `product_quantity` VALUES (11,13,'CHA2601N0002','2026-01-22 10:01:59.634049',1,8,NULL),(12,9,'CHA2601Q0003','2026-01-22 09:57:57.154068',1,9,NULL),(15,11,'CHA2601Z0006','2026-01-22 09:55:13.594053',1,12,NULL),(16,5,'CHA2601L0007','2026-01-08 12:50:11.623397',1,13,NULL),(17,12,'CAB2601F0005','2026-01-22 09:49:48.041129',1,14,NULL),(18,10,'CAB2601W0004','2026-01-22 09:48:07.372617',1,15,NULL),(19,3,'CHA2601W0008','2026-01-22 12:23:53.693465',1,16,NULL),(20,5,'CHA2601Y0009','2026-01-08 14:51:39.069017',1,17,NULL),(21,4,'CAB2601R0010','2026-01-17 12:30:48.561822',1,18,NULL),(22,4,'CHA2601M0011','2026-01-21 15:27:59.189879',1,19,NULL),(23,3,'CHA2601Z0012','2026-01-21 15:33:10.250267',1,20,NULL),(25,2,'CHA2601G0013','2026-01-21 15:14:15.029236',1,22,NULL),(26,6,'CHA2601V0013','2026-01-21 15:17:21.869357',1,23,NULL),(27,6,'CAB2601L0015','2026-01-08 13:34:59.042668',1,24,NULL),(28,5,'CHA2601D0016','2026-01-08 13:39:47.706178',1,25,NULL),(29,5,'CHA2601M0017','2026-01-22 09:01:49.994651',1,26,NULL),(30,5,'EAR2601U0018','2026-01-21 13:00:16.593788',1,27,NULL),(31,2,'CAB2601K0019','2026-01-08 13:48:08.740805',1,28,NULL),(32,3,'CHA2601G0020','2026-01-21 15:39:33.828187',1,29,NULL),(33,3,'HEA2601D0021','2026-01-08 13:52:57.419172',1,30,NULL),(34,2,'HEA2601M0022','2026-01-08 13:53:04.044734',1,31,NULL),(35,1,'HEA2601T0023','2026-01-08 13:55:12.045060',1,32,NULL),(36,1,'EAR2601P0024','2026-01-08 14:01:16.278899',1,33,NULL),(37,1,'CHA2601B0025','2026-01-08 14:04:30.193192',1,34,NULL),(38,2,'POW2601L0026','2026-01-08 14:08:12.479863',1,35,NULL),(39,2,'POW2601J0027','2026-01-08 14:10:57.489845',1,36,NULL),(40,5,'POW2601E0028','2026-01-08 14:12:54.692583',1,37,NULL),(41,3,'POW2601R0029','2026-01-08 14:14:24.350360',1,38,NULL),(42,1,'POW2601S0030','2026-01-08 14:15:38.122537',1,39,NULL),(43,3,'MAG2601N0031','2026-01-08 14:18:13.231788',1,40,NULL),(44,2,'CHA2601D0032','2026-01-08 14:19:48.385289',1,41,NULL),(45,6,'CAB2601U0033','2026-01-21 15:01:24.779618',1,42,NULL),(46,2,'POW2601G0034','2026-01-21 13:09:30.137968',1,43,NULL),(47,3,'STA2601D0035','2026-01-08 14:31:32.302875',1,44,NULL),(48,1,'MAG2601U0036','2026-01-08 14:34:04.147259',1,45,NULL),(49,4,'STA2601O0037','2026-01-08 14:35:32.283071',1,46,NULL),(50,1,'POW2601I0038','2026-01-08 14:40:59.416380',1,47,NULL),(51,1,'POW2601E0039','2026-01-08 14:44:52.491459',1,48,NULL),(52,1,'EAR2601Z0040','2026-01-08 14:46:58.254880',1,49,NULL),(53,1,'PEN2601X0041','2026-01-08 14:48:32.652485',1,50,NULL),(54,1,'POW2601X0042','2026-01-08 14:50:38.919300',1,51,NULL),(55,3,'CHA2601E0043','2026-01-17 11:37:51.237104',1,52,NULL),(56,1,'WIR2601P0044','2026-01-08 14:59:01.860386',1,53,NULL),(57,2,'POW2601J0045','2026-01-22 10:10:46.694912',1,54,NULL),(58,1,'MAG2601G0046','2026-01-08 15:02:58.303076',1,55,NULL),(59,1,'CHA2601K0047','2026-01-21 15:37:10.059254',1,56,NULL),(60,1,'POW2601B0048','2026-01-08 15:10:16.749085',1,57,NULL),(61,1,'PEN2601S0049','2026-01-08 15:12:35.594698',1,58,NULL),(62,1,'CAB2601D0050','2026-01-08 15:15:02.220270',1,59,NULL),(63,1,'CAB2601L0051','2026-01-08 15:16:51.849365',1,60,NULL),(64,1,'HEA2601D0052','2026-01-08 15:18:30.926045',1,61,NULL),(65,1,'CHA2601E0053','2026-01-08 15:20:44.672851',1,62,NULL),(66,1,'EAR2601I0054','2026-01-22 09:39:23.234530',1,63,NULL),(67,1,'POW2601T0055','2026-01-08 15:28:04.402432',1,64,NULL),(68,1,'STA2601V0056','2026-01-08 15:29:34.655462',1,65,NULL),(69,2,'EAR2601C0057','2026-01-08 15:31:50.203633',1,66,NULL),(70,2,'MAG2601O0058','2026-01-08 15:39:15.375538',1,67,NULL),(71,2,'STA2601B0059','2026-01-08 15:40:52.016819',1,68,NULL),(72,1,'STA2601Y0060','2026-01-08 15:43:13.546911',1,69,NULL),(73,2,'CAB2601L0061','2026-01-08 15:45:17.928541',1,70,NULL),(74,1,'CAB2601D0062','2026-01-08 15:49:20.417207',1,71,NULL),(75,2,'CAB2601T0063','2026-01-08 15:50:32.354047',1,72,NULL),(76,1,'CHA2601E0064','2026-01-17 11:09:44.658211',1,73,NULL),(77,0,'CHA2601S0065','2026-01-17 11:09:44.660978',2,73,NULL),(78,0,'CHA2601J0065','2026-01-21 15:22:06.021571',1,74,NULL),(79,1,'CHA2601Y0066','2026-01-21 15:12:19.148641',1,75,NULL),(80,3,'CHA2601C0067','2026-01-21 11:25:21.868772',1,76,NULL),(81,1,'CAB2601S0068','2026-01-17 11:29:48.953174',1,77,NULL),(82,1,'CHA2601O0069','2026-01-21 15:29:16.503756',1,78,NULL),(83,1,'CAB2601O0070','2026-01-21 14:54:40.672970',1,79,NULL),(84,1,'POW2601N0071','2026-01-17 12:26:08.178194',1,80,NULL),(85,2,'CHA2601V0072','2026-01-17 12:27:48.663511',1,81,NULL),(86,2,'CHA2601W0073','2026-01-22 08:48:35.742299',1,82,NULL),(87,1,'CHA2601L0074','2026-01-17 12:37:14.319123',1,83,NULL),(88,1,'CHA2601F0075','2026-01-17 12:37:30.536933',1,84,NULL),(89,1,'CHA2601K0076','2026-01-17 12:37:37.358077',1,85,NULL),(90,10,'MAG2601H0077','2026-01-17 13:09:29.705007',1,86,NULL),(91,3,'STA2601R0078','2026-01-17 13:12:10.384684',1,87,NULL),(92,2,'WAT2601Q0079','2026-01-17 13:16:22.332763',1,88,NULL),(93,2,'WAT2601P0080','2026-01-17 13:16:35.231678',1,89,NULL),(94,4,'BUD2601E0081','2026-01-17 13:19:46.334471',1,90,NULL),(95,1,'BUD2601R0082','2026-01-17 13:22:36.959827',1,91,NULL),(96,1,'BUD2601H0083','2026-01-17 13:24:17.059726',1,92,NULL),(97,1,'WAT2601G0084','2026-01-21 12:50:13.154044',1,93,NULL),(98,1,'SPE2601B0085','2026-01-17 13:30:07.544986',1,94,NULL),(99,3,'BUD2601R0086','2026-01-22 10:04:39.664396',1,95,NULL),(100,3,'BUD2601T0087','2026-01-22 10:08:44.831421',1,96,NULL),(101,2,'BUD2601I0088','2026-01-22 10:07:21.817568',1,97,NULL),(102,1,'BUD2601Q0089','2026-01-17 13:47:57.457285',1,98,NULL),(103,2,'EAR2601E0090','2026-01-22 10:06:04.413955',1,99,NULL),(104,1,'EAR2601E0091','2026-01-17 13:56:56.924003',1,100,NULL),(105,1,'EAR2601Z0092','2026-01-17 13:58:05.924289',1,101,NULL),(106,5,'CAB2601G0093','2026-01-17 14:03:30.944393',1,102,NULL),(107,5,'CAB2601F0094','2026-01-17 14:06:21.368945',1,103,NULL),(108,5,'CAB2601Z0095','2026-01-17 14:10:55.942480',1,104,NULL),(109,6,'CAB2601D0096','2026-01-17 14:29:34.412088',1,105,NULL),(110,5,'CAB2601F0097','2026-01-17 14:39:50.451928',1,106,NULL),(111,3,'STA2601E0098','2026-01-17 14:47:46.753827',1,107,NULL),(112,1,'CHA2601S0099','2026-01-17 14:56:38.673553',1,108,NULL),(113,34,'EAR2601U0100','2026-01-19 13:58:21.413133',4,109,NULL),(114,23,'CAB2601F0101','2026-01-19 14:01:49.400063',4,110,NULL),(115,9,'CHA2601Z0102','2026-01-19 14:35:31.807887',4,111,NULL),(116,5,'CHA2601F0103','2026-01-19 14:39:22.129459',4,112,NULL),(117,22,'CAB2601V0104','2026-01-19 14:43:02.420891',4,113,NULL),(118,7,'EAR2601G0105','2026-01-19 14:49:31.149156',4,114,NULL),(119,8,'EAR2601I0106','2026-01-19 14:58:23.876251',4,115,NULL),(120,9,'EAR2601B0107','2026-01-19 15:01:08.332645',4,116,NULL),(121,7,'EAR2601H0108','2026-01-21 11:11:11.110532',4,117,NULL),(122,1,'EAR2601N0109','2026-01-21 11:10:27.769025',4,118,NULL),(123,3,'CAB2601A0110','2026-01-21 11:14:50.498324',4,119,NULL),(124,1,'CHA2601C0101','2026-01-21 11:29:18.956721',4,76,NULL),(125,0,'WAT2601A0110','2026-01-21 12:50:13.155693',4,93,NULL),(126,2,'HEA2601L0111','2026-01-21 12:56:35.311275',4,120,NULL),(127,0,'EAR2601Y0112','2026-01-21 13:00:55.047058',4,121,NULL),(128,10,'EAR2601G0112','2026-01-21 13:00:16.598161',4,27,NULL),(129,3,'EAR2601Z0113','2026-01-21 13:06:44.513097',4,122,NULL),(130,1,'POW2601J0113','2026-01-21 13:09:30.141711',4,43,NULL),(131,1,'EAR2601K0114','2026-01-21 13:12:05.185747',4,123,NULL),(132,5,'EAR2601P0115','2026-01-21 13:14:22.346174',4,124,NULL),(133,1,'EAR2601J0115','2026-01-21 13:18:05.600373',4,101,NULL),(134,3,'POW2601P0116','2026-01-21 14:15:11.149500',4,125,NULL),(135,4,'EAR2601J0117','2026-01-21 14:17:02.682490',4,126,NULL),(136,4,'WAT2601T0118','2026-01-21 14:21:25.940981',4,127,NULL),(137,1,'WAT2601R0119','2026-01-21 14:23:16.706844',4,128,NULL),(138,1,'WAT2601W0120','2026-01-21 14:24:10.147685',4,129,NULL),(139,1,'POW2601X0121','2026-01-21 14:25:54.973771',4,130,NULL),(140,1,'POW2601G0122','2026-01-21 14:26:06.873826',4,131,NULL),(141,2,'BUD2601T0123','2026-01-21 14:27:39.729721',4,132,NULL),(142,2,'BUD2601Y0124','2026-01-21 14:29:09.864089',4,133,NULL),(143,2,'EAR2601R0125','2026-01-21 14:30:48.641247',4,134,NULL),(144,1,'EAR2601I0126','2026-01-21 14:32:12.870911',4,135,NULL),(145,4,'CAB2601H0127','2026-01-21 14:34:51.112244',4,136,NULL),(146,5,'CAB2601I0128','2026-01-21 14:36:25.088860',4,137,NULL),(147,1,'BUD2601S0129','2026-01-21 14:40:11.881979',4,138,NULL),(148,5,'CAB2601Y0130','2026-01-21 14:41:22.583885',4,139,NULL),(149,0,'CAB2601B0131','2026-01-21 14:55:07.707437',4,140,NULL),(150,5,'CAB2601U0132','2026-01-21 14:50:42.323382',4,141,NULL),(151,1,'CAB2601H0133','2026-01-21 14:52:45.509359',4,142,NULL),(152,5,'CAB2601U0133','2026-01-21 14:54:40.679048',4,79,NULL),(153,1,'CAB2601G0134','2026-01-21 15:00:14.282954',4,143,NULL),(154,5,'CAB2601H0134','2026-01-21 15:01:24.782717',4,42,NULL),(155,1,'CAB2601U0135','2026-01-21 15:04:24.693205',4,144,NULL),(156,5,'CAB2601U0136','2026-01-21 15:07:13.902390',4,145,NULL),(157,1,'CAB2601D0137','2026-01-21 15:08:44.810979',4,146,NULL),(158,2,'CAB2601F0138','2026-01-21 15:10:47.372366',4,147,NULL),(159,5,'CHA2601C0138','2026-01-21 15:12:19.152305',4,75,NULL),(160,4,'CHA2601U0138','2026-01-21 15:14:15.031954',4,22,NULL),(161,6,'CHA2601U0138','2026-01-21 15:17:21.875113',4,23,NULL),(162,4,'CHA2601X0138','2026-01-21 15:27:59.191477',4,19,NULL),(163,3,'CHA2601Y0138','2026-01-21 15:29:16.506970',4,78,NULL),(164,2,'CHA2601N0138','2026-01-21 15:33:10.251977',4,20,NULL),(165,2,'CHA2601K0138','2026-01-21 15:37:10.061789',4,56,NULL),(166,3,'CHA2601F0138','2026-01-21 15:39:33.831507',4,29,NULL),(167,5,'CHA2601N0139','2026-01-21 15:43:57.633747',4,148,NULL),(168,4,'CHA2601O0139','2026-01-22 09:01:49.996336',4,26,NULL),(169,1,'STA2601H0140','2026-01-21 15:48:55.981966',4,149,NULL),(170,1,'STA2601M0141','2026-01-21 15:50:49.581018',4,150,NULL),(171,6,'CHA2601Y0142','2026-01-21 16:02:03.037149',4,151,NULL),(172,1,'POW2601G0143','2026-01-21 16:03:47.643868',4,152,NULL),(173,1,'CHA2601H0144','2026-01-21 16:05:17.558500',4,153,NULL),(174,5,'CHA2601H0145','2026-01-21 16:06:52.409547',4,154,NULL),(175,2,'CHA2601J0146','2026-01-21 16:13:38.865526',4,155,NULL),(176,3,'CHA2601D0147','2026-01-22 09:00:25.806741',4,156,NULL),(177,1,'EAR2601U0148','2026-01-22 08:36:05.507198',4,157,NULL),(178,4,'STA2601N0149','2026-01-22 08:37:51.050344',4,158,NULL),(179,1,'CAB2601Y0150','2026-01-22 08:40:31.899665',4,159,NULL),(180,1,'CHA2601K0150','2026-01-22 08:48:35.745821',4,82,NULL),(181,1,'CHA2601C0151','2026-01-22 08:53:19.500361',4,160,NULL),(182,1,'POW2601Z0152','2026-01-22 08:59:08.167502',4,161,NULL),(183,1,'CAB2601G0153','2026-01-22 09:37:30.813504',4,162,NULL),(184,1,'EAR2601U0153','2026-01-22 09:39:23.237752',4,63,NULL),(185,7,'CAB2601G0153','2026-01-22 09:48:07.376910',4,15,NULL),(186,3,'CAB2601X0153','2026-01-22 09:49:48.044043',4,14,NULL),(187,3,'CHA2601V0153','2026-01-22 09:55:13.596852',4,12,NULL),(188,7,'CHA2601K0153','2026-01-22 09:57:57.157197',4,9,NULL),(189,1,'CHA2601U0153','2026-01-22 10:01:59.635862',4,8,NULL),(190,2,'BUD2601X0153','2026-01-22 10:04:39.667089',4,95,NULL),(191,1,'EAR2601U0153','2026-01-22 10:06:04.416890',4,99,NULL),(192,2,'BUD2601V0153','2026-01-22 10:07:21.820439',4,97,NULL),(193,2,'BUD2601P0153','2026-01-22 10:08:44.835218',4,96,NULL),(194,1,'POW2601V0153','2026-01-22 10:10:46.698988',4,54,NULL),(195,1,'POW2601M0154','2026-01-22 12:17:53.180505',4,163,NULL),(196,7,'CHA2601D0155','2026-01-22 12:21:40.631272',4,164,NULL),(197,1,'CHA2601T0155','2026-01-22 12:23:53.697257',4,16,NULL),(198,1,'STA2601S0156','2026-01-22 12:26:19.468997',4,165,NULL);
/*!40000 ALTER TABLE `product_quantity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_rack`
--

DROP TABLE IF EXISTS `product_rack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_rack` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `branch_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_rack_name_branch_id_9a1cf4cf_uniq` (`name`,`branch_id`),
  KEY `product_rack_branch_id_dcb66979_fk_company_branch_id` (`branch_id`),
  CONSTRAINT `product_rack_branch_id_dcb66979_fk_company_branch_id` FOREIGN KEY (`branch_id`) REFERENCES `company_branch` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_rack`
--

LOCK TABLES `product_rack` WRITE;
/*!40000 ALTER TABLE `product_rack` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_rack` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_serialnumber`
--

DROP TABLE IF EXISTS `product_serialnumber`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_serialnumber` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `serial_number` varchar(100) NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  `purchase_date` datetime(6) NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_serialnumber_product_id_a4c07125_fk_product_product_id` (`product_id`),
  CONSTRAINT `product_serialnumber_product_id_a4c07125_fk_product_product_id` FOREIGN KEY (`product_id`) REFERENCES `product_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=773 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_serialnumber`
--

LOCK TABLES `product_serialnumber` WRITE;
/*!40000 ALTER TABLE `product_serialnumber` DISABLE KEYS */;
INSERT INTO `product_serialnumber` VALUES (218,'C4H5235Y6M3PM0WAJ',1,'2026-01-08 12:50:11.624507',13),(219,'C4H5235JWVGPM0WAZ',1,'2026-01-08 12:50:11.626514',13),(220,'C4H52352JHYPM0WAB',1,'2026-01-08 12:50:11.626933',13),(221,'C4H4355R74KPM0WA1',1,'2026-01-08 12:50:11.627246',13),(222,'C4H5235GEQHPM0WA1',1,'2026-01-08 12:50:11.627548',13),(248,'6933138624852',1,'2026-01-08 13:34:59.043197',24),(249,'6933138624852',1,'2026-01-08 13:34:59.043598',24),(250,'6933138624852',1,'2026-01-08 13:34:59.043843',24),(251,'6933138624852',1,'2026-01-08 13:34:59.044069',24),(252,'6933138624852',1,'2026-01-08 13:34:59.044286',24),(253,'6933138624852',1,'2026-01-08 13:34:59.045165',24),(254,'8645404009802',1,'2026-01-08 13:39:47.706742',25),(255,'8645404009802',1,'2026-01-08 13:39:47.707005',25),(256,'8645404009802',1,'2026-01-08 13:39:47.707184',25),(257,'8645404009802',1,'2026-01-08 13:39:47.707349',25),(258,'8645404009802',1,'2026-01-08 13:39:47.707497',25),(269,'6954120783029',1,'2026-01-08 13:48:08.741899',28),(270,'6954120783029',1,'2026-01-08 13:48:08.742331',28),(274,'6971437913680',1,'2026-01-08 13:53:04.045068',31),(275,'6971437913734',1,'2026-01-08 13:53:04.045288',31),(276,'6971437913000',1,'2026-01-08 13:55:12.046116',32),(278,'6971437913147',1,'2026-01-08 14:08:12.480276',35),(279,'6971437912966',1,'2026-01-08 14:08:12.480704',35),(280,'76933925133450',1,'2026-01-08 14:12:54.693898',37),(281,'76933925133450',1,'2026-01-08 14:12:54.694372',37),(282,'76933925133450',1,'2026-01-08 14:12:54.694692',37),(283,'76933925133450',1,'2026-01-08 14:12:54.694971',37),(284,'76933925133450',1,'2026-01-08 14:12:54.695308',37),(285,'6978541697321',1,'2026-01-08 14:14:24.350862',38),(286,'6978541697321',1,'2026-01-08 14:14:24.351323',38),(287,'6978541697321',1,'2026-01-08 14:14:24.351662',38),(288,'6933138327968',1,'2026-01-08 14:15:38.122946',39),(289,'8645404009710',1,'2026-01-08 14:19:48.386337',41),(290,'8645404009710',1,'2026-01-08 14:19:48.386718',41),(300,'6933138691342',1,'2026-01-08 14:40:59.416879',47),(301,'6922936306855',1,'2026-01-08 14:44:52.491940',48),(302,'653461696338',1,'2026-01-08 14:50:38.919753',51),(307,'8904274423713',1,'2026-01-08 14:51:39.070723',17),(308,'8904274424864',1,'2026-01-08 14:51:39.071092',17),(309,'8904274424864',1,'2026-01-08 14:51:39.071374',17),(310,'8904274424864',1,'2026-01-08 14:51:39.071611',17),(311,'8904274424864',1,'2026-01-08 14:51:39.071823',17),(313,'6933138700082',1,'2026-01-08 14:59:01.861281',53),(316,'6955482531297',1,'2026-01-08 15:10:16.749674',57),(317,'6933185730421',1,'2026-01-08 15:15:02.220782',59),(318,'6971437913024',1,'2026-01-08 15:18:30.926510',61),(319,'6901530236461',1,'2026-01-08 15:20:44.673211',62),(321,'6932172617608',1,'2026-01-08 15:28:04.402805',64),(328,'6933138692028',1,'2026-01-17 11:09:44.661800',73),(340,'6904846525250',1,'2026-01-17 11:29:48.953490',77),(342,'8645404009727',1,'2026-01-17 11:37:51.238338',52),(343,'8645404009727',1,'2026-01-17 11:37:51.238657',52),(344,'8645404009727',1,'2026-01-17 11:37:51.238894',52),(346,'6971437913772',1,'2026-01-17 12:26:08.178797',80),(347,'6971536923146',1,'2026-01-17 12:27:48.663982',81),(348,'6971536923146',1,'2026-01-17 12:27:48.664280',81),(351,'6933138693643',1,'2026-01-17 12:30:48.563014',18),(352,'6933138693643',1,'2026-01-17 12:30:48.563358',18),(353,'6933138693643',1,'2026-01-17 12:30:48.564033',18),(356,'SWNFCHB0402432',1,'2026-01-17 13:16:35.232091',89),(357,'SWNFCHB0403894',1,'2026-01-17 13:16:35.232457',89),(358,'6254861384340',1,'2026-01-17 13:30:07.545452',94),(370,'OZBU5410090',1,'2026-01-17 13:47:57.457856',98),(373,'6484864752529',1,'2026-01-17 13:56:56.924812',100),(375,'D4816133F5N001994',1,'2026-01-17 14:03:30.946238',102),(376,'D4816133F5N013334',1,'2026-01-17 14:03:30.946976',102),(377,'D4816133F5N001097',1,'2026-01-17 14:03:30.947363',102),(378,'D4816133F5N001091',1,'2026-01-17 14:03:30.947672',102),(379,'D4816133F5N013524',1,'2026-01-17 14:03:30.947994',102),(380,'250516151001012551',1,'2026-01-17 14:06:21.369498',103),(381,'250516151001012509',1,'2026-01-17 14:06:21.369852',103),(382,'250516151001012007',1,'2026-01-17 14:06:21.370087',103),(383,'250516151001012542',1,'2026-01-17 14:06:21.370315',103),(384,'250516151001012590',1,'2026-01-17 14:06:21.370498',103),(385,'D631460000012F6D024107',1,'2026-01-17 14:10:55.943651',104),(386,'D631460000012F6D024081',1,'2026-01-17 14:10:55.944152',104),(387,'D631460000012F6007221',1,'2026-01-17 14:10:55.944557',104),(388,'D631460000012F6D006864',1,'2026-01-17 14:10:55.944761',104),(389,'D631460000012F6D007234',1,'2026-01-17 14:10:55.944922',104),(390,'47415/00847507',1,'2026-01-17 14:29:34.412860',105),(391,'47415/00847531',1,'2026-01-17 14:29:34.413375',105),(392,'47415/00847530',1,'2026-01-17 14:29:34.413651',105),(393,'47415/00847537',1,'2026-01-17 14:29:34.413879',105),(394,'47415/00847522',1,'2026-01-17 14:29:34.414806',105),(395,'47415/00847532',1,'2026-01-17 14:29:34.415132',105),(396,'FGJ5024QUI91NR1LH',1,'2026-01-17 14:39:50.452634',106),(397,'FGJ5024EIKA1NR1LH',1,'2026-01-17 14:39:50.453065',106),(398,'FGJ5024KKL61NR1LH',1,'2026-01-17 14:39:50.453313',106),(399,'FGJ5024616S1NR1LH',1,'2026-01-17 14:39:50.453529',106),(400,'FGJ5024APK41NR1LH',1,'2026-01-17 14:39:50.453772',106),(418,'8907444526658',1,'2026-01-17 14:56:38.674119',108),(419,'6903245712582',1,'2026-01-19 14:35:31.808421',111),(420,'6903245712582',1,'2026-01-19 14:35:31.808804',111),(421,'6903245712582',1,'2026-01-19 14:35:31.809004',111),(422,'6903245712582',1,'2026-01-19 14:35:31.809179',111),(423,'6903245712582',1,'2026-01-19 14:35:31.809342',111),(424,'6903245712582',1,'2026-01-19 14:35:31.809525',111),(425,'6903245712582',1,'2026-01-19 14:35:31.809690',111),(426,'6903245712582',1,'2026-01-19 14:35:31.809838',111),(427,'6903245712582',1,'2026-01-19 14:35:31.809975',111),(428,'6903457812582',1,'2026-01-19 14:39:22.129930',112),(429,'6903457812582',1,'2026-01-19 14:39:22.130276',112),(430,'6903457812582',1,'2026-01-19 14:39:22.130473',112),(431,'6903457812582',1,'2026-01-19 14:39:22.130650',112),(432,'6903457812582',1,'2026-01-19 14:39:22.130820',112),(433,'653461769353',1,'2026-01-19 14:49:31.149974',114),(434,'653461769353',1,'2026-01-19 14:49:31.150611',114),(435,'653461769353',1,'2026-01-19 14:49:31.150961',114),(436,'653461769353',1,'2026-01-19 14:49:31.151289',114),(437,'653461769353',1,'2026-01-19 14:49:31.151601',114),(438,'653461769353',1,'2026-01-19 14:49:31.151899',114),(439,'653461769353',1,'2026-01-19 14:49:31.152208',114),(443,'6901548846966',1,'2026-01-21 11:25:21.871535',76),(444,'6901548846966',1,'2026-01-21 11:25:21.871990',76),(445,'6901548846966',1,'2026-01-21 11:25:21.872278',76),(446,'6975131820459',1,'2026-01-21 12:56:35.311995',120),(447,'6975131820459',1,'2026-01-21 12:56:35.313145',120),(453,'653461699360',1,'2026-01-21 13:00:16.599411',27),(454,'653461699360',1,'2026-01-21 13:00:16.599717',27),(455,'653461699360',1,'2026-01-21 13:00:16.599906',27),(456,'653461699360',1,'2026-01-21 13:00:16.600117',27),(457,'653461699360',1,'2026-01-21 13:00:16.600329',27),(458,'653461699360',1,'2026-01-21 13:00:16.601002',27),(459,'653461699360',1,'2026-01-21 13:00:16.601337',27),(460,'653461699360',1,'2026-01-21 13:00:16.601538',27),(461,'653461699360',1,'2026-01-21 13:00:16.601741',27),(462,'653461699360',1,'2026-01-21 13:00:16.601911',27),(463,'653461699360',1,'2026-01-21 13:00:55.049426',121),(464,'653461699360',1,'2026-01-21 13:00:55.050119',121),(465,'653461699360',1,'2026-01-21 13:00:55.050687',121),(466,'653461699360',1,'2026-01-21 13:00:55.051852',121),(467,'653461699360',1,'2026-01-21 13:00:55.052673',121),(468,'653461782901',1,'2026-01-21 13:06:44.513872',122),(469,'653461782901',1,'2026-01-21 13:06:44.514357',122),(470,'653461782901',1,'2026-01-21 13:06:44.514652',122),(471,'653461764327',1,'2026-01-21 13:09:30.142956',43),(472,'653461764327',1,'2026-01-21 13:09:30.143256',43),(473,'653461764327',1,'2026-01-21 13:09:30.143544',43),(474,'643781655825',1,'2026-01-21 13:12:05.186982',123),(475,'659629754391',1,'2026-01-21 13:14:22.346752',124),(476,'659629754391',1,'2026-01-21 13:14:22.347050',124),(477,'659629754391',1,'2026-01-21 13:14:22.347260',124),(478,'659629754391',1,'2026-01-21 13:14:22.347494',124),(479,'659629754391',1,'2026-01-21 13:14:22.347782',124),(480,'6965489710700',1,'2026-01-21 13:18:05.602108',101),(481,'6978541258638',1,'2026-01-21 14:15:11.150634',125),(482,'6978541258638',1,'2026-01-21 14:15:11.151354',125),(483,'6978541258638',1,'2026-01-21 14:15:11.156619',125),(484,'653461977512',1,'2026-01-21 14:17:02.683381',126),(485,'653461977512',1,'2026-01-21 14:17:02.683767',126),(486,'653461977512',1,'2026-01-21 14:17:02.684153',126),(487,'653461977512',1,'2026-01-21 14:17:02.684439',126),(488,'1212',1,'2026-01-21 14:26:06.874392',131),(489,'643781962268',1,'2026-01-21 14:27:39.730208',132),(490,'643781962268',1,'2026-01-21 14:27:39.730571',132),(491,'643781737682',1,'2026-01-21 14:29:09.864599',133),(492,'643781737682',1,'2026-01-21 14:29:09.864933',133),(493,'8645404009734',1,'2026-01-21 14:30:48.641699',134),(494,'8645404009734',1,'2026-01-21 14:30:48.642041',134),(495,'643781650660',1,'2026-01-21 14:40:11.882454',138),(496,'6904846525250',1,'2026-01-21 14:41:22.584321',139),(497,'6904846525250',1,'2026-01-21 14:41:22.584646',139),(498,'6904846525250',1,'2026-01-21 14:41:22.584868',139),(499,'6904846525250',1,'2026-01-21 14:41:22.585077',139),(500,'6904846525250',1,'2026-01-21 14:41:22.585256',139),(506,'6904845625258',1,'2026-01-21 14:50:42.323957',141),(507,'6904845625258',1,'2026-01-21 14:50:42.324440',141),(508,'6904845625258',1,'2026-01-21 14:50:42.324720',141),(509,'6904845625258',1,'2026-01-21 14:50:42.324944',141),(510,'6904845625258',1,'2026-01-21 14:50:42.325188',141),(511,'8645404008201',1,'2026-01-21 14:52:45.510010',142),(512,'76933925117498',1,'2026-01-21 14:54:40.681217',79),(513,'76933925117498',1,'2026-01-21 14:54:40.681658',79),(514,'76933925117498',1,'2026-01-21 14:54:40.681953',79),(515,'76933925117498',1,'2026-01-21 14:54:40.682272',79),(516,'76933925117498',1,'2026-01-21 14:54:40.682542',79),(517,'76933925117498',1,'2026-01-21 14:54:40.682784',79),(523,'76933925117498',1,'2026-01-21 14:55:37.104666',140),(524,'76933925117498',1,'2026-01-21 14:55:37.105044',140),(525,'76933925117498',1,'2026-01-21 14:55:37.105317',140),(526,'76933925117498',1,'2026-01-21 14:55:37.105586',140),(527,'76933925117498',1,'2026-01-21 14:55:37.105837',140),(528,'6365469835636',1,'2026-01-21 15:00:14.284115',143),(529,'6901548845754',1,'2026-01-21 15:01:24.783875',42),(530,'6901548845754',1,'2026-01-21 15:01:24.784164',42),(531,'6901548845754',1,'2026-01-21 15:01:24.784414',42),(532,'6901548845754',1,'2026-01-21 15:01:24.784641',42),(533,'6901548845754',1,'2026-01-21 15:01:24.785613',42),(534,'6901548845754',1,'2026-01-21 15:01:24.787068',42),(535,'6901548845754',1,'2026-01-21 15:01:24.787321',42),(536,'6901548845754',1,'2026-01-21 15:01:24.787562',42),(537,'6901548845754',1,'2026-01-21 15:01:24.787854',42),(538,'6901548845754',1,'2026-01-21 15:01:24.788028',42),(539,'6901548845754',1,'2026-01-21 15:01:24.788247',42),(540,'6933138692653',1,'2026-01-21 15:04:24.693776',144),(541,'6901549376851',1,'2026-01-21 15:07:13.902843',145),(542,'6901549376851',1,'2026-01-21 15:07:13.903129',145),(543,'6901549376851',1,'2026-01-21 15:07:13.903420',145),(544,'6901549376851',1,'2026-01-21 15:07:13.903700',145),(545,'6901549376851',1,'2026-01-21 15:07:13.903944',145),(546,'6933138695425',1,'2026-01-21 15:08:44.811675',146),(547,'6921470328545',1,'2026-01-21 15:10:47.372910',147),(548,'6921470328545',1,'2026-01-21 15:10:47.373249',147),(549,'6970463503018',1,'2026-01-21 15:12:19.153682',75),(550,'6970463503018',1,'2026-01-21 15:12:19.154323',75),(551,'6970463503018',1,'2026-01-21 15:12:19.154581',75),(552,'6970463503018',1,'2026-01-21 15:12:19.154798',75),(553,'6970463503018',1,'2026-01-21 15:12:19.155014',75),(554,'6970463503018',1,'2026-01-21 15:12:19.155230',75),(555,'6970463503018',1,'2026-01-21 15:14:15.033469',22),(556,'6970463503018',1,'2026-01-21 15:14:15.034179',22),(557,'6970463503018',1,'2026-01-21 15:14:15.034589',22),(558,'6970463503018',1,'2026-01-21 15:14:15.034805',22),(559,'6970463503018',1,'2026-01-21 15:14:15.034994',22),(560,'6970463503018',1,'2026-01-21 15:14:15.035155',22),(561,'6970463503018',1,'2026-01-21 15:17:21.878037',23),(562,'6970463503018',1,'2026-01-21 15:17:21.878558',23),(563,'6970463503018',1,'2026-01-21 15:17:21.878815',23),(564,'6970463503018',1,'2026-01-21 15:17:21.879114',23),(565,'6970463503018',1,'2026-01-21 15:17:21.879391',23),(566,'6970463503018',1,'2026-01-21 15:17:21.879642',23),(567,'6970463503018',1,'2026-01-21 15:17:21.879874',23),(568,'6970463503018',1,'2026-01-21 15:17:21.880240',23),(569,'6970463503018',1,'2026-01-21 15:17:21.880826',23),(570,'6970463503018',1,'2026-01-21 15:17:21.881138',23),(571,'6970463503018',1,'2026-01-21 15:17:21.881359',23),(576,'6901475239701',1,'2026-01-21 15:22:06.024085',74),(585,'6901475239701',1,'2026-01-21 15:27:59.192729',19),(586,'6901475239701',1,'2026-01-21 15:27:59.193162',19),(587,'6901475239701',1,'2026-01-21 15:27:59.193461',19),(588,'6901475239701',1,'2026-01-21 15:27:59.193694',19),(589,'6901475239701',1,'2026-01-21 15:27:59.193896',19),(590,'6901475239701',1,'2026-01-21 15:27:59.194097',19),(591,'6901475239701',1,'2026-01-21 15:27:59.194326',19),(592,'6901475239701',1,'2026-01-21 15:27:59.194536',19),(593,'6901530232449',1,'2026-01-21 15:29:16.508114',78),(594,'6901530232449',1,'2026-01-21 15:29:16.508531',78),(595,'6901530232449',1,'2026-01-21 15:29:16.508792',78),(596,'6901530232449',1,'2026-01-21 15:29:16.509013',78),(607,'6901530232357',1,'2026-01-21 15:33:10.253171',20),(608,'6901530232357',1,'2026-01-21 15:33:10.253528',20),(609,'6901530232357',1,'2026-01-21 15:33:10.253764',20),(610,'6901530232357',1,'2026-01-21 15:33:10.253985',20),(611,'6901530232357',1,'2026-01-21 15:33:10.254241',20),(612,'6901549376219',1,'2026-01-21 15:37:10.062776',56),(613,'6901549376219',1,'2026-01-21 15:37:10.063038',56),(614,'6901549376219',1,'2026-01-21 15:37:10.063255',56),(615,'653461867035',1,'2026-01-21 15:39:33.832644',29),(616,'653461867035',1,'2026-01-21 15:39:33.833032',29),(617,'653461867035',1,'2026-01-21 15:39:33.833376',29),(626,'1596146423203',1,'2026-01-21 16:02:03.037742',151),(627,'1596146423203',1,'2026-01-21 16:02:03.038088',151),(628,'1596146423203',1,'2026-01-21 16:02:03.038293',151),(629,'1596146423203',1,'2026-01-21 16:02:03.038469',151),(630,'1596146423203',1,'2026-01-21 16:02:03.038638',151),(631,'1596146423203',1,'2026-01-21 16:02:03.038837',151),(632,'6978541258638',1,'2026-01-21 16:03:47.644443',152),(633,'6941383798785',1,'2026-01-21 16:05:17.558971',153),(634,'8645040200007',1,'2026-01-21 16:06:52.410066',154),(635,'8645040200007',1,'2026-01-21 16:06:52.410425',154),(636,'8645040200007',1,'2026-01-21 16:06:52.410679',154),(637,'8645040200007',1,'2026-01-21 16:06:52.410930',154),(638,'8645040200007',1,'2026-01-21 16:06:52.411144',154),(639,'248658452523',1,'2026-01-22 08:36:05.507759',157),(640,'6901548849608',1,'2026-01-22 08:40:31.900251',159),(641,'6903642105789',1,'2026-01-22 08:48:35.747089',82),(642,'6903642105789',1,'2026-01-22 08:48:35.747629',82),(643,'6903642105789',1,'2026-01-22 08:48:35.747938',82),(644,'6933138602126',1,'2026-01-22 08:53:19.501134',160),(645,'0001',1,'2026-01-22 08:59:08.168883',161),(646,'653461536566',1,'2026-01-22 09:01:49.997577',26),(647,'653461536566',1,'2026-01-22 09:01:49.998034',26),(648,'653461536566',1,'2026-01-22 09:01:49.998273',26),(649,'653461536566',1,'2026-01-22 09:01:49.998453',26),(650,'653461536566',1,'2026-01-22 09:01:49.998664',26),(651,'653461536566',1,'2026-01-22 09:01:50.000189',26),(652,'653461536566',1,'2026-01-22 09:01:50.001342',26),(653,'653461536566',1,'2026-01-22 09:01:50.002075',26),(654,'653461536566',1,'2026-01-22 09:01:50.002471',26),(655,'R621711000001F4V03KF2B',1,'2026-01-22 09:39:23.238866',63),(656,'R621711000002F4M01CE2G',1,'2026-01-22 09:39:23.239233',63),(657,'RF7TUP67RYDRTB',1,'2026-01-22 09:48:07.378588',15),(658,'RF7TUK53HSZRTB',1,'2026-01-22 09:48:07.379315',15),(659,'RF7TUP42M42RTB',1,'2026-01-22 09:48:07.379683',15),(660,'RF7TYO16U16RTB',1,'2026-01-22 09:48:07.380012',15),(661,'RF7TYN53MIMRTB',1,'2026-01-22 09:48:07.380455',15),(662,'RF7TYN53Z53RTB',1,'2026-01-22 09:48:07.380791',15),(663,'RF7TUL29X29RTB',1,'2026-01-22 09:48:07.381117',15),(664,'RF7TUK64PBORTB',1,'2026-01-22 09:48:07.381497',15),(665,'RF7TYN61CTJRTB',1,'2026-01-22 09:48:07.381864',15),(666,'RF7TUK69MQZRTB',1,'2026-01-22 09:48:07.382303',15),(667,'RF7TUL59X59RTB',1,'2026-01-22 09:48:07.382606',15),(668,'RF7TUK63GQLRTB',1,'2026-01-22 09:48:07.383207',15),(669,'RF7TYN53O53RTB',1,'2026-01-22 09:48:07.383565',15),(670,'RF7TYN93Z93RTB',1,'2026-01-22 09:48:07.383909',15),(671,'RF7TUK61TFSRTB',1,'2026-01-22 09:48:07.384191',15),(672,'RF7TUP72WIVRTB',1,'2026-01-22 09:48:07.384558',15),(673,'RF7TYN68AULRTB',1,'2026-01-22 09:48:07.384869',15),(674,'RF6W2HTACYLRTB',1,'2026-01-22 09:49:48.046025',14),(675,'RF7Y9O55BHFRTB',1,'2026-01-22 09:49:48.046597',14),(676,'R3V2LZ74HSPRT3',1,'2026-01-22 09:49:48.047312',14),(677,'RF6W2HTAJ1DRTB',1,'2026-01-22 09:49:48.047781',14),(678,'R3V2LZ87TAQRT3',1,'2026-01-22 09:49:48.048103',14),(679,'RF7Y9C17WNDRTB',1,'2026-01-22 09:49:48.048441',14),(680,'R3V2LZ82M82RT3',1,'2026-01-22 09:49:48.048776',14),(681,'RF6W2HTABN6RTB',1,'2026-01-22 09:49:48.048996',14),(682,'R3V2LZ18IMXRT3',1,'2026-01-22 09:49:48.049697',14),(683,'R3V2LZ59X59RT3',1,'2026-01-22 09:49:48.050052',14),(684,'RF7Y9O64Q64RTB',1,'2026-01-22 09:49:48.050292',14),(685,'R3V2LZ30VQKRT3',1,'2026-01-22 09:49:48.050584',14),(686,'R3V2LY96QIWRT3',1,'2026-01-22 09:49:48.050899',14),(687,'R3V2LZ60Z60RT3',1,'2026-01-22 09:49:48.051123',14),(688,'R3V2LZ10E10RT3',1,'2026-01-22 09:49:48.051461',14),(689,'RF7Y925IQN1DKB',1,'2026-01-22 09:55:13.598111',12),(690,'RF7Y9XF0AK1DKB',1,'2026-01-22 09:55:13.598406',12),(691,'RF7Y9JO3TW1DKB',1,'2026-01-22 09:55:13.598676',12),(692,'RF7Y93RB1U1DKB',1,'2026-01-22 09:55:13.598904',12),(693,'RF7Y97XNYA1DKB',1,'2026-01-22 09:55:13.599873',12),(694,'RF7Y9O7KYK1DKB',1,'2026-01-22 09:55:13.600234',12),(695,'RF7Y9FYOPM1DKB',1,'2026-01-22 09:55:13.600567',12),(696,'RF7Y93U68T1DKB',1,'2026-01-22 09:55:13.600854',12),(697,'RF7Y94HO7L1DKB',1,'2026-01-22 09:55:13.601230',12),(698,'RF7Y99QNBC1DKB',1,'2026-01-22 09:55:13.601469',12),(699,'RF7Y9O5HXR1DKB',1,'2026-01-22 09:55:13.601823',12),(700,'RF7Y9UDV7A1DKB',1,'2026-01-22 09:55:13.602022',12),(701,'RF7Y9ZFJ0K1DKB',1,'2026-01-22 09:55:13.602345',12),(702,'RF7Y9MK',1,'2026-01-22 09:55:13.602526',12),(703,'RZ7Y9WI8OM1RCB',1,'2026-01-22 09:57:57.158452',9),(704,'RZ7Y9PRJ3I1RCB',1,'2026-01-22 09:57:57.158793',9),(705,'RZ7Y9MEPF91RCB',1,'2026-01-22 09:57:57.159028',9),(706,'RZ7Y91CI2Y1RCB',1,'2026-01-22 09:57:57.159255',9),(707,'RZ7Y9M9VHT1RCB',1,'2026-01-22 09:57:57.159501',9),(708,'RZ7Y9E59GM1RCB',1,'2026-01-22 09:57:57.159714',9),(709,'RZ7Y9LL4VV1RCB',1,'2026-01-22 09:57:57.159911',9),(710,'RZ7Y98Q0GR1RCB',1,'2026-01-22 09:57:57.160100',9),(711,'RZ7Y1JCYMK1DKB',1,'2026-01-22 09:57:57.160289',9),(712,'RZ7Y9CX5L01RCB',1,'2026-01-22 09:57:57.160504',9),(728,'SHHY54230956263MA8',1,'2026-01-22 10:01:59.637119',8),(729,'HHY515603M9263MAN',1,'2026-01-22 10:01:59.637469',8),(730,'SHHY54230959263MA5',1,'2026-01-22 10:01:59.637708',8),(731,'HHY51560HGB263MAM',1,'2026-01-22 10:01:59.637967',8),(732,'SHHY542306TZ263MAL',1,'2026-01-22 10:01:59.638267',8),(733,'SHHY54230E02263MAN',1,'2026-01-22 10:01:59.638882',8),(734,'SHHY54230NAC263MA8',1,'2026-01-22 10:01:59.639243',8),(735,'HHY51561HPJ263MAQ',1,'2026-01-22 10:01:59.639510',8),(736,'HHY54231N5A263MAN',1,'2026-01-22 10:01:59.639794',8),(737,'SHHY54230XWV263MAQ',1,'2026-01-22 10:01:59.640090',8),(738,'SHHY54230WJC263MAA',1,'2026-01-22 10:01:59.640344',8),(739,'SHHY542302WB263MA3',1,'2026-01-22 10:01:59.640568',8),(740,'SHHY54231MXF263MA8',1,'2026-01-22 10:01:59.640813',8),(741,'HHY51561YEV263MAR',1,'2026-01-22 10:01:59.641101',8),(742,'8904130885518',1,'2026-01-22 10:04:39.667995',95),(743,'8904130885549',1,'2026-01-22 10:04:39.669151',95),(744,'8904130885518',1,'2026-01-22 10:04:39.669434',95),(745,'8904130885549',1,'2026-01-22 10:04:39.669650',95),(746,'8904130885549',1,'2026-01-22 10:04:39.669853',95),(747,'BAMJ8281706',1,'2026-01-22 10:06:04.417946',99),(748,'TFOG5840843',1,'2026-01-22 10:06:04.418279',99),(749,'LLF01034867',1,'2026-01-22 10:06:04.418518',99),(750,'V1714000024FBFF034R2L',1,'2026-01-22 10:07:21.821488',97),(751,'V1714000027FAW00B32L',1,'2026-01-22 10:07:21.821778',97),(752,'V1714000025FAF03Z12B',1,'2026-01-22 10:07:21.821993',97),(753,'V1714000027FBH00N82L',1,'2026-01-22 10:07:21.822213',97),(754,'250811422306904126',1,'2026-01-22 10:08:44.837286',96),(755,'250912422306914180',1,'2026-01-22 10:08:44.837656',96),(756,'250808422306903051',1,'2026-01-22 10:08:44.837900',96),(757,'250807422306907459',1,'2026-01-22 10:08:44.838181',96),(758,'250811422306904083',1,'2026-01-22 10:08:44.838380',96),(759,'6954851250029',1,'2026-01-22 10:10:46.700262',54),(760,'6954851250029',1,'2026-01-22 10:10:46.700609',54),(761,'6954851250036',1,'2026-01-22 10:10:46.700859',54),(762,'6954851250050',1,'2026-01-22 12:17:53.181443',163),(763,'RF7XCR9J2R1DKB',1,'2026-01-22 12:21:40.631947',164),(764,'RF7X7K5X1TCDKB',1,'2026-01-22 12:21:40.632320',164),(765,'R37X1218LS0DKA',1,'2026-01-22 12:21:40.632618',164),(766,'R37X1218LIIDKB',1,'2026-01-22 12:21:40.632857',164),(767,'R37X1218LX8DKA',1,'2026-01-22 12:21:40.633082',164),(768,'R46R4T6LWYUSEA',1,'2026-01-22 12:21:40.633293',164),(769,'R37W8LBG46FSEB',1,'2026-01-22 12:21:40.633573',164),(770,'C4H512005R91VHJAL',1,'2026-01-22 12:23:53.698584',16),(771,'C4H51201KG21VHJA3',1,'2026-01-22 12:23:53.698880',16),(772,'C4H512001Q71VHJAV',1,'2026-01-22 12:23:53.699128',16);
/*!40000 ALTER TABLE `product_serialnumber` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_subbrand`
--

DROP TABLE IF EXISTS `product_subbrand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_subbrand` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `category_id` bigint DEFAULT NULL,
  `subcategory_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_subbrand_category_id_7728b49d_fk_product_category_id` (`category_id`),
  KEY `product_subbrand_subcategory_id_519a889d_fk_product_s` (`subcategory_id`),
  CONSTRAINT `product_subbrand_category_id_7728b49d_fk_product_category_id` FOREIGN KEY (`category_id`) REFERENCES `product_category` (`id`),
  CONSTRAINT `product_subbrand_subcategory_id_519a889d_fk_product_s` FOREIGN KEY (`subcategory_id`) REFERENCES `product_subcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_subbrand`
--

LOCK TABLES `product_subbrand` WRITE;
/*!40000 ALTER TABLE `product_subbrand` DISABLE KEYS */;
INSERT INTO `product_subbrand` VALUES (1,'Apple','',1,1),(2,'boat','',1,3);
/*!40000 ALTER TABLE `product_subbrand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_subcategory`
--

DROP TABLE IF EXISTS `product_subcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_subcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_subcategory_category_id_74573633_fk_product_category_id` (`category_id`),
  CONSTRAINT `product_subcategory_category_id_74573633_fk_product_category_id` FOREIGN KEY (`category_id`) REFERENCES `product_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_subcategory`
--

LOCK TABLES `product_subcategory` WRITE;
/*!40000 ALTER TABLE `product_subcategory` DISABLE KEYS */;
INSERT INTO `product_subcategory` VALUES (1,'Phone',1),(2,'Charger',1),(3,'Buds',1),(4,'Tablet',1),(5,'Watch',1),(6,'Laptop',1),(7,'Phone',2),(8,'Tablet',2),(9,'Watch',2),(10,'Wired',3),(12,'Wired',4),(13,'Wireless',3),(14,'Phone',6),(15,'Watch',6),(16,'Car',6),(17,'Wirelss',6),(18,'All in one',6),(19,'Wired',7),(20,'Wireless',7),(21,'Wired',8),(22,'Wireless',8),(23,'Glossy',9),(24,'Matt',9),(25,'Privacy',9),(26,'Auto Repair',9),(27,'Print',9),(28,'Leather',9),(29,'Leather Print',9),(30,'Laptop',9),(31,'Transperent',9),(32,'Table',10),(33,'Car',10),(34,'Bike',10),(35,'Activa',10),(36,'Tripod',10),(37,'Type C',11),(38,'V8',11),(39,'C TO LIGHTNING',11),(40,'All in one',11),(41,'C To C',11),(42,'USB To C',11),(43,'Silicon',17),(44,'Loop',17),(45,'Welcrow',17),(46,'Leather',17),(47,'Chain',17),(48,'Magnetic Silicon',17),(49,'Magnetic Chain',17),(50,'Ceramic',17),(51,'Normal',16),(52,'Diamond',16),(53,'Football',16),(54,'Wired',14),(55,'Wireless',14),(56,'Wired',15),(57,'Wireless',15),(58,'Leather Wallet',19),(59,'Pop Socket',19),(60,'Rings',19),(61,'Wireless',4),(62,'Magsafe Wallet',19),(63,'USB To Lightning',11),(64,'MAGSAFE STAND',19),(65,'ALL IN ONE',12),(66,'LIGHTNING TO AUX',11),(67,'AUX',11),(68,'MAGSAFE FILL LIGHT',19),(70,'WATCH CABLE',11),(71,'4 IN 1',11);
/*!40000 ALTER TABLE `product_subcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_type`
--

DROP TABLE IF EXISTS `product_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_type_category_id_203829a5_fk_product_category_id` (`category_id`),
  CONSTRAINT `product_type_category_id_203829a5_fk_product_category_id` FOREIGN KEY (`category_id`) REFERENCES `product_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_type`
--

LOCK TABLES `product_type` WRITE;
/*!40000 ALTER TABLE `product_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_task`
--

DROP TABLE IF EXISTS `task_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_task` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `task_name` varchar(200) NOT NULL,
  `description` longtext,
  `task_frequency` json DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `assigned_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `task_task_assigned_by_id_9618ab3c_fk_accounts_user_id` (`assigned_by_id`),
  CONSTRAINT `task_task_assigned_by_id_9618ab3c_fk_accounts_user_id` FOREIGN KEY (`assigned_by_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_task`
--

LOCK TABLES `task_task` WRITE;
/*!40000 ALTER TABLE `task_task` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_task_assigned_to`
--

DROP TABLE IF EXISTS `task_task_assigned_to`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_task_assigned_to` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `task_id` bigint NOT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_task_assigned_to_task_id_employee_id_f71bda93_uniq` (`task_id`,`employee_id`),
  KEY `task_task_assigned_t_employee_id_145c7745_fk_employee_` (`employee_id`),
  CONSTRAINT `task_task_assigned_t_employee_id_145c7745_fk_employee_` FOREIGN KEY (`employee_id`) REFERENCES `employee_employee` (`id`),
  CONSTRAINT `task_task_assigned_to_task_id_ea8fe472_fk_task_task_id` FOREIGN KEY (`task_id`) REFERENCES `task_task` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_task_assigned_to`
--

LOCK TABLES `task_task_assigned_to` WRITE;
/*!40000 ALTER TABLE `task_task_assigned_to` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_task_assigned_to` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_taskimage`
--

DROP TABLE IF EXISTS `task_taskimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_taskimage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `submission_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `task_taskimage_submission_id_f1f48c31_fk_task_tasksubmission_id` (`submission_id`),
  CONSTRAINT `task_taskimage_submission_id_f1f48c31_fk_task_tasksubmission_id` FOREIGN KEY (`submission_id`) REFERENCES `task_tasksubmission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_taskimage`
--

LOCK TABLES `task_taskimage` WRITE;
/*!40000 ALTER TABLE `task_taskimage` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_taskimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_tasksubmission`
--

DROP TABLE IF EXISTS `task_tasksubmission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_tasksubmission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `submitted_at` datetime(6) NOT NULL,
  `notes` longtext,
  `status` varchar(20) NOT NULL,
  `submitted_by_id` bigint NOT NULL,
  `task_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `task_tasksubmission_submitted_by_id_71f178c9_fk_employee_` (`submitted_by_id`),
  KEY `task_tasksubmission_task_id_3bb8c5ff_fk_task_task_id` (`task_id`),
  CONSTRAINT `task_tasksubmission_submitted_by_id_71f178c9_fk_employee_` FOREIGN KEY (`submitted_by_id`) REFERENCES `employee_employee` (`id`),
  CONSTRAINT `task_tasksubmission_task_id_3bb8c5ff_fk_task_task_id` FOREIGN KEY (`task_id`) REFERENCES `task_task` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_tasksubmission`
--

LOCK TABLES `task_tasksubmission` WRITE;
/*!40000 ALTER TABLE `task_tasksubmission` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_tasksubmission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor_purchase`
--

DROP TABLE IF EXISTS `vendor_purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor_purchase` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `total` decimal(12,2) NOT NULL,
  `purchase_date` date NOT NULL,
  `notes` longtext,
  `created_at` datetime(6) NOT NULL,
  `vendor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendor_purchase_vendor_id_512e2102_fk_vendor_vendor_id` (`vendor_id`),
  CONSTRAINT `vendor_purchase_vendor_id_512e2102_fk_vendor_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendor_vendor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor_purchase`
--

LOCK TABLES `vendor_purchase` WRITE;
/*!40000 ALTER TABLE `vendor_purchase` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendor_purchase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor_purchasereceipt`
--

DROP TABLE IF EXISTS `vendor_purchasereceipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor_purchasereceipt` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `purchase_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendor_purchaserecei_purchase_id_72b3df29_fk_vendor_pu` (`purchase_id`),
  CONSTRAINT `vendor_purchaserecei_purchase_id_72b3df29_fk_vendor_pu` FOREIGN KEY (`purchase_id`) REFERENCES `vendor_purchase` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor_purchasereceipt`
--

LOCK TABLES `vendor_purchasereceipt` WRITE;
/*!40000 ALTER TABLE `vendor_purchasereceipt` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendor_purchasereceipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor_vendor`
--

DROP TABLE IF EXISTS `vendor_vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor_vendor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `contact_person` varchar(150) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `gst` varchar(20) DEFAULT NULL,
  `address` longtext,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor_vendor`
--

LOCK TABLES `vendor_vendor` WRITE;
/*!40000 ALTER TABLE `vendor_vendor` DISABLE KEYS */;
INSERT INTO `vendor_vendor` VALUES (1,'Paras','Paras','9568273613','','',NULL,'active','2026-01-06 10:27:53.278174'),(2,'Jhala','Jhala','9892662063','','',NULL,'active','2026-01-08 10:22:01.292690'),(3,'Narendra','Narendra','9004744493','','',NULL,'active','2026-01-08 10:22:23.610133'),(4,'Altaf','Altaf','9099916587','','',NULL,'active','2026-01-08 10:22:47.372682'),(5,'Stuffcool','Bhavesh','','','',NULL,'active','2026-01-08 13:12:20.722002');
/*!40000 ALTER TABLE `vendor_vendor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor_vendorreturnmonthly`
--

DROP TABLE IF EXISTS `vendor_vendorreturnmonthly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor_vendorreturnmonthly` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `year` int unsigned NOT NULL,
  `month` int unsigned NOT NULL,
  `total_qty` int unsigned NOT NULL,
  `last_updated` datetime(6) NOT NULL,
  `branch_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `vendor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vendor_vendorreturnmonth_product_id_vendor_id_bra_96c3ae86_uniq` (`product_id`,`vendor_id`,`branch_id`,`year`,`month`),
  KEY `vendor_vendorreturnm_branch_id_be738770_fk_company_b` (`branch_id`),
  KEY `vendor_vendorreturnm_vendor_id_5c06ba6f_fk_vendor_ve` (`vendor_id`),
  CONSTRAINT `vendor_vendorreturnm_branch_id_be738770_fk_company_b` FOREIGN KEY (`branch_id`) REFERENCES `company_branch` (`id`),
  CONSTRAINT `vendor_vendorreturnm_product_id_1caf4bd3_fk_product_p` FOREIGN KEY (`product_id`) REFERENCES `product_product` (`id`),
  CONSTRAINT `vendor_vendorreturnm_vendor_id_5c06ba6f_fk_vendor_ve` FOREIGN KEY (`vendor_id`) REFERENCES `vendor_vendor` (`id`),
  CONSTRAINT `vendor_vendorreturnmonthly_chk_1` CHECK ((`year` >= 0)),
  CONSTRAINT `vendor_vendorreturnmonthly_chk_2` CHECK ((`month` >= 0)),
  CONSTRAINT `vendor_vendorreturnmonthly_chk_3` CHECK ((`total_qty` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor_vendorreturnmonthly`
--

LOCK TABLES `vendor_vendorreturnmonthly` WRITE;
/*!40000 ALTER TABLE `vendor_vendorreturnmonthly` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendor_vendorreturnmonthly` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-23 13:31:13
