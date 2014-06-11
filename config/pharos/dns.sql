-- MySQL dump 10.13  Distrib 5.1.48, for unknown-linux-gnu (x86_64)
--
-- Host: localhost    Database: dns_config
-- ------------------------------------------------------
-- Server version	5.1.48-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `dns_config`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `dns_config` /*!40100 DEFAULT CHARACTER SET gbk */;

USE `dns_config`;

--
-- Table structure for table `comple_region`
--


DROP TABLE IF EXISTS `comple_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comple_region` (
  `original_name` varchar(255) NOT NULL,
  `comple_name` varchar(255) NOT NULL,
  PRIMARY KEY  (`original_name`,`comple_name`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `current_db`
--

DROP TABLE IF EXISTS `current_db`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `current_db` (
  `dbid` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
insert into current_db values(2);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `datacenter`
--

DROP TABLE IF EXISTS `datacenter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `datacenter` (
  `datacenter` varchar(255) NOT NULL DEFAULT '',
  `vs_name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY  (`datacenter`,`vs_name`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pool`
--

DROP TABLE IF EXISTS `pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool` (
  `name` varchar(255) NOT NULL,
  `rr_ldns_limit` int(11) DEFAULT '1',
  `in_use` int(11) NOT NULL DEFAULT '1',
  `available` int(11) NOT NULL DEFAULT '1',
  `ttl` int(11) NOT NULL DEFAULT '300',
  `type` int(11) NOT NULL DEFAULT '1',
  `value` varchar(1024) DEFAULT NULL,
  PRIMARY KEY  (`name`),
  KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pool_region`
--

DROP TABLE IF EXISTS `pool_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool_region` (
  `pool_name` varchar(255) NOT NULL,
  `region_name` varchar(255) NOT NULL,
  `score` int(11) NOT NULL,
  PRIMARY KEY (pool_name, region_name),
  KEY `region_name` (`region_name`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pool_vs`
--

DROP TABLE IF EXISTS `pool_vs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool_vs` (
  `pool_name` varchar(255) NOT NULL,
  `vs_address` varchar(255) NOT NULL,
  `ratio` int(11) DEFAULT '1',
  PRIMARY KEY  (`pool_name`,`vs_address`),
  KEY `pool_name` (`pool_name`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `region_ip`
--

DROP TABLE IF EXISTS `region_ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `region_ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region_name` varchar(255) NOT NULL,
  `ip_start` int(10) unsigned NOT NULL,
  `ip_end` int(10) unsigned NOT NULL,
  `ip_prefix` int(10) unsigned DEFAULT NULL,
  `region_priority` int(10) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `ip_start` (`ip_prefix`,`region_priority`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `region_region`
--

DROP TABLE IF EXISTS `region_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `region_region` (
  `big_region` varchar(255) NOT NULL,
  `small_region` varchar(255) NOT NULL,
  `relation` int(11) NOT NULL,
  `custom_type` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY  (`big_region`,`small_region`),
  KEY `small_region` (`small_region`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vs`
--

DROP TABLE IF EXISTS `vs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vs` (
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `in_use` int(11) NOT NULL DEFAULT '1',
  `no_check` int(11) NOT NULL DEFAULT '0',
  `available` int(11) NOT NULL DEFAULT '1',
  `type` int(11) NOT NULL DEFAULT '0',
  `itvl` int(11) NOT NULL DEFAULT '10',
  `timeout` int(11) NOT NULL DEFAULT '5',
  `retries` int(11) NOT NULL DEFAULT '3',
  `port` int(11) NOT NULL DEFAULT '80',
  `host` varchar(1024) NOT NULL DEFAULT '',
  `uri` varchar(1024) NOT NULL DEFAULT '',
  PRIMARY KEY  (`name`),
  UNIQUE KEY (`address`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wideip_pool`
--

DROP TABLE IF EXISTS `wideip_pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wideip_pool` (
  `wideip_name` varchar(1024) NOT NULL,
  `pool_name` varchar(255) NOT NULL,
  `in_use` int(11) NOT NULL DEFAULT '1',
  `wideip_type` int(11) not null default '0',
  KEY `pool_name` (`pool_name`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
ALTER table wideip_pool add primary key(wideip_name(256),pool_name);
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `user_role`;
CREATE TABLE `user_role` (
   `user_name` varchar(128) NOT NULL,
   `role` tinyint(1) NOT NULL default 0,
   PRIMARY KEY  (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
insert into user_role values('lianming', 1);
insert into user_role values('daoxian', 1);
insert into user_role values('fenghan.ly', 1);

DROP TABLE IF EXISTS `git_commit_history`;
CREATE TABLE `git_commit_history` (
  `commit_time` datetime NOT NULL,
  `comment` varchar(1024) NOT NULL default '',
  `user_name` varchar(128) NOT NULL default '',
  `commit_md5` varchar(256) NOT NULL default '',
  `id` int(11) NOT NULL auto_increment,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB;


DROP TABLE IF EXISTS `zone_soa`;
CREATE TABLE `zone_soa` (
  `zone` varchar(255) NOT NULL,
  `ttl` int(11) NOT NULL DEFAULT '86400',
  `name_server` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `sn` int(11) NOT NULL DEFAULT '2012031100',
  `refresh` int(11) NOT NULL DEFAULT '10800',
  `retry` int(11) NOT NULL DEFAULT '3600',
  `expiry` int(11) NOT NULL DEFAULT '604800',
  `min` int(11) NOT NULL DEFAULT '10800',
  PRIMARY KEY (`zone`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;

INSERT INTO `zone_soa` VALUES ('a.hichinacdn.net',86400,'ans1.hichinacdn.net','root.taobao.com',1,3600,3600,360000,10800),('danuoyi.tbcache.com',10800,'danuoyins1.tbcache.com','root.taobao.com',2012031100,10800,3600,604800,10800),('mobgslb.tbcache.com',86400,'mobgslbns1.tbcache.com','root.taobao.com',1,3600,3600,360000,3600);

DROP TABLE IF EXISTS `zone_ns`;
CREATE TABLE `zone_ns` (
  `zone` varchar(255) NOT NULL,
  `ttl` int(11) NOT NULL DEFAULT '86400',
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`zone`,`value`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;


--
-- Dumping routines for database 'dns_config'
--
/*!50003 DROP PROCEDURE IF EXISTS `add_region_ip` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `add_region_ip`(
in rgn varchar(255),
in ips int unsigned,
in ipe int unsigned,
in pri int unsigned
)
func:begin
  declare ipp int unsigned;
  set ipp = ips&4294901760;
  loop0: while ipp <= ipe do
    insert into region_ip(region_name, ip_start, ip_end, ip_prefix, region_priority) value (rgn, ips, ipe, ipp, pri);
    set ipp = ipp + 65536;
  end while loop0;
end */;;
DELIMITER ;
/*!50003 DROP FUNCTION IF EXISTS `add_region_ip_filter` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 FUNCTION `add_region_ip_filter`(
rgn varchar(255),
ips int unsigned,
ipe int unsigned
) RETURNS int(11)
    READS SQL DATA
func:begin
  declare ipp int unsigned;
  declare ret int;

  select ip_start into ipp from region_ip ri LEFT JOIN region_region rr ON ri.region_name=rr.big_region AND rr.relation=0 where ipe>=ip_start and ips<=ip_end and ri.region_priority=1 limit 1;
  if ipp is not null then
    return 0;
    leave func;
  end if;

  set ipp = ips&4294901760;
  set ret = 0;
  loop0: while ipp <= ipe do
    insert into region_ip(region_name, ip_start, ip_end, ip_prefix, region_priority) value (rgn, ips, ipe, ipp, 1);
    set ret = 1;
    set ipp = ipp + 65536;
  end while loop0;
  return ret;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `lookup_only_vs` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `lookup_only_vs`(in wideip varchar(255), in ip varchar(255))
func:begin
  declare _dbid int;
  select dbid into _dbid from current_db where dbid > 0;
  if _dbid = 2 then
    call dns_config2.real_lookup_vs(wideip,ip,0);
  else
    call dns_config3.real_lookup_vs(wideip,ip,0);
  end if;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `lookup_vs` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `lookup_vs`(in wideip varchar(255), in ip varchar(255))
func:begin
  declare _dbid int;
  select dbid into _dbid from current_db where dbid > 0;
  if _dbid = 2 then
    call dns_config2.real_lookup_vs(wideip,ip,1);
  else
    call dns_config3.real_lookup_vs(wideip,ip,1);
  end if;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `real_update_vs_available` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `real_update_vs_available`(
in vs_addr char(255),
in avail int
)
func:begin
  declare selected_pool varchar(255);
  declare avail_vs int;
  declare stopFlag int;

  DECLARE pool_cur CURSOR for select pool_name from pool_vs pv join pool p on(pv.pool_name=p.name) where vs_address=vs_addr and p.type<>5;
  DECLARE CONTINUE HANDLER FOR NOT FOUND set stopFlag=1;

  set stopFlag=0;
  update vs set available = avail where address =  vs_addr;

  open pool_cur;
  REPEAT
  FETCH pool_cur INTO selected_pool;
  begin
    if stopFlag = 0 then
      select count(*) into avail_vs from pool_vs pv join vs on (pv.vs_address=vs.address) where pool_name = selected_pool and vs.available=1 and vs.in_use=1;
      if avail_vs = 0 then
	update pool set available = 0 where name =  selected_pool;
      else
	update pool set available = 1 where name =  selected_pool;
      end if;
    end if;
  end;
  UNTIL stopFlag = 1
  END REPEAT;
  CLOSE pool_cur;

end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `reload_data` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `reload_data`()
begin
  declare _dbid int;
  declare someone_reloading int;
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
      delete from current_db where dbid = -1;
    END;
  repeat
    start transaction;
    set someone_reloading = null;
    select dbid into someone_reloading from current_db where dbid = -1 for update;
    if someone_reloading is not null then
      commit;
      set @a=sleep(1);
    else
      insert into current_db values(-1);
      commit;
    end if;
    until someone_reloading is null
  end repeat;

  select dbid into _dbid from current_db where dbid > 0 limit 1;
  if _dbid = 2 then
    call dns_config3.real_reload_data();
    update current_db set dbid=3 where dbid > 0;
  else
    call dns_config2.real_reload_data();
    if _dbid is null then
      insert into current_db values(2);
    else
      update current_db set dbid=2 where dbid > 0;
    end if;
  end if;

  delete from current_db where dbid = -1;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `update_vs_available` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `update_vs_available`(
in vs_addr char(255),
in avail int
)
func:begin
  declare _dbid int;

  call dns_config.real_update_vs_available(vs_addr, avail);

  select dbid into _dbid from current_db where dbid > 0;
  if _dbid = 2 then
    call dns_config2.real_update_vs_available(vs_addr, avail);
  else
    call dns_config3.real_update_vs_available(vs_addr, avail);
  end if;

  select avail;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Current Database: `dns_config2`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `dns_config2` /*!40100 DEFAULT CHARACTER SET gbk */;

USE `dns_config2`;

--
-- Table structure for table `datacenter`
--

DROP TABLE IF EXISTS `datacenter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `datacenter` (
  `datacenter` varchar(255) NOT NULL DEFAULT '',
  `vs_name` varchar(255) NOT NULL DEFAULT ''
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `direct_region_pool`
--

DROP TABLE IF EXISTS `direct_region_pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `direct_region_pool` (
  `big_region` varchar(255) NOT NULL,
  `small_region` varchar(255) NOT NULL,
  `pool_name` varchar(255) NOT NULL,
  `region_name` varchar(255) NOT NULL,
  `score` int(11) NOT NULL,
  KEY `small_region` (`small_region`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pool`
--

DROP TABLE IF EXISTS `pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool` (
  `name` varchar(255) NOT NULL,
  `rr_ldns_limit` int(11) DEFAULT '1',
  `in_use` int(11) NOT NULL DEFAULT '1',
  `available` int(11) NOT NULL DEFAULT '1',
  `ttl` int(11) NOT NULL DEFAULT '300',
  `type` int(11) NOT NULL DEFAULT '1',
  `value` varchar(1024) DEFAULT NULL,
  KEY `name` (`name`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pool_region`
--

DROP TABLE IF EXISTS `pool_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool_region` (
  `pool_name` varchar(255) NOT NULL,
  `region_name` varchar(255) NOT NULL,
  `score` int(11) NOT NULL,
  PRIMARY KEY (pool_name, region_name),
  KEY `region_name` (`region_name`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pool_vs`
--

DROP TABLE IF EXISTS `pool_vs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool_vs` (
  `pool_name` varchar(255) NOT NULL,
  `vs_address` varchar(255) NOT NULL,
  `ratio` int(11) DEFAULT '1',
  KEY `pool_name` (`pool_name`),
  KEY `vs_address` (`vs_address`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `region_ip`
--

DROP TABLE IF EXISTS `region_ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `region_ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region_name` varchar(255) NOT NULL,
  `ip_start` int(10) unsigned NOT NULL,
  `ip_end` int(10) unsigned NOT NULL,
  `ip_prefix` int(10) unsigned DEFAULT NULL,
  `region_priority` int(10) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `ip_start` (`ip_prefix`,`region_priority`) USING BTREE
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `region_region`
--

DROP TABLE IF EXISTS `region_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `region_region` (
  `big_region` varchar(255) NOT NULL,
  `small_region` varchar(255) NOT NULL,
  `relation` int(11) NOT NULL,
  `custom_type` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY  (`big_region`,`small_region`),
  KEY `small_region` (`small_region`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `small_comple`
--

DROP TABLE IF EXISTS `small_comple`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `small_comple` (
  `small_region` varchar(255) NOT NULL,
  `comple_region` varchar(255) NOT NULL,
  PRIMARY KEY (`small_region`,`comple_region`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `comple_region`
--

DROP TABLE IF EXISTS `comple_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comple_region` (
  `original_name` varchar(255) NOT NULL,
  `comple_name` varchar(255) NOT NULL,
  PRIMARY KEY (`original_name`,`comple_name`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vs`
--

DROP TABLE IF EXISTS `vs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vs` (
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `in_use` int(11) NOT NULL DEFAULT '1',
  `no_check` int(11) NOT NULL DEFAULT '0',
  `available` int(11) NOT NULL DEFAULT '1',
  `type` int(11) NOT NULL DEFAULT '0',
  `itvl` int(11) NOT NULL DEFAULT '10',
  `timeout` int(11) NOT NULL DEFAULT '5',
  `retries` int(11) NOT NULL DEFAULT '3',
  `port` int(11) NOT NULL DEFAULT '80',
  `host` varchar(1024) NOT NULL DEFAULT '',
  `uri` varchar(1024) NOT NULL DEFAULT '',
  PRIMARY KEY  (`name`),
  UNIQUE KEY (`address`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wideip_pool`
--

DROP TABLE IF EXISTS `wideip_pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wideip_pool` (
  `wideip_name` varchar(1024) NOT NULL,
  `pool_name` varchar(255) NOT NULL,
  `in_use` int(11) NOT NULL DEFAULT '1',
  `wideip_type` int(11) not null default '0',
  KEY `pool_name` (`pool_name`),
  KEY `wideip_name` (`wideip_name`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'dns_config2'
--
/*!50003 DROP PROCEDURE IF EXISTS `real_lookup_vs` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `real_lookup_vs`(
in wideip varchar(255),
in ip char(15),
in show_all_result int
)
func:begin
  declare selected_pool varchar(255);
  declare selected_region varchar(255);
  declare selected_wideip varchar(255);
  declare vs_limit int;
  declare result_address varchar(255);
  declare result_ratio int;
  declare ipn int unsigned;
  declare log_code int;
  declare type_value int;
  declare need_return_null int;
  set log_code = 0;
  set type_value = 0;
  set need_return_null=0;
  set ipn = inet_aton(ip);




  select region_name into selected_region from region_ip where ipn >= ip_start and ipn <= ip_end and ip_prefix=ipn&4294901760 order by region_priority desc limit 1;
  if found_rows()=0 then
    set log_code = log_code | 1;
  end if;

  if selected_region is not null then
    select p.name  into selected_pool
      from direct_region_pool drp  join wideip_pool w on (drp.pool_name = w.pool_name) join pool p on (drp.pool_name=p.name)
      where drp.small_region=selected_region and  p.in_use=1 and p.available=1 and w.wideip_name=wideip and w.in_use=1
      order by score desc, rand() limit 1;
  else
    select p.name into selected_pool from comple_region cr join pool_region pr on (cr.comple_name=pr.region_name) join wideip_pool w on (pr.pool_name = w.pool_name) join pool p on (pr.pool_name=p.name)
      where p.in_use=1 and p.available=1 and w.wideip_name=wideip and w.in_use=1
      order by score desc, rand() limit 1;
  end if;

  if found_rows()=0 then
    set log_code = log_code | 16;
  end if;

  if selected_pool is null then

    set selected_wideip = null;
    select wideip_name into selected_wideip from wideip_pool where wideip_name=wideip limit 1;
    if selected_wideip is null then
      set log_code = log_code | 2;
      set need_return_null = 1;
    end if;

    set selected_pool = null;
    select pool_name into selected_pool from wideip_pool wp join pool p on(wp.pool_name=p.name) where wp.wideip_name=wideip and wp.in_use=1 and p.in_use=1 order by rand() limit 1;
    if selected_pool is null then
      set log_code = log_code | 4;
      set need_return_null = 1;
    end if;

    if need_return_null = 1 then
      if show_all_result=1 then
	select null as pool_name, null as rr_ldns_limit, null as ttl, null as type, null as value;
      end if;

      select null as vs_address, null as ratio;

      if show_all_result=1 then
	select selected_region, log_code;
      end if;

      leave func;
    end if;

    set selected_pool = null;
    select pool_name into selected_pool from wideip_pool wp join pool p on(wp.pool_name=p.name) where wp.wideip_name=wideip and wp.in_use=1 and p.available=1 and p.in_use=1 order by rand() limit 1;
    if selected_pool is null then
      set log_code = log_code | 4;
      set need_return_null = 2;
    end if;

   if need_return_null = 2 then
     if show_all_result=1 then
       select pool_name into selected_pool from wideip_pool wp join pool p on(wp.pool_name=p.name) where wp.wideip_name=wideip and wp.in_use=1 and p.in_use=1 order by rand() limit 1;
       select name,rr_ldns_limit,ttl,type,value from pool where name = selected_pool limit 1;
     end if;


  select pool_vs.vs_address , ratio into result_address, result_ratio
    from pool_vs, vs
    where pool_vs.pool_name = selected_pool and
      pool_vs.vs_address = vs.address and
	vs.in_use = 1 limit 1 ;

  if result_address is null then
    select null as vs_address, null as ratio;
    set log_code = log_code | 100;
  else
    select pool_vs.vs_address , ratio
      from pool_vs, vs
      where pool_vs.pool_name = selected_pool and
	pool_vs.vs_address = vs.address and
	  vs.in_use = 1;
  end if;

     if show_all_result=1 then
      select selected_region, log_code;
     end if;

     leave func;
   end if;

  end if;

  if show_all_result=1 then
    select name,rr_ldns_limit,ttl,type,value
      from pool where name = selected_pool limit 1;

    if found_rows() = 0 then
      set log_code = log_code | 4;
    end if;
  end if;

if show_all_result=0 then
  select type into type_value from pool where name= selected_pool;
  if type_value = 5 then
  select value as vs_address, -1 as ratio from pool where name= selected_pool;
  leave func;
  end if;
 end if;

  select pool_vs.vs_address , ratio into result_address, result_ratio
    from pool_vs, vs
    where pool_vs.pool_name = selected_pool and
      pool_vs.vs_address = vs.address and
	vs.in_use = 1 and vs.available = 1 limit 1 ;

  if result_address is null then
    select null as vs_address, null as ratio;
    set log_code = log_code | 32;
  else
    select pool_vs.vs_address , ratio
      from pool_vs, vs
      where pool_vs.pool_name = selected_pool and
	pool_vs.vs_address = vs.address and
	  vs.in_use = 1 and vs.available = 1 ;
  end if;

  if show_all_result=1 then
    select selected_region, log_code;
  end if;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `real_reload_data` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `real_reload_data`()
func:begin
  declare stopFlag int;
  DECLARE comple_rname varchar(255);
  DECLARE region_cur CURSOR for select comple_name from dns_config.comple_region;
  DECLARE CONTINUE HANDLER FOR NOT FOUND set stopFlag=1;

  truncate table pool;
  truncate table pool_region;
  truncate table pool_vs;
  truncate table region_ip;
  truncate table region_region;
  truncate table vs;
  truncate table wideip_pool;
  truncate table datacenter;
  truncate table comple_region;
  truncate table small_comple;
  truncate table direct_region_pool;

  insert ignore into pool (select * from dns_config.pool);
  insert ignore into pool_region (select * from dns_config.pool_region);
  insert ignore into pool_vs (select * from dns_config.pool_vs);
  insert ignore into region_ip (select * from dns_config.region_ip);
  insert ignore into region_region (select * from dns_config.region_region);
  insert ignore into vs (select * from dns_config.vs);
  insert ignore into wideip_pool (select * from dns_config.wideip_pool);
  insert ignore into datacenter (select * from dns_config.datacenter);
  insert ignore into comple_region (select * from dns_config.comple_region);

  set stopFlag = 0;
  open region_cur;
  REPEAT
  FETCH region_cur INTO comple_rname;
  begin
    if stopFlag = 0 then
      insert ignore into small_comple select distinct ro.small_region,comple_rname from region_region ro left join (select distinct small_region, comple_name,big_region from region_region rr, dns_config.comple_region cr where rr.big_region=cr.original_name and cr.comple_name=comple_rname) t on (ro.small_region=t.small_region) where t.small_region is  null;
    end if;
  end;
  UNTIL stopFlag = 1
  END REPEAT;
  insert into region_region  (big_region, small_region, relation) select comple_region, small_region, -1 from small_comple;
  insert into direct_region_pool (select big_region, small_region, pool_name, region_name, score from region_region rr join pool_region pr on (rr.big_region=pr.region_name) order by small_region , score );
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `real_update_vs_available` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `real_update_vs_available`(
in vs_addr char(255),
in avail int
)
func:begin
  declare selected_pool varchar(255);
  declare avail_vs int;
  declare stopFlag int;

  DECLARE pool_cur CURSOR for select pool_name from pool_vs pv join pool p on(pv.pool_name=p.name) where vs_address=vs_addr and p.type<>5;
  DECLARE CONTINUE HANDLER FOR NOT FOUND set stopFlag=1;

  set stopFlag=0;
  update vs set available = avail where address =  vs_addr;

  open pool_cur;
  REPEAT
  FETCH pool_cur INTO selected_pool;
  begin
    if stopFlag = 0 then
      select count(*) into avail_vs from pool_vs pv join vs on (pv.vs_address=vs.address) where pool_name = selected_pool and vs.available=1 and vs.in_use=1;
      if avail_vs = 0 then
	update pool set available = 0 where name =  selected_pool;
      else
	update pool set available = 1 where name =  selected_pool;
      end if;
    end if;
  end;
  UNTIL stopFlag = 1
  END REPEAT;
  CLOSE pool_cur;

end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Current Database: `dns_config3`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `dns_config3` /*!40100 DEFAULT CHARACTER SET gbk */;

USE `dns_config3`;

--
-- Table structure for table `datacenter`
--

DROP TABLE IF EXISTS `datacenter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `datacenter` (
  `datacenter` varchar(255) NOT NULL DEFAULT '',
  `vs_name` varchar(255) NOT NULL DEFAULT ''
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `direct_region_pool`
--

DROP TABLE IF EXISTS `direct_region_pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `direct_region_pool` (
  `big_region` varchar(255) NOT NULL,
  `small_region` varchar(255) NOT NULL,
  `pool_name` varchar(255) NOT NULL,
  `region_name` varchar(255) NOT NULL,
  `score` int(11) NOT NULL,
  KEY `small_region` (`small_region`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pool`
--

DROP TABLE IF EXISTS `pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool` (
  `name` varchar(255) NOT NULL,
  `rr_ldns_limit` int(11) DEFAULT '1',
  `in_use` int(11) NOT NULL DEFAULT '1',
  `available` int(11) NOT NULL DEFAULT '1',
  `ttl` int(11) NOT NULL DEFAULT '300',
  `type` int(11) NOT NULL DEFAULT '1',
  `value` varchar(1024) DEFAULT NULL,
  KEY `name` (`name`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pool_region`
--

DROP TABLE IF EXISTS `pool_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool_region` (
  `pool_name` varchar(255) NOT NULL,
  `region_name` varchar(255) NOT NULL,
  `score` int(11) NOT NULL,
  PRIMARY KEY (pool_name, region_name),
  KEY `region_name` (`region_name`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pool_vs`
--

DROP TABLE IF EXISTS `pool_vs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pool_vs` (
  `pool_name` varchar(255) NOT NULL,
  `vs_address` varchar(255) NOT NULL,
  `ratio` int(11) DEFAULT '1',
  KEY `pool_name` (`pool_name`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `region_ip`
--

DROP TABLE IF EXISTS `region_ip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `region_ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region_name` varchar(255) NOT NULL,
  `ip_start` int(10) unsigned NOT NULL,
  `ip_end` int(10) unsigned NOT NULL,
  `ip_prefix` int(10) unsigned DEFAULT NULL,
  `region_priority` int(10) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `ip_start` (`ip_prefix`,`region_priority`) USING BTREE
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `region_region`
--

DROP TABLE IF EXISTS `region_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `region_region` (
  `big_region` varchar(255) NOT NULL,
  `small_region` varchar(255) NOT NULL,
  `relation` int(11) NOT NULL,
  `custom_type` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY  (`big_region`,`small_region`),
  KEY `small_region` (`small_region`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `small_comple`
--

DROP TABLE IF EXISTS `small_comple`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `small_comple` (
  `small_region` varchar(255) NOT NULL,
  `comple_region` varchar(255) NOT NULL,
  PRIMARY KEY (`small_region`,`comple_region`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `comple_region`
--

DROP TABLE IF EXISTS `comple_region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comple_region` (
  `original_name` varchar(255) NOT NULL,
  `comple_name` varchar(255) NOT NULL,
  PRIMARY KEY (`original_name`,`comple_name`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vs`
--

DROP TABLE IF EXISTS `vs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vs` (
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `in_use` int(11) NOT NULL DEFAULT '1',
  `no_check` int(11) NOT NULL DEFAULT '0',
  `available` int(11) NOT NULL DEFAULT '1',
  `type` int(11) NOT NULL DEFAULT '0',
  `itvl` int(11) NOT NULL DEFAULT '10',
  `timeout` int(11) NOT NULL DEFAULT '5',
  `retries` int(11) NOT NULL DEFAULT '3',
  `port` int(11) NOT NULL DEFAULT '80',
  `host` varchar(1024) NOT NULL DEFAULT '',
  `uri` varchar(1024) NOT NULL DEFAULT '',
  PRIMARY KEY  (`name`),
  UNIQUE KEY (`address`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wideip_pool`
--

DROP TABLE IF EXISTS `wideip_pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wideip_pool` (
  `wideip_name` varchar(1024) NOT NULL,
  `pool_name` varchar(255) NOT NULL,
  `in_use` int(11) NOT NULL DEFAULT '1',
  `wideip_type` int(11) not null default '0',
  KEY `pool_name` (`pool_name`),
  KEY `wideip_name` (`wideip_name`)
) ENGINE=MEMORY DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'dns_config3'
--
/*!50003 DROP PROCEDURE IF EXISTS `real_lookup_vs` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `real_lookup_vs`(
in wideip varchar(255),
in ip char(15),
in show_all_result int
)
func:begin
  declare selected_pool varchar(255);
  declare selected_region varchar(255);
  declare selected_wideip varchar(255);
  declare vs_limit int;
  declare result_address varchar(255);
  declare result_ratio int;
  declare ipn int unsigned;
  declare log_code int;
  declare type_value int;
  declare need_return_null int;
  set log_code = 0;
  set type_value = 0;
  set need_return_null=0;
  set ipn = inet_aton(ip);




  select region_name into selected_region from region_ip where ipn >= ip_start and ipn <= ip_end and ip_prefix=ipn&4294901760 order by region_priority desc limit 1;
  if found_rows()=0 then
    set log_code = log_code | 1;
  end if;

  if selected_region is not null then
    select p.name  into selected_pool
      from direct_region_pool drp  join wideip_pool w on (drp.pool_name = w.pool_name) join pool p on (drp.pool_name=p.name)
      where drp.small_region=selected_region and  p.in_use=1 and p.available=1 and w.wideip_name=wideip and w.in_use=1
      order by score desc, rand() limit 1;
  else
    select p.name into selected_pool from comple_region cr join pool_region pr on (cr.comple_name=pr.region_name) join wideip_pool w on (pr.pool_name = w.pool_name) join pool p on (pr.pool_name=p.name)
      where p.in_use=1 and p.available=1 and w.wideip_name=wideip and w.in_use=1
      order by score desc, rand() limit 1;
  end if;

  if found_rows()=0 then
    set log_code = log_code | 16;
  end if;

  if selected_pool is null then

    set selected_wideip = null;
    select wideip_name into selected_wideip from wideip_pool where wideip_name=wideip limit 1;
    if selected_wideip is null then
      set log_code = log_code | 2;
      set need_return_null = 1;
    end if;

    set selected_pool = null;
    select pool_name into selected_pool from wideip_pool wp join pool p on(wp.pool_name=p.name) where wp.wideip_name=wideip and wp.in_use=1 and p.in_use=1 order by rand() limit 1;
    if selected_pool is null then
      set log_code = log_code | 4;
      set need_return_null = 1;
    end if;

    if need_return_null = 1 then
      if show_all_result=1 then
	select null as pool_name, null as rr_ldns_limit, null as ttl, null as type, null as value;
      end if;

      select null as vs_address, null as ratio;

      if show_all_result=1 then
	select selected_region, log_code;
      end if;

      leave func;
    end if;

    set selected_pool = null;
    select pool_name into selected_pool from wideip_pool wp join pool p on(wp.pool_name=p.name) where wp.wideip_name=wideip and wp.in_use=1 and p.available=1 and p.in_use=1 order by rand() limit 1;
    if selected_pool is null then
      set log_code = log_code | 4;
      set need_return_null = 2;
    end if;


    if need_return_null = 2 then
     if show_all_result=1 then
       select pool_name into selected_pool from wideip_pool wp join pool p on(wp.pool_name=p.name) where wp.wideip_name=wideip and wp.in_use=1 and p.in_use=1 order by rand() limit 1;
       select name,rr_ldns_limit,ttl,type,value from pool where name = selected_pool limit 1;
     end if;


  select pool_vs.vs_address , ratio into result_address, result_ratio
    from pool_vs, vs
    where pool_vs.pool_name = selected_pool and
      pool_vs.vs_address = vs.address and
	vs.in_use = 1 limit 1 ;

  if result_address is null then
    select null as vs_address, null as ratio;
    set log_code = log_code | 100;
  else
    select pool_vs.vs_address , ratio
      from pool_vs, vs
      where pool_vs.pool_name = selected_pool and
	pool_vs.vs_address = vs.address and
	  vs.in_use = 1;
  end if;


     if show_all_result=1 then
      select selected_region, log_code;
     end if;

     leave func;
   end if;

  end if;

  if show_all_result=1 then
    select name,rr_ldns_limit,ttl,type,value
      from pool where name = selected_pool limit 1;

    if found_rows() = 0 then
      set log_code = log_code | 4;
    end if;
  end if;
  
if show_all_result=0 then
  select type into type_value from pool where name= selected_pool;
  if type_value = 5 then
  select value as vs_address, -1 as ratio from pool where name= selected_pool;
  leave func;
  end if;
 end if;

  select pool_vs.vs_address , ratio into result_address, result_ratio
    from pool_vs, vs
    where pool_vs.pool_name = selected_pool and
      pool_vs.vs_address = vs.address and
	vs.in_use = 1 and vs.available = 1 limit 1 ;

  if result_address is null then
    select null as vs_address, null as ratio;
    set log_code = log_code | 32;
  else
    select pool_vs.vs_address , ratio
      from pool_vs, vs
      where pool_vs.pool_name = selected_pool and
	pool_vs.vs_address = vs.address and
	  vs.in_use = 1 and vs.available = 1 ;
  end if;

  if show_all_result=1 then
    select selected_region, log_code;
  end if;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `real_reload_data` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `real_reload_data`()
func:begin
  declare stopFlag int;
  DECLARE comple_rname varchar(255);
  DECLARE region_cur CURSOR for select comple_name from dns_config.comple_region;
  DECLARE CONTINUE HANDLER FOR NOT FOUND set stopFlag=1;

  truncate table pool;
  truncate table pool_region;
  truncate table pool_vs;
  truncate table region_ip;
  truncate table region_region;
  truncate table vs;
  truncate table wideip_pool;
  truncate table datacenter;
  truncate table small_comple;
  truncate table direct_region_pool;
  truncate table comple_region;

  insert ignore into pool (select * from dns_config.pool);
  insert ignore into pool_region (select * from dns_config.pool_region);
  insert ignore into pool_vs (select * from dns_config.pool_vs);
  insert ignore into region_ip (select * from dns_config.region_ip);
  insert ignore into region_region (select * from dns_config.region_region);
  insert ignore into vs (select * from dns_config.vs);
  insert ignore into wideip_pool (select * from dns_config.wideip_pool);
  insert ignore into datacenter (select * from dns_config.datacenter);
  insert ignore into comple_region (select * from dns_config.comple_region);

  set stopFlag = 0;
  open region_cur;
  REPEAT
  FETCH region_cur INTO comple_rname;
  begin
    if stopFlag = 0 then
      insert ignore into small_comple select distinct ro.small_region,comple_rname from region_region ro left join (select distinct small_region, comple_name,big_region from region_region rr, dns_config.comple_region cr where rr.big_region=cr.original_name and cr.comple_name=comple_rname) t on (ro.small_region=t.small_region) where t.small_region is  null;
    end if;
  end;
  UNTIL stopFlag = 1
  END REPEAT;
  insert into region_region  (big_region, small_region, relation) select comple_region, small_region, -1 from small_comple;
  insert into direct_region_pool (select big_region, small_region, pool_name, region_name, score from region_region rr join pool_region pr on (rr.big_region=pr.region_name) order by small_region , score );
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `real_update_vs_available` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `real_update_vs_available`(
in vs_addr char(255),
in avail int
)
func:begin
  declare selected_pool varchar(255);
  declare avail_vs int;
  declare stopFlag int;

  DECLARE pool_cur CURSOR for select pool_name from pool_vs pv join pool p on(pv.pool_name=p.name) where vs_address=vs_addr and p.type<>5;
  DECLARE CONTINUE HANDLER FOR NOT FOUND set stopFlag=1;

  set stopFlag=0;
  update vs set available = avail where address =  vs_addr;

  open pool_cur;
  REPEAT
  FETCH pool_cur INTO selected_pool;
  begin
    if stopFlag = 0 then
      select count(*) into avail_vs from pool_vs pv join vs on (pv.vs_address=vs.address) where pool_name = selected_pool and vs.available=1 and vs.in_use=1;
      if avail_vs = 0 then
	update pool set available = 0 where name =  selected_pool;
      else
	update pool set available = 1 where name =  selected_pool;
      end if;
    end if;
  end;
  UNTIL stopFlag = 1
  END REPEAT;
  CLOSE pool_cur;

end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;



USE dns_config;

DROP TABLE IF EXISTS `cluster_info`;
CREATE TABLE `cluster_info` (
  `name` varchar(128) NOT NULL DEFAULT '',
  `ns_from_member` text NOT NULL DEFAULT '',
  PRIMARY KEY (`name`)
) ENGINE=InnoDB;


DROP TABLE IF EXISTS `cluster_member`;
CREATE TABLE `cluster_member` (
  `cluster_name` varchar(128) NOT NULL DEFAULT '',
  `member_name` varchar(256) NOT NULL,
  PRIMARY KEY (`cluster_name`,`member_name`)
)ENGINE=InnoDB;


DROP TABLE IF EXISTS `cluster_region`;
CREATE TABLE `cluster_region` (
  `cluster_name` varchar(128) NOT NULL DEFAULT '',
  `region_name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`cluster_name`,`region_name`)
)ENGINE=InnoDB;

DROP TABLE IF EXISTS `pharos_info`;
CREATE TABLE `pharos_info` (
  `pharos_name` varchar(256) NOT NULL DEFAULT '',
  `service_ip` varchar(16) DEFAULT '',
  `node` varchar(16) NOT NULL DEFAULT '',
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`pharos_name`)
) ENGINE=InnoDB;


DROP TABLE IF EXISTS `datacenter_info`;
CREATE TABLE `datacenter_info` (
  `node_name` varchar(64) NOT NULL DEFAULT '',
  `node_type` int(11) NOT NULL DEFAULT '0',
  `isp` varchar(128) NOT NULL DEFAULT '',
  `region` varchar(128) NOT NULL DEFAULT '',
  `capacity` varchar(32) NOT NULL DEFAULT '',
  `memo` text NOT NULL,
  PRIMARY KEY (`node_name`)
)ENGINE=InnoDB;


DROP TABLE IF EXISTS `introduce_channel`;
CREATE TABLE `introduce_channel` (
  `channel_name` varchar(256) NOT NULL,
  `introduce_name` varchar(128) NOT NULL DEFAULT '',
  PRIMARY KEY (`channel_name`)
)ENGINE=InnoDB;


DROP TABLE IF EXISTS `slave_vs`;
CREATE TABLE `slave_vs` (
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `in_use` int(11) NOT NULL DEFAULT '1',
  `available` int(11) NOT NULL DEFAULT '1',
  `type` int(11) NOT NULL DEFAULT '0',
  `itvl` int(11) NOT NULL DEFAULT '10',
  `timeout` int(11) NOT NULL DEFAULT '5',
  `retries` int(11) NOT NULL DEFAULT '3',
  `port` int(11) NOT NULL DEFAULT '80',
  `host` varchar(1024) NOT NULL DEFAULT '',
  `uri` varchar(1024) NOT NULL DEFAULT '',
  `pharos_name` varchar(255) NOT NULL DEFAULT '',
  `no_check` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`pharos_name`,`name`),
  KEY `address` (`address`)
) ENGINE=InnoDB;


DROP TABLE IF EXISTS `slave_pool`;
CREATE TABLE `slave_pool` (
  `name` varchar(255) NOT NULL,
  `rr_ldns_limit` int(11) DEFAULT '1',
  `in_use` int(11) NOT NULL DEFAULT '1',
  `available` int(11) NOT NULL DEFAULT '1',
  `ttl` int(11) NOT NULL DEFAULT '300',
  `type` int(11) NOT NULL DEFAULT '1',
  `value` varchar(1024) DEFAULT NULL,
  `pharos_name` varchar(256) NOT NULL DEFAULT '',
  PRIMARY KEY (`pharos_name`,`name`)
) ENGINE=InnoDB;


DROP TABLE IF EXISTS `increment_sql`;
CREATE TABLE `increment_sql` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`sql_string` varchar(512) DEFAULT NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB;


DROP TABLE IF EXISTS `ipdata_update_record`;
CREATE TABLE `ipdata_update_record` (
  `task_id` int(11) NOT NULL AUTO_INCREMENT,
  `ver_from` varchar(64) DEFAULT NULL,
  `ver_to` varchar(64) DEFAULT NULL,
  `operator` varchar(64) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`task_id`)
) ENGINE=InnoDB;


DROP TABLE IF EXISTS `region_affected`;
CREATE TABLE `region_affected` (
  `region_name` varchar(128) DEFAULT NULL,
  `flag_schedule` int(11) DEFAULT NULL,
  `flag_add_remove` int(11) DEFAULT NULL,
  `num_out` int(11) DEFAULT NULL,
  `num_in` int(11) DEFAULT NULL,
  `num_combine` int(11) DEFAULT NULL
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `ipdata_version`;
CREATE TABLE `ipdata_version` (
  `id` varchar(64) NOT NULL DEFAULT 'current_version',
  `version` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;


CREATE DATABASE /*!32312 IF NOT EXISTS*/ `ipdata_update` /*!40100 DEFAULT CHARACTER SET gbk */;

USE `ipdata_update`;

DROP TABLE IF EXISTS `region_ip_new`;
CREATE TABLE `region_ip_new` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region_name` varchar(255) NOT NULL,
  `ip_start` int(10) unsigned NOT NULL,
  `ip_end` int(10) unsigned NOT NULL,
  `ip_prefix` int(10) unsigned DEFAULT NULL,
  `region_priority` int(10) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `ip_start` (`ip_prefix`,`ip_start`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `region_region_new`;
CREATE TABLE `region_region_new` (
  `big_region` varchar(255) NOT NULL,
  `small_region` varchar(255) NOT NULL,
  `relation` int(11) NOT NULL,
  `custom_type` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`big_region`,`small_region`),
  KEY `small_region` (`small_region`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `ipdata_version_new`;
CREATE TABLE `ipdata_version_new` (
  `id` varchar(64) NOT NULL DEFAULT 'current_version',
  `version` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `ipdata_diff`;
CREATE TABLE `ipdata_diff` (
  `lipstart` int(11) unsigned NOT NULL,
  `lipend` int(11) unsigned NOT NULL,
  `region_old` varchar(128) DEFAULT NULL,
  `region_new` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`lipstart`,`lipend`)
) ENGINE=InnoDB;

-- Dump completed on 2011-11-15 11:10:20

