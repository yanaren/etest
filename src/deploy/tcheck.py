'''
Created by 2014.06
Author junbao.kjb
Function:
'''
import thread, socket, struct, time
import src.util.system_util as system_util
import src.util.db          as db
from src.util.logger        import logger
from src.deploy             import ENV, CONFIG, TCHECK, VS, DB

vs_conf      = {}
tcheck_master= {}
tcheck_slave = {}

# parse config for virtual server
def parse_vs(config):
    global vs_conf
    vs = config['vs']
    vs_num = len(vs)
    for i in vs:
        name = i
        if vs[i].has_key('vs_ip'):
            ip = vs[i]['vs_ip']
        else:
            raise 
        if vs[i].has_key('address_type'):
            address_type = vs[i]['address_type']
        else:
            address_type = 1
        if vs[i].has_key('vs_port'):
            port = vs[i]['vs_port']
        else:
            port = 8008
        if vs[i].has_key('host_name'):
            host_name = vs[i]['host_name']
        else:
            host_name = 'vkvm160053.sqa.cm6'
        if vs[i].has_key('in_use'):
            in_use = vs[i]['in_use']
        else:
            in_use = 1
        if vs[i].has_key('no_check'):
            no_check = vs[i]['no_check']
        else:
            no_check = 0
        if vs[i].has_key('available'):
            available = vs[i]['available']
        else:
            available = 1
        if vs[i].has_key('HC_type'):
            HC_type = vs[i]['HC_type']
        else:
            HC_type = 0
        if vs[i].has_key('itvl'):
            itvl = vs[i]['itvl']
        else:
            itvl = 30
        if vs[i].has_key('timeout'):
            timeout = vs[i]['timeout']
        else:
            timeout = 5
        if vs[i].has_key('retries'):
            retries = vs[i]['retries']
        else:
            retries = 3
        if vs[i].has_key('host'):
            host = vs[i]['host']
        else:
            host = host_name
        if vs[i].has_key('url'):
            url = vs[i]['url']
        else:
            url = '/index.html'
        vs_item = {'vs_ip': ip, 'address_type': address_type, 'vs_port': port, 'host_name': host_name,
                   'in_use': in_use, 'no_check': no_check, 'available': available, 'HC_type': HC_type, 
                   'itvl':itvl, 'timeout':timeout, 'retries': retries, 'host': host, 'url':url}
        vs_conf[name] = vs_item
    return True


# parse tcheck config, conf must contains 'master', 'slave'
def parse_tcheck(conf):
    global tcheck_master, tcheck_slave
    tcheck_master = TCHECK[conf['tcheck']['master']]

    for tc in conf['tcheck']['slave']:
        tcheck_slave[tc] = TCHECK[tc]
    return True

# parse vs & tcheck info
def parse(conf):
    parse_vs(conf)
    parse_tcheck(conf)
    return True


# clean DB for tcheck
def cleanDB():
    DB=tcheck_master
    tables = ["vs"]
    for item in tables:
        sql = 'drop table IF EXISTS ' + item
        db.execute(DB, sql)
    return True

# initial DB for tcheck
def initialDB():
    DB=tcheck_master
    srcfile = '~/project/etest/config/pharos/update_vs.sql'
    dstfile = '/home/admin/pharos/conf/update_vs.sql'
    ip = DB['DB_HOST']
    system_util.copy_file_2_server(ip, srcfile, dstfile)
    cmd = 'mysql -u'+DB['DB_USER'] + ' -p' + DB['DB_PASS'] + ' < ' + dstfile
    system_util.exe_cmd_via_ssh(ip, cmd)

    sql ='CREATE TABLE vs (\
          name varchar(255) NOT NULL,\
          address varchar(255) NOT NULL,\
          address_type int(11) NULL DEFAULT 1,\
          in_use int(11) NOT NULL DEFAULT 1,\
          available int(11) NOT NULL DEFAULT 1,\
          type int(11) NOT NULL DEFAULT 0,\
          itvl int(11) NOT NULL DEFAULT 10,\
          timeout int(11) NOT NULL DEFAULT 5,\
          retries int(11) NOT NULL DEFAULT 3,\
          port int(11) NOT NULL DEFAULT 80,\
          host varchar(1024) NOT NULL DEFAULT \'\',\
          uri varchar(1024) NOT NULL DEFAULT \'\',\
          no_check int(11) NOT NULL DEFAULT 0,\
          PRIMARY KEY  (name),\
          UNIQUE KEY (address)\
          ) ENGINE=InnoDB DEFAULT CHARSET=gbk;'
    db.execute(DB, sql)
    return True

