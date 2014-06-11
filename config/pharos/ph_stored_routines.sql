DELIMITER ;;

USE dns_config;;

DROP PROCEDURE if exists gen_frs_region_ip;;
CREATE PROCEDURE gen_frs_region_ip()
begin
    declare cmos_region varchar(255);
    declare cmos_start  int unsigned;
    declare cmos_end    int unsigned;
    declare std_id      int unsigned;
    declare std_region  varchar(255);
    declare std_start   int unsigned;
    declare std_end     int unsigned;
    declare std_pri     int unsigned;
    declare is_stop     boolean default false;


    DECLARE cmos_cur CURSOR FOR
        SELECT region_name, ip_start, ip_end FROM region_ip
        WHERE region_priority = 1;
    DECLARE auto_cur CURSOR FOR
        SELECT region_name, ip_start, ip_end FROM region_ip
        WHERE region_priority = 2;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET is_stop = true;

    TRUNCATE TABLE frs_region_ip;

    INSERT INTO frs_region_ip(region_name, ip_start, ip_end, priority)
    (SELECT DISTINCT region_name, ip_start, ip_end, region_priority
    FROM region_ip WHERE region_priority = 0);


    OPEN cmos_cur;
    cmos_loop: LOOP
        FETCH cmos_cur INTO cmos_region, cmos_start, cmos_end;
        if is_stop then
          CLOSE cmos_cur;
          LEAVE cmos_loop;
        end if;


        SET std_id = null;
        SELECT id, region_name, ip_start, ip_end, priority
        INTO std_id, std_region, std_start, std_end, std_pri
        FROM frs_region_ip WHERE ip_start <= cmos_start AND ip_end >= cmos_end;

        if std_id is not null then
        -- Cmos:            --------------
        -- Standard:   -----------------------
            DELETE FROM frs_region_ip WHERE id = std_id;

            if std_start != cmos_start then
                INSERT INTO frs_region_ip(region_name, ip_start, ip_end, priority)
                    VALUES(std_region, std_start, cmos_start - 1, std_pri);
            end if;

            if std_end != cmos_end then
                INSERT INTO frs_region_ip(region_name, ip_start, ip_end, priority)
                    VALUES(std_region, cmos_end + 1, std_end, std_pri);
            end if;

        else
            -- Deal with :
            -- Cmos:             --------------------------
            -- Standard:   ---------  -----  ------   ----------


            -- 1,    a,    --------   b,   --------   c,  --------
            --             ----              ----           ------
            DELETE FROM frs_region_ip where ip_start >= cmos_start AND ip_end <= cmos_end;


            -- 2,               --------
            --             -------
            SET std_id = null;
            SELECT id, region_name, ip_start, ip_end
            INTO std_id, std_region, std_start, std_end
            FROM frs_region_ip
            WHERE ip_start < cmos_start AND ip_end < cmos_end AND ip_end >= cmos_start;

            if std_id is not null then
                UPDATE frs_region_ip SET ip_end = cmos_start - 1 WHERE id = std_id;
            end if;

            -- 3,           --------
            --                   -------
            SET std_id = null;
            SELECT id, region_name, ip_start, ip_end
            INTO std_id, std_region, std_start, std_end
            FROM frs_region_ip
            WHERE ip_start > cmos_start AND ip_end > cmos_end AND ip_start <= cmos_end;

            if std_id is not null then
                UPDATE frs_region_ip SET ip_start = cmos_end + 1 WHERE id = std_id;
            end if;

        end if;

        INSERT INTO frs_region_ip(region_name, ip_start, ip_end, priority)
            VALUES(cmos_region, cmos_start, cmos_end, 1);

        SET is_stop = false;

    END LOOP cmos_loop;


    set is_stop = false;
    OPEN auto_cur;
    auto_loop: LOOP
        FETCH auto_cur INTO cmos_region, cmos_start, cmos_end;
        if is_stop then
          CLOSE auto_cur;
          LEAVE auto_loop;
        end if;

        SET std_id = null;
        SELECT id, region_name, ip_start, ip_end, priority
        INTO std_id, std_region, std_start, std_end, std_pri
        FROM frs_region_ip WHERE ip_start <= cmos_start AND ip_end >= cmos_end;

        if std_id is not null then
        -- Cmos:            --------------
        -- Standard:   -----------------------
            DELETE FROM frs_region_ip WHERE id = std_id;

            if std_start != cmos_start then
                INSERT INTO frs_region_ip(region_name, ip_start, ip_end, priority)
                    VALUES(std_region, std_start, cmos_start - 1, std_pri);
            end if;

            if std_end != cmos_end then
                INSERT INTO frs_region_ip(region_name, ip_start, ip_end, priority)
                    VALUES(std_region, cmos_end + 1, std_end, std_pri);
            end if;

        else
            -- Deal with :
            -- Cmos:             --------------------------
            -- Standard:   ---------  -----  ------   ----------


            -- 1,    a,    --------   b,   --------   c,  --------
            --             ----              ----           ------
            DELETE FROM frs_region_ip where ip_start >= cmos_start AND ip_end <= cmos_end;


            -- 2,               --------
            --             -------
            SET std_id = null;
            SELECT id, region_name, ip_start, ip_end
            INTO std_id, std_region, std_start, std_end
            FROM frs_region_ip
            WHERE ip_start < cmos_start AND ip_end < cmos_end AND ip_end >= cmos_start;

            if std_id is not null then
                UPDATE frs_region_ip SET ip_end = cmos_start - 1 WHERE id = std_id;
            end if;

            -- 3,           --------
            --                   -------
            SET std_id = null;
            SELECT id, region_name, ip_start, ip_end
            INTO std_id, std_region, std_start, std_end
            FROM frs_region_ip
            WHERE ip_start > cmos_start AND ip_end > cmos_end AND ip_start <= cmos_end;

            if std_id is not null then
                UPDATE frs_region_ip SET ip_start = cmos_end + 1 WHERE id = std_id;
            end if;

        end if;

        INSERT INTO frs_region_ip(region_name, ip_start, ip_end, priority)
            VALUES(cmos_region, cmos_start, cmos_end, 2);

        SET is_stop = false;
    END LOOP auto_loop;

