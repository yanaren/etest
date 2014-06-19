'''
Created by 2014.05
Author junbao.kjb

Function:
1. startPharos()
2. stopPharos()
3. installPharos()
4. unstallPharos()
5. deploy()  // save to db
'''
import thread, socket, struct, time
import src.util.system_util as system_util
import src.util.db          as db
from   src.util.logger      import logger
from   src.deploy           import DNS, TCHECK, VS


vs_conf      = {}
pool_conf    = {}
region_conf  = {}
wideip_conf  = {}
tcheck_master= {}
tcheck_slave = {}
rs_list      = []

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
            ip = '10.235.160.53'
        if vs[i].has_key('address_type'):
            address_type = vs[i]['address_type']
        else:
            address_type = 1
        if vs[i].has_key('vs_port'):
            port = vs[i]['vs_port']
        else:
            port = 80
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
            itvl = 60
        if vs[i].has_key('timeout'):
            timeout = vs[i]['timeout']
        else:
            timeout = 60
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
            url = '/status'
        vs_item = {'vs_ip': ip, 'address_type': address_type, 'vs_port': port, 'host_name': host_name,
                   'in_use': in_use, 'no_check': no_check, 'available': available, 'HC_type': HC_type, 
                   'itvl':itvl, 'timeout':timeout, 'retries': retries, 'host': host, 'url':url}
        vs_conf[name] = vs_item


# parse pool config
def parse_pool(config): 
    global pool_conf
    pool = config['pool']
    pool_num = len(pool)
    for i in pool:
        name = i
        if pool[i].has_key('rr_ldns_limit'):
            limit = pool[i]['rr_ldns_limit']
        else:
            limit = 1
        if pool[i].has_key('in_use'):
            in_use = pool[i]['in_use']
        else:
            in_use = 1
        if pool[i].has_key('available'):
            available = pool[i]['available']
        else:
            available = 1
        if pool[i].has_key('a6_available'):
            a6_available = pool[i]['a6_available']
        else:
            a6_available = 0
        if pool[i].has_key('ttl'):
            ttl = pool[i]['ttl']
        else:
            ttl = 1
        if pool[i].has_key('QueryType'):
            if pool[i]['QueryType'] == 'A':
                type = 1
        else:
            type = 1
        if pool[i].has_key('vs'):
            vs = pool[i]['vs']
        else:
            vs = []
        pool_item = {'rr_ldns_limit': limit, 'in_use': in_use, 'available': available, 
                     'a6_available':a6_available, 'ttl':ttl, 'QueryType':type, 'vs': vs}
        pool_conf[name] = pool_item

# parse region config
def parse_region(config):
    global region_conf
    region = config['region']
    region_num = len(region)
    for i in region:
        name = i
        if region[i].has_key('range'):
            rang = region[i]['range']
        else:
            rang = []
        if region[i].has_key('pool'):
            pool = region[i]['pool']
        else:
            pool = []
        region_item = {'range': rang, 'pool': pool}
        region_conf[name] = region_item

# parse wideip config
def parse_wideip(config):
    global wideip_conf
    wideip = config['wideip']
    wideip_num = len(wideip)
    for i in wideip:
        name = i
        if wideip[i].has_key('url'):
            url = wideip[i]['url']
        else:
            url = 'img01.taobaocdn.com.danuoyi.tbcache.com'
        if wideip[i].has_key('pool'):
            pool = wideip[i]['pool']
        else:
            pool = []
        if wideip[i].has_key('in_use'):
            in_use = wideip[i]['in_use']
        else:
            in_use = 1
        wideip_item = {'url': url, 'pool': pool, 'in_use': in_use}
        wideip_conf[name] = wideip_item


# parse configuration for DB setting
def parse(config):
    parse_vs(config)
    parse_pool(config)
    parse_region(config)
    parse_wideip(config)
    return 'True'


# clean DB for pharos
def cleanDB():
    tables = ["pool","pool_region","pool_vs","region_ip","region_region","vs","wideip_pool","datacenter"]
    for item in tables:
        sql = 'delete from ' + item
        db.execute(sql)
    return 'True'


# save vs conf to db
def write_vs2DB():
    for vs_name in vs_conf:
        vs = vs_conf[vs_name]
        sql = 'insert into vs (name,address,address_type,in_use,no_check,available,type,itvl,timeout,retries,port,host,uri) values \
               (\"' + vs['host_name'] + '\", \"' + vs['vs_ip'] + '\", ' + str(vs['address_type']) + ', ' + str(vs['in_use']) + ', ' + \
               str(vs['no_check']) + ', ' + str(vs['available']) + ', ' +  str(vs['HC_type']) + ', ' + str(vs['itvl'] ) + ', ' + str(vs['timeout']) + \
               ', ' + str(vs['retries']) + ', ' +  str(vs['vs_port']) + ', \"' + vs['host'] + '\", \"' + vs['url'] + '\")'
        db.execute(sql)


# sava pool conf to db
def write_pool2DB():
    for pool_name in pool_conf:
        pool = pool_conf[pool_name]
        sql = 'insert into pool (name,rr_ldns_limit,in_use,available,a6_available,ttl,type,value) values (\"' + \
               pool_name + '\", ' + str(pool['rr_ldns_limit']) + ', ' + str(pool['in_use']) + ', ' + str(pool['available']) + \
               ', ' + str(pool['a6_available']) + ', ' + str(pool['ttl']) + ', ' + str(pool['QueryType']) + ', \"null\")'
        db.execute(sql) 
        for vs in pool['vs']:
            vs_name = vs[0]
            vs_ratio= vs[1]
            sql = 'insert into pool_vs (pool_name,vs_address,ratio) values (\"' + pool_name + '\", \"' + vs_conf[vs_name]['vs_ip'] + '\", ' + str(vs_ratio) + ')'
            db.execute(sql) 