# save vs conf to db
def write_vs2DB():
    for vs_name in vs_conf:
        vs = vs_conf[vs_name]
        sql = 'insert into vs (name,address,address_type,in_use,no_check,available,\
               type,itvl,timeout,retries,port,host,uri) values (\"' + vs['host_name'] \
               + '\", \"' + vs['vs_ip'] + '\", ' + str(vs['address_type']) + ', ' \
               + str(vs['in_use']) + ', ' + str(vs['no_check']) + ', ' + str(vs['available']) \
               + ', ' +  str(vs['HC_type']) + ', ' + str(vs['itvl'] ) + ', ' + str(vs['timeout']) \
               + ', ' + str(vs['retries']) + ', ' +  str(vs['vs_port']) + ', \"' + vs['host'] \
               + '\", \"' + vs['url'] + '\")'
        db.execute(tcheck_master, sql)
    return True

# restart all vs
def restart_all_vs():
    ips_vs = []
    for vs in vs_conf:
        ips_vs.append(vs_conf[vs]['vs_ip'])
    stop_nginx(ips_vs)
    start_nginx(ips_vs)

# start vs(nginx), input: ['vs1', 'vs2']
def start_vs(vss):
    for vs in vss:
        ip = vs_conf[vs]['vs_ip']
        if vs_conf[vs]['HC_type'] == 0: 
            logger.debug("# Test # started vs(tcp check): "+ip)
        elif vs_conf[vs]['HC_type'] == 1:
            logger.debug("# Test # started vs(http check): "+ip)
        start_nginx([ip])

def start_nginx(ips):
    srcfile = '~/project/etest/config/pharos/nginx.conf'
    dstfile = '/usr/local/nginx/conf/nginx.conf'
    cmd = '/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf'
    nginx_run = 'ps -ef |grep nginx | wc -l'
    for ip in ips:
        system_util.copy_file_2_server(ip, srcfile, dstfile)
        system_util.exe_cmd_via_ssh(ip, cmd)
        assert ( system_util.exe_cmd_via_ssh(ip, nginx_run))

# stop vs(nginx), input: ['vs1', 'vs2']
def stop_vs(vss):
    for vs in vss:
        ip = vs_conf[vs]['vs_ip']
        if vs_conf[vs]['HC_type'] == 0:
            logger.debug("# Test # stopped vs(tcp check): "+ip)
        elif vs_conf[vs]['HC_type'] == 1:
            logger.debug("# Test # stopped vs(http check): "+ip)
        stop_nginx([ip])
def stop_nginx(ips):
    cmd = 'killall -9 /usr/local/nginx/sbin/nginx'
    nginx_run = 'ps -ef |grep /usr/local/nginx/sbin/nginx | wc -l'
    for ip in ips:
        system_util.exe_cmd_via_ssh(ip, cmd)
        system_util.exe_cmd_via_ssh(ip, nginx_run)


# virturl ip addr for linux
#def start_ipaddr(ips):
#    for ip in ips:
#        cmd = 'ip addr del '+ ip[1] + ' dev eth0:1'
#        system_util.exe_cmd_via_ssh(ip[0], cmd)
#def stop_ipaddr(ips):
#    for ip in ips:
#        cmd = 'ifconfig eth0:1 ' + ip[1] +' netmask 255.255.255.0'
#        system_util.exe_cmd_via_ssh(ip[0], cmd)

# start all tcheck use in one case
def start_all_tcheck():
    checkers=[]
    checkers.append('master')
    for slave in tcheck_slave:
        checkers.append(slave)
    start_tcheck(checkers)

# start tchecks in: ['master', 'slave1', 'slave2']
def start_tcheck(checkers):
    cmd     = '/home/admin/pharos/bin/tcheck -f /home/admin/pharos/conf/tcheck.conf'
    dstfile = '/home/admin/pharos/conf/tcheck.conf'
    tc_run  = 'ps -ef |grep tcheck | grep \'/home/admin/pharos/\' | awk \'{print $2}\''
    for item in checkers:
        if item == 'master':
            ip      = tcheck_master['TC_HOST']
            srcfile = '~/project/etest/config/pharos/tcheck_master_'+ str(len(tcheck_slave)) + '.conf'
            continue
        else:
            ip = tcheck_slave[item]['TC_HOST']
            srcfile = '~/project/etest/config/pharos/tcheck_slave.conf'
        logger.debug('#Deploy#  Copy ' + srcfile[30:-1] + ' to ' + ip)
        system_util.copy_file_2_server(ip, srcfile, dstfile)
        logger.debug('#Deploy#  Start tcheck at: ' + ip)
        system_util.exe_cmd_via_ssh(ip, cmd)
        output = system_util.exe_cmd_via_ssh(ip, tc_run)
        assert (output[0].find('/home/admin/pharos/bin/tcheck') != -1)