end ;;


DROP PROCEDURE if exists gen_frs_topo;;
CREATE PROCEDURE gen_frs_topo()
begin

    declare stop_flag int default 0;
    declare comple_rname varchar(255);

    DECLARE region_cur CURSOR FOR
      SELECT comple_name FROM comple_region;
    DECLARE CONTINUE HANDLER FOR NOT FOUND set stop_flag = 1;

    TRUNCATE TABLE rr_tmp;
    TRUNCATE TABLE ri_tmp;
    TRUNCATE TABLE frs_topo;

    INSERT IGNORE INTO rr_tmp (SELECT * FROM region_region);
    INSERT IGNORE INTO ri_tmp (SELECT DISTINCT region_name FROM region_ip);

    set stop_flag = 0;
    OPEN region_cur;
    region_loop: LOOP
        FETCH region_cur INTO comple_rname;
        if stop_flag then
            CLOSE region_cur;
            LEAVE region_loop;
        end if;

        INSERT IGNORE INTO rr_tmp(small_region, big_region, relation)
        SELECT DISTINCT ro.small_region, comple_rname, -1
        FROM region_region ro LEFT JOIN (
            SELECT DISTINCT small_region, comple_name, big_region
            FROM region_region rr, dns_config.comple_region cr
            WHERE rr.big_region = cr.original_name and cr.comple_name = comple_rname) t
        ON (ro.small_region = t.small_region)
        WHERE t.small_region is null;

    END LOOP region_loop;

    INSERT IGNORE INTO frs_topo(region_name, wideip_name, pool_name, score, type)
    SELECT rr_tmp.small_region, wp.wideip_name, wp.pool_name, pr.score, 1
    FROM ri_tmp
    JOIN rr_tmp ON (ri_tmp.region_name = rr_tmp.small_region)
    JOIN pool_region pr ON (rr_tmp.big_region = pr.region_name)
    JOIN wideip_pool wp ON (pr.pool_name = wp.pool_name)
    JOIN pool p ON (wp.pool_name = p.name)
    WHERE p.in_use = 1 and p.available = 1 and wp.in_use = 1;

    INSERT IGNORE INTO frs_topo(region_name, wideip_name, pool_name, score, type)
    SELECT rr_tmp.small_region, wp.wideip_name, wp.pool_name, pr.score, 28
    FROM ri_tmp
    JOIN rr_tmp ON (ri_tmp.region_name = rr_tmp.small_region)
    JOIN pool_region pr ON (rr_tmp.big_region = pr.region_name)
    JOIN wideip_pool wp ON (pr.pool_name = wp.pool_name)
    JOIN pool p ON (wp.pool_name = p.name)
    WHERE p.in_use = 1 and p.a6_available = 1 and wp.in_use = 1;