# save region config to db
def write_region2DB():
    for region_name in region_conf:
        region = region_conf[region_name]
        for pool in region['pool']:
            pool_name = pool[0]
            pool_ratio = pool[1]
            sql = 'insert into pool_region (region_name,pool_name,score) values (\"' + region_name + '\", \"' + pool_name + '\", ' + str(pool_ratio) + ')'
            db.execute(sql) 

        sql = 'insert into region_region (big_region,small_region,relation) values (\"' + region_name + '\", \"' + region_name + '\", 0)'
        db.execute(sql) 
        for rang in region['range']:
            packedIP = socket.inet_aton(rang[0])
            ipstart = struct.unpack("!L", packedIP)[0]
            packedIP  = socket.inet_aton(rang[1])
            ipstop  = struct.unpack("!L", packedIP)[0]
            db.callproc('add_region_ip', [region_name, ipstart, ipstop, 1])


# save wideip conf to db
def write_wideip2DB():
    for wideip_name in wideip_conf:
        wideip = wideip_conf[wideip_name]
        for pool in wideip['pool']:
            sql = 'insert into wideip_pool (wideip_name,pool_name, in_use) values (\"' + wideip['url'] + '\", \"' + pool + '\", ' + str(wideip['in_use']) + ')'
            db.execute(sql) 


# save configuration to db
def write2DB():
    write_vs2DB()
    write_pool2DB()
    write_region2DB()
    write_wideip2DB()
    return 'True'


# copy file to pharos machine, initial DB, 
def initPharos():
    logger.debug("# Deploy # copy %s to pharos %s...", DNS['Pharos_org'], DNS['DNS_HOST'])
    system_util.copy_file_2_server(DNS['DNS_HOST'], DNS['Pharos_org'], DNS['pharos_dst'])
    logger.debug("# Deploy # copy %s to pharos %s...", DNS['dbinit_org'], DNS['DNS_HOST'])
    system_util.copy_file_2_server(DNS['DNS_HOST'], DNS['dbinit_org'], DNS['dbinit_dst'])
    logger.debug("# Deploy # copy %s to pharos %s...", DNS['create_org'], DNS['DNS_HOST'])
    system_util.copy_file_2_server(DNS['DNS_HOST'], DNS['create_org'], DNS['create_dst'])
    logger.debug("# Deploy # copy %s to pharos %s...", DNS['stored_org'], DNS['DNS_HOST'])
    system_util.copy_file_2_server(DNS['DNS_HOST'], DNS['stored_org'], DNS['stored_dst'])
    logger.debug("# Deploy # copy %s to pharos %s...", DNS['proced_org'], DNS['DNS_HOST'])
    system_util.copy_file_2_server(DNS['DNS_HOST'], DNS['proced_org'], DNS['proced_dst'])

    logger.debug("# Deploy # intial Databases...")
    db.execute('drop database dns_config;drop database dns_config2;drop database dns_config3;') 
    cmd = '/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/dns.sql'
    system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], cmd)
    system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], '/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/create_table.sql')
    system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], '/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/ph_stored_routines.sql')
    return 'True'

def stopPharos():
    cmd = 'killall -9 pharos'
    system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], cmd)
    return 'True'
 
def startPharos():
    cmd = '/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/callProcedure.sql '
    system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], cmd)

    cmd = '/home/admin/pharos/bin/pharos -c /home/admin/pharos/conf/pharos.conf '
    thread.start_new_thread(system_util.exe_cmd_via_ssh, (DNS['DNS_HOST'], cmd))
    return 'True'


# deploy test environment, 
def deploy(config):
    logger.debug("# Test # start to do the env deploy...")

    logger.debug("# Deploy # stopPharos...")
    if stopPharos() != 'True':
        return 'False'

    logger.debug("# Deploy # cleanDB...")
    if cleanDB() != 'True':
        return 'False'

    if parse(config) != 'True':
        return 'False'

    # copy config file, initial db 
    logger.debug("# Deploy # copy file, initail db...")
    if initPharos() != 'True':
        return 'False'

    logger.debug("# Deploy # save config db...")
    if write2DB() != 'True':
        return 'False'

    logger.debug("# Deploy # start pharos...")
    if startPharos() != 'True':
        return 'False'

    return 'True'


def checkDBRunning(ips):
    cmd = '/sbin/service mysqld status'
    for ip in ips:
        resp = system_util.exe_cmd_via_ssh(ip, cmd)
        if resp[0].find('running') == -1:
            return 'False'
    return 'True'

def installPharos():
    cmd = 'yum install t-pharos2 -b test -y'
    system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], cmd)


# do some prepare work before test
def setup():
    if DNS['Has_Setup'] == 'True':
        return 'True'
    logger.debug("Test setup (check DB running, install pharos)")
    checkDBRunning([DNS['DNS_HOST']])
    installPharos()
    DNS['Has_Setup'] = 'True'
    return 'True'

def setDNS(dns_conf):
    if dns_conf.has_key('DNS_HOST'):
        DNS['DNS_HOST'] = dns_conf['DNS_HOST']

    if dns_conf.has_key('DB_HOST'):
        DNS['DB_HOST'] = dns_conf['DB_HOST']



