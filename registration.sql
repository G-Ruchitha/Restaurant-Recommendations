# HeidiSQL Dump 
#
# --------------------------------------------------------
# Host:                 127.0.0.1
# Database:             registration
# Server version:       5.5.62
# Server OS:            Win64
# Target-Compatibility: Standard ANSI SQL
# HeidiSQL version:     3.2 Revision: 1129
# --------------------------------------------------------

/*!40100 SET CHARACTER SET latin1;*/
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ANSI';*/
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;*/


#
# Database structure for database 'registration'
#

CREATE DATABASE /*!32312 IF NOT EXISTS*/ "registration" /*!40100 DEFAULT CHARACTER SET latin1 */;

USE "registration";


#
# Table structure for table 'user'
#

CREATE TABLE /*!32312 IF NOT EXISTS*/ "user" (
  "id" int(10) unsigned NOT NULL AUTO_INCREMENT,
  "first_name" varchar(50) DEFAULT NULL,
  "last_name" varchar(50) DEFAULT NULL,
  "email" varchar(50) DEFAULT NULL,
  "password" varchar(500) DEFAULT NULL,
  "created_on" varchar(50) DEFAULT NULL,
  "updated_on" varchar(50) DEFAULT NULL,
  PRIMARY KEY ("id")
) AUTO_INCREMENT=3 /*!40100 DEFAULT CHARSET=latin1*/;



#
# Dumping data for table 'user'
#

LOCK TABLES "user" WRITE;
/*!40000 ALTER TABLE "user" DISABLE KEYS;*/
REPLACE INTO "user" ("id", "first_name", "last_name", "email", "password", "created_on", "updated_on") VALUES
	('1','THIRUMALAI KUMAR','PERUMAL','thiru.fstpl@gmail.com','$2b$12$xg4feZnq2RU7CeylGgGSJ.1iJfQY72HtxsxZ6oiU8JHyNO4uTi/Lu','2021-11-30 09:19:29','2021-11-30 09:19:29');
REPLACE INTO "user" ("id", "first_name", "last_name", "email", "password", "created_on", "updated_on") VALUES
	('2','THIRUMALAI KUMAR','PERUMAL','dataalcott@gmail.com','$2b$12$bNDofNema.3VOSzu2wtFeOgspM2Jel1WLCUieuHF2Ou4Izw8uivL.','2021-11-30 09:28:13','2021-11-30 09:28:13');
/*!40000 ALTER TABLE "user" ENABLE KEYS;*/
UNLOCK TABLES;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE;*/
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;*/