end;;


DROP PROCEDURE if exists gen_frs_pool;;
CREATE PROCEDURE gen_frs_pool()
begin

    TRUNCATE TABLE frs_pool;

    INSERT IGNORE INTO frs_pool
    SELECT p.name, p.rr_ldns_limit, p.ttl, 1, pv.vs_address, pv.ratio, -1, -1, vs.available, 0
    FROM pool p
    JOIN pool_vs pv
    ON (p.name = pv.pool_name)
    JOIN vs on (vs.address = pv.vs_address)
    WHERE vs.address_type = 1 AND vs.in_use = 1;

    INSERT IGNORE INTO frs_pool
    SELECT p.name, p.rr_ldns_limit, p.ttl, 28, pv.vs_address, pv.ratio, -1, -1, 0, vs.available
    FROM pool p
    JOIN pool_vs pv
    ON (p.name = pv.pool_name)
    JOIN vs on (vs.address = pv.vs_address)
    WHERE vs.address_type = 28 AND vs.in_use = 1;

    INSERT IGNORE INTO frs_pool
    SELECT p.name, p.rr_ldns_limit, p.ttl, 33, ps.srv, ps.pri, ps.weight, ps.port, 0, 0
    FROM pool p
    JOIN pool_srv ps on (p.name = ps.pool_name)
    WHERE ps.in_use = 1;

    INSERT IGNORE INTO frs_pool
    SELECT p.name, p.rr_ldns_limit, p.ttl, p.type, p.value, -1, -1, -1, 0, 0
    FROM pool p WHERE p.type = 5;

end ;;


DROP PROCEDURE if exists gen_frs_wideip_pool;;
CREATE PROCEDURE gen_frs_wideip_pool()
begin

    TRUNCATE TABLE frs_wideip_pool;

    INSERT IGNORE INTO frs_wideip_pool
        SELECT wp.wideip_name, wp.pool_name, p.available, p.a6_available
        FROM wideip_pool wp
        JOIN pool p
        ON (wp.pool_name = p.name)
        WHERE wp.in_use = 1 and p.in_use = 1;

end ;;