#stop all tcheck in one case
def stop_all_tcheck():
    checkers=[]
    checkers.append('master')
    for slave in tcheck_slave:
        checkers.append(slave)
    stop_tcheck(checkers)
    return True

# stop tchecks in: ['master', 'slave1', 'slave2']
def stop_tcheck(checkers):
    cmd = 'killall -9 tcheck'
    tc_run = 'ps -ef |grep tcheck | grep \'/home/admin/pharos/\' | awk \'{print $2}\''
    for item in checkers:
        if item == 'master':
            ip = tcheck_master['TC_HOST']
            continue
        else:
            ip = tcheck_slave[item]['TC_HOST']
        system_util.exe_cmd_via_ssh(ip, cmd)
        output = system_util.exe_cmd_via_ssh(ip, tc_run)
        assert (output[0].find('/home/admin/pharos/bin/tcheck') == -1)

# deploy the test 
def deploy(config):
    logger.debug("# Test # Start to do the deploy...")
    if parse(config) != True:
        return False
    logger.debug("#Deploy# Stop all tcheck...")
    if stop_all_tcheck() != True:
        return False
    logger.debug("#Deploy# Restart all vs...")
    restart_all_vs()
    logger.debug("#Deploy# Clean all DB vs data...")
    if cleanDB() != True:
        return False
    logger.debug("#Deploy# Initial DB vs table...")
    if initialDB() != True:
        return False
    logger.debug("#Deploy# Save vs config to db...")
    if write_vs2DB() != True:
        return False
    logger.debug("#Deploy# Start all tcheck...")
    if start_all_tcheck() != True:
        return False
    return True


def check_DB_running(ips):
    cmd = '/sbin/service mysqld status'
    for ip in ips:
        resp = system_util.exe_cmd_via_ssh(ip, cmd)
        if resp[0].find('running') == -1:
            return False
    return True
def check_tcheck_install(ips):
    cmd = 'file /home/admin/pharos/bin/tcheck'
    for ip in ips:
        resp = system_util.exe_cmd_via_ssh(ip, cmd)
        if resp[0].find('ERROR') != -1:
            return False
    return True

# do some prepare work before test
def start_check():
    logger.debug("Test setup (check DB running, install tcheck)")
    if ENV['Has_Setup'] == 'True':
        return 'True'
    tcheck_master = CONFIG['tcheck']['master']
    tcheck_slave  = {}
    for check in CONFIG['tcheck']:
        if check != 'master':
            tcheck_slave[check] = CONFIG['tcheck'][check]

    ips=[]
    ips.append(tcheck_master['DB_HOST'])
    for slave in tcheck_slave:
        ips.append(tcheck_slave[slave]['DB_HOST'])
    assert check_DB_running(ips)
    assert check_tcheck_install(ips)
    ENV['Has_Setup'] = 'True'
    tcheck_master={}
    tcheck_slave ={}
    return True
   

# condition time check
def check_db(vs_in, max_time = 30):
    logger.debug('# test # check result: '+str(vs_in))
    sleep_time = 0
    sleep_time_span = 3
    while sleep_time < max_time:
        if check_vs(vs_in):
            info = '# test # check result: ' + str(vs_in) + ' is Expected!' 
            logger.debug(info)
            return True
        else:
            sleep_time += sleep_time_span
            time.sleep(sleep_time_span)
    assert False

# vs status check, input: [('vs1', 1), ('vs2', 0)]
def check_vs(vs_in):
    isexpected = True
    for vs in vs_in:
        sql = 'select available from vs where address = \'%s\' ' % (vs_conf[vs[0]]['vs_ip'])
        result = db.execute(tcheck_master, sql)
        if result[0][0] != vs[1]:
            isexpected = False
    for slave in tcheck_slave:
        DB = tcheck_slave[slave]
        for vs in vs_in:
            sql = 'select available from vs where address = \'%s\' ' % (vs_conf[vs[0]]['vs_ip'])
            result = db.execute(DB, sql)
            if result[0][0] != vs[1]:
                isexpected = False
    return isexpected


# sleep func for tcheck
def sleep(sec):
    info = '# test # Wait for ' + str(sec) + ' seconds...'
    logger.debug(info)
    time.sleep(sec)



