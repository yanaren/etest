
use dns_config;

-- 临时内存表，辅助做扁平化
DROP TABLE if EXISTS ri_tmp;
CREATE TABLE ri_tmp (
  region_name varchar(255),
  key region_name (region_name)
) engine=memory DEFAULT charset=utf8;

DROP TABLE if EXISTS rr_tmp;
CREATE TABLE rr_tmp (
  big_region varchar(255),
  small_region varchar(255),
  relation int(11),
  custom_type int(11) DEFAULT 0,
  key small_region(small_region),
  key big_region(big_region)
) engine=memory DEFAULT charset=utf8;



-- 更改表
-- 为pool增加v6的状态信息
ALTER TABLE pool ADD COLUMN a6_available int(11) DEFAULT 0 AFTER available;
-- 为vs增加类型表示address_type
ALTER TABLE vs ADD COLUMN address_type int(11) DEFAULT 1 AFTER address;

-- 注意: pool表里面的type字段在A或AAAA时无意义,frs_pool的type字段有意义;

-- 新增的srv信息表
DROP TABLE if EXISTS pool_srv;
CREATE TABLE pool_srv (
  pool_name varchar(255),
  srv varchar(1024),
  in_use int(11),
  pri int(11),
  weight int(11),
  port int(11),
  key pool_name(pool_name)
) engine=innodb DEFAULT charset=utf8;

insert into pool_srv values('WangTong_Beijing_SRV_Pool', 'host1.taobao.com', 1, 2, 3, 5333);
insert into pool_srv values('WangTong_Beijing_SRV_Pool', 'host2.taobao.com', 1, 3, 2, 5333);
insert into pool_srv values('WangTong_Beijing_SRV_Pool', 'host3.taobao.com', 1, 2, 2, 5333);

-- pool的扁平化结果表
DROP TABLE if EXISTS frs_pool;
CREATE TABLE frs_pool (
  name varchar(255),
  rr_ldns_limit int(11),
  ttl int(11),
  type int(11),
  value varchar(255),
  pri  int(11),
  weight int(11),
  port int(11),
  available int(11) default 1,
  a6_available int(11) default 0
) engine=memory DEFAULT charset=utf8;


-- topology的扁平化结果表
DROP TABLE if EXISTS frs_topo;
CREATE TABLE frs_topo (
  region_name varchar(255),
  wideip_name varchar(255),
  pool_name varchar(255),
  score int(11),
  type int(11)
) engine=memory DEFAULT charset=utf8;


-- wideip_pool的扁平化结果表
-- frs_wp存放in_use的wideip包含的in_use的pool
DROP TABLE if EXISTS frs_wideip_pool;
CREATE TABLE frs_wideip_pool (
  wideip_name varchar(1024),
  pool_name varchar(255),
  available int(11),
  a6_available int(11)
) engine=memory DEFAULT charset=utf8;


-- region_ip 表的扁平化结果表
DROP TABLE IF EXISTS `frs_region_ip`;
CREATE TABLE IF NOT EXISTS `frs_region_ip` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `region_name` varchar(255) NOT NULL,
 `ip_start` int(10) unsigned NOT NULL,
 `ip_end` int(10) unsigned NOT NULL,
 `priority` int (10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT charset=utf8;

-- 标识扁平化数据的版本号
-- 每次扁平化操作之后版本号增1
DROP TABLE IF EXISTS `frs_serial_num`;
CREATE TABLE IF NOT EXISTS `frs_serial_num` (
 `sn` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT charset=utf8;
INSERT INTO frs_serial_num values(6);