DROP PROCEDURE if exists update_vs_available;;
CREATE PROCEDURE update_vs_available(
in vs_addr char(255),
in avail int
)
do_update:begin
    declare selected_pool varchar(255);
    declare selected_type int;
    declare pool_avail    int;
    declare affected_pool int;
    declare is_stop       boolean default false;

    DECLARE pool_cur CURSOR FOR
    SELECT pool_name
    FROM pool_vs pv
    JOIN pool p on (pv.pool_name = p.name)
    WHERE vs_address = vs_addr AND p.type<>5;
    DECLARE CONTINUE HANDLER FOR NOT FOUND set is_stop = true;

    -- 查看vs的状态是否发生了变化，如果发生了变化，则更新pool，调用reload
    -- 如果没有发生变化，则退出存储过程
    SELECT NAME INTO affected_pool FROM vs
    WHERE address = vs_addr AND available != avail;
    if affected_pool is not null then
        UPDATE vs SET available = avail WHERE address =  vs_addr;
    else
        LEAVE do_update;
    end if;


    SELECT address_type INTO selected_type FROM vs WHERE address = vs_addr;

    set is_stop = false;
    open pool_cur;
    pool_loop: LOOP
        FETCH pool_cur INTO selected_pool;
        if is_stop then
          CLOSE pool_cur;
          LEAVE pool_loop;
        end if;

        SELECT COUNT(DISTINCT(pool_name)) INTO pool_avail
        FROM pool_vs pv
        JOIN vs ON (pv.vs_address = vs.address)
        WHERE pool_name = selected_pool AND vs.available = 1
        AND vs.in_use = 1 AND vs.address_type = selected_type;

        if selected_type = 1 then
            UPDATE pool SET available = pool_avail WHERE name =  selected_pool;
        elseif selected_type = 28 then
            UPDATE pool SET a6_available = pool_avail WHERE name =  selected_pool;
        end if;

    END LOOP pool_loop;


    call reload_data();
--  UPDATE frs_pool SET vs_available = avail WHERE value = vs_addr AND vs_available != avail;
--  call gen_frs_topo;
--  call gen_frs_wideip_pool;
end ;;


-- 增量更新frs_region_ip表
-- 每次调用存储过程add_region_ip做完正常处理后调用
DROP PROCEDURE if exists frs_region_ip_add;;
CREATE PROCEDURE frs_region_ip_add(
in reg varchar(255),
in ips int unsigned,
in ipe int unsigned,
in pri int unsigned
)
begin
    declare std_id      int unsigned;
    declare std_region  varchar(255);
    declare std_start   int unsigned;
    declare std_end     int unsigned;
    declare std_pri     int unsigned;
    declare is_stop     boolean default false;

    DECLARE cur CURSOR FOR
        SELECT id, region_name, ip_start, ip_end
        FROM frs_region_ip
        WHERE ip_start >= ips AND ip_end <= ipe
        AND priority = 2;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET is_stop = true;

    -- 覆盖优先级小于等于pri的区间
    SET std_id = null;
    SELECT id, region_name, ip_start, ip_end, priority
    INTO std_id, std_region, std_start, std_end, std_pri
    FROM frs_region_ip WHERE ip_start <= ips AND ip_end >= ipe
    AND priority <= pri;

    if std_id is not null then
    -- 新增区间:        --------------
    -- 原来区间:   -----------------------
        DELETE FROM frs_region_ip WHERE id = std_id;

        if std_start != ips then
            INSERT INTO frs_region_ip(region_name, ip_start, ip_end, priority)
            VALUES(std_region, std_start, ips - 1, std_pri);
        end if;

        if std_end != ipe then
            INSERT INTO frs_region_ip(region_name, ip_start, ip_end, priority)
            VALUES(std_region, ipe + 1, std_end, std_pri);
        end if;
    else
        -- 新增区间:         --------------------------
        -- 原来区间:        --------    -------    --------


        -- 1,    a,    --------   b,   --------   c,  --------
        --             ----              ----           ------
        DELETE FROM frs_region_ip where ip_start >= ips AND ip_end <= ipe;

        -- 2,               --------
        --             -------
        SET std_id = null;
        SELECT id, region_name, ip_start, ip_end
        INTO std_id, std_region, std_start, std_end
        FROM frs_region_ip
        WHERE ip_start < ips AND ip_end < ipe AND ip_end >= ips
        AND priority <= pri;

        if std_id is not null then
            UPDATE frs_region_ip SET ip_end = ips - 1 WHERE id = std_id;
        else
            -- 3,           --------
            --                   -------
            SET std_id = null;
            SELECT id, region_name, ip_start, ip_end
            INTO std_id, std_region, std_start, std_end
            FROM frs_region_ip
            WHERE ip_start > ips AND ip_end > ipe AND ip_start <= ipe
            AND priority <= pri;

            if std_id is not null then
                UPDATE frs_region_ip SET ip_start = ipe + 1 WHERE id = std_id;
            end if;
        end if;


    end if;

    INSERT INTO frs_region_ip(region_name, ip_start, ip_end, priority)
    VALUES(reg, ips, ipe, pri);


    -- custom类型的region不能覆盖cmos类型的region
    if pri = 1 then

        -- 1 :      ---------
        -- 2 :         ---------
        SET std_id = null;
        SELECT id, region_name, ip_start, ip_end, priority
        INTO std_id, std_region, std_start, std_end, std_pri
        FROM frs_region_ip
        WHERE ip_start > ips AND ip_end > ipe AND ip_start <= ipe
        AND priority = 2;

        if std_id is not null then
            UPDATE frs_region_ip SET ip_end = std_start - 1
            WHERE region_name = reg AND ip_start = ips AND ip_end = ipe;
        else
            -- 1 :        ---------
            -- 2 :   ---------
            SET std_id = null;
            SELECT id, region_name, ip_start, ip_end
            INTO std_id, std_region, std_start, std_end
            FROM frs_region_ip
            WHERE ip_start < ips AND ip_end < ipe AND ip_end >= ips
            AND priority = 2;

            if std_id is not null then
                UPDATE frs_region_ip SET ip_start = std_end + 1
                WHERE region_name = reg AND ip_start = ips AND ip_end = ipe;
            else
                -- 1 :        ------
                -- 2 :   -------------
                SET std_id = null;
                SELECT id, region_name, ip_start, ip_end
                INTO std_id, std_region, std_start, std_end
                FROM frs_region_ip
                WHERE ip_start <= ips AND ip_end >= ipe
                AND priority = 2;

                if std_id is not null then
                    DELETE FROM frs_region_ip
                   WHERE region_name = reg AND ip_start = ips AND ip_end = ipe;
                else

                    -- 1 :      ------------------
                    -- 2 :         -----   ----
                    SET std_id = null;

                    OPEN cur;
                    frs_loop: LOOP
                        FETCH cur INTO std_id, std_region, std_start, std_end;
                        if is_stop then
                            CLOSE cur;
                            LEAVE frs_loop;
                        end if;

                        DELETE FROM frs_region_ip WHERE id = std_id;

                        call frs_region_ip_add(std_region, std_start, std_end, 2);

                    END LOOP frs_loop;

                end if;
            end if;
        end if;
    end if;

