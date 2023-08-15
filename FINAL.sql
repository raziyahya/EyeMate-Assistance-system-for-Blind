/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.7.36 : Database - eyemate
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`eyemate` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `eyemate`;

/*Table structure for table `accident` */

DROP TABLE IF EXISTS `accident`;

CREATE TABLE `accident` (
  `accident_id` int(11) NOT NULL AUTO_INCREMENT,
  `accident_date` datetime DEFAULT NULL,
  `accident_latitude` varchar(200) DEFAULT NULL,
  `accident_longitude` varchar(200) DEFAULT NULL,
  `blind_id` int(5) DEFAULT NULL,
  PRIMARY KEY (`accident_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `accident` */

insert  into `accident`(`accident_id`,`accident_date`,`accident_latitude`,`accident_longitude`,`blind_id`) values (5,'2023-06-16 11:30:41','11.8683739','75.3631623',1);

/*Table structure for table `admin` */

DROP TABLE IF EXISTS `admin`;

CREATE TABLE `admin` (
  `admin_id` int(11) DEFAULT NULL,
  `admin_name` varchar(30) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `admin` */

/*Table structure for table `blind` */

DROP TABLE IF EXISTS `blind`;

CREATE TABLE `blind` (
  `blind_id` int(11) NOT NULL AUTO_INCREMENT,
  `blind_name` varchar(30) DEFAULT NULL,
  `blind_age` int(11) DEFAULT NULL,
  `blind_gender` varchar(10) DEFAULT NULL,
  `blind_mob` bigint(10) DEFAULT NULL,
  `blind_pin` int(11) DEFAULT NULL,
  `blind_place` varchar(50) DEFAULT NULL,
  `blind_email` varchar(20) DEFAULT NULL,
  `ct_id` int(5) NOT NULL,
  PRIMARY KEY (`blind_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `blind` */

insert  into `blind`(`blind_id`,`blind_name`,`blind_age`,`blind_gender`,`blind_mob`,`blind_pin`,`blind_place`,`blind_email`,`ct_id`) values (1,'juraij',45,'Male',8138873341,670555,'kanada','sur@gmail.com',2),(2,'razi',36,'Male',9539082561,670554,'Duetschland','shiba@gmail.com',2),(10,'adarsh',54,'Male',9658695869,655245,'Amerika','dsfg@ggty.tgh',2),(9,'haneen',44,'Female',4554554554,422444,'Frankreich','hf@gmail.com',2);

/*Table structure for table `caretaker` */

DROP TABLE IF EXISTS `caretaker`;

CREATE TABLE `caretaker` (
  `ct_id` int(11) NOT NULL AUTO_INCREMENT,
  `ct_name` varchar(50) DEFAULT NULL,
  `ct_gender` varchar(10) DEFAULT NULL,
  `ct_mob` bigint(11) DEFAULT NULL,
  `ct_pincode` int(11) DEFAULT NULL,
  `ct_mail` varchar(50) DEFAULT NULL,
  `ct_place` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ct_id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

/*Data for the table `caretaker` */

insert  into `caretaker`(`ct_id`,`ct_name`,`ct_gender`,`ct_mob`,`ct_pincode`,`ct_mail`,`ct_place`) values (13,'aaa','male',1234,670543,'a@gmail.com','ggg'),(5,'sinan','male',2147483647,456987,'sinan@gmail.com','knr'),(4,'juraij','male',888555444,657986,'jur@gmail.com','kasrod'),(3,'haneen','female',2147483647,681752,'hani@gmail.com','malapuram'),(1,'razi','male',956868686,670302,'razi@gmail.com','kannur'),(14,'Juraij','male',784155,4512,'jurai@gmail.com','tkr'),(2,'adarsh','male',8281233341,670521,'adarsh@gmail.com','kvr'),(15,'jura','male',457854544,54132,'dtfjyfhf@hjh.hjj','lkhn');

/*Table structure for table `emergency` */

DROP TABLE IF EXISTS `emergency`;

CREATE TABLE `emergency` (
  `emergency_id` int(11) NOT NULL AUTO_INCREMENT,
  `emergency_date` datetime DEFAULT NULL,
  `emergency_latitude` varchar(200) DEFAULT NULL,
  `emergency_longitude` varchar(200) DEFAULT NULL,
  `blind_id` int(5) NOT NULL,
  PRIMARY KEY (`emergency_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `emergency` */

insert  into `emergency`(`emergency_id`,`emergency_date`,`emergency_latitude`,`emergency_longitude`,`blind_id`) values (1,'2023-05-15 15:24:58','11.8683617','75.3631796',1),(4,'2023-06-16 11:31:22','11.8683735','75.3631625',1);

/*Table structure for table `knownperson` */

DROP TABLE IF EXISTS `knownperson`;

CREATE TABLE `knownperson` (
  `kp_id` int(11) NOT NULL AUTO_INCREMENT,
  `kp_name` varchar(50) DEFAULT NULL,
  `kp_age` int(11) DEFAULT NULL,
  `kp_gender` varchar(10) DEFAULT NULL,
  `kp_mobile` bigint(11) DEFAULT NULL,
  `kp_address` varchar(50) DEFAULT NULL,
  `blind_id` int(5) NOT NULL,
  `kp_image` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`kp_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `knownperson` */

insert  into `knownperson`(`kp_id`,`kp_name`,`kp_age`,`kp_gender`,`kp_mobile`,`kp_address`,`blind_id`,`kp_image`) values (1,'adarsh',45,'Male',8282232341,'Kannur',1,'/static/pic/20230515-145302.jpg'),(2,'juraij',22,'Male',9494606012,'Kasaragod',1,'/static/knownperson/20230515-150554.jpg');

/*Table structure for table `location` */

DROP TABLE IF EXISTS `location`;

CREATE TABLE `location` (
  `loc_id` int(11) NOT NULL AUTO_INCREMENT,
  `loc_latitude` varchar(50) DEFAULT NULL,
  `loc_longitude` varchar(50) DEFAULT NULL,
  `blind_id` int(5) DEFAULT NULL,
  PRIMARY KEY (`loc_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `location` */

insert  into `location`(`loc_id`,`loc_latitude`,`loc_longitude`,`blind_id`) values (1,'11.868430017493665','75.36122152581811',1),(2,'11.8683636','75.3631804',2);

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `usertype` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values (0,'admin','admin1','admin'),(14,'jurai@gmail.com','1234','caretaker'),(13,'a@gmail.com','123','rejected'),(5,'sinan','123','caretaker'),(4,'juraij','456','rejected'),(3,'haneen','456','caretaker'),(2,'adarsh','456','caretaker'),(1,'razi','456','rejected'),(15,'dtfjyfhf@hjh.hjj','123','caretaker');

/*Table structure for table `reviews` */

DROP TABLE IF EXISTS `reviews`;

CREATE TABLE `reviews` (
  `review_id` int(11) NOT NULL AUTO_INCREMENT,
  `ct_id` int(11) DEFAULT NULL,
  `review` varchar(100) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `review_date` date DEFAULT NULL,
  PRIMARY KEY (`review_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `reviews` */

insert  into `reviews`(`review_id`,`ct_id`,`review`,`rating`,`review_date`) values (1,1,'Good',5,'2023-01-01'),(2,2,'Awesome',5,'2023-02-22'),(3,3,'Good',4,'2023-02-27'),(4,4,'nicw',4,'2023-02-02'),(5,2,'cool',4,NULL),(6,2,'goodd',1,'2023-03-18'),(7,2,'sefgd',4,'2023-04-24');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