end ;;

-- 每次有更新操作后的reload_data存储过程
-- 先获得锁（以2s的时间间隔轮询），再做reload操作
DROP PROCEDURE if exists reload_data;;
CREATE PROCEDURE reload_data()
begin
    declare is_free int default 0;

    frs_loop: LOOP
        SELECT GET_LOCK('dns_config_lock', 2) into is_free;
        if is_free = 1 then
            LEAVE frs_loop;
        end if;
    END LOOP frs_loop;

    call gen_frs_topo;
    call gen_frs_pool;
    call gen_frs_wideip_pool;

    update frs_serial_num set sn = sn + 1;

    SELECT RELEASE_LOCK('dns_config_lock');
end ;;

-- add_region_ip存储过程中添加增量增加region_ip功能
-- 每次做完正常的请求后，对frs_region_ip做一次增量更新
DROP PROCEDURE if exists add_region_ip;;
CREATE PROCEDURE add_region_ip(
in rgn varchar(255),
in ips int unsigned,
in ipe int unsigned,
in pri int unsigned
)
begin
  DECLARE ipp int unsigned;

  SET ipp = ips&4294901760;
  loop0: while ipp <= ipe do
      INSERT INTO region_ip(region_name, ip_start, ip_end, ip_prefix, region_priority)
      VALUE (rgn, ips, ipe, ipp, pri);
      SET ipp = ipp + 65536;
  end while loop0;

  call frs_region_ip_add(rgn, ips, ipe, pri);
end ;;

DELIMITER ;