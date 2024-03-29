'''
Created by 2014.05
Author junbao.kjb

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
            ip = '10.235.160.93'
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
            host_name = 'vkvm160093.sqa.cm6'
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
            ttl = 300
        if pool[i].has_key('QueryType'):
            if pool[i]['QueryType'] == 'A':
                type = 1
            elif pool[i]['QueryType'] == 'CName':
                type = 5
            elif pool[i]['QueryType'] == 'NS':
                type = 2
            elif pool[i]['QueryType'] == 'SRV':
                type = 33
            elif pool[i]['QueryType'] == 'AAAA':
                type = 28
            elif pool[i]['QueryType'] == 'SOA':
                type = 6
            elif pool[i]['QueryType'] == 'PTR':
                type = 12
        else:
            type = 1
        if pool[i].has_key('vs'):
            vs = pool[i]['vs']
        else:
            vs = []
        if pool[i].has_key('value'):
            value = pool[i]['value']
        else:
            value = 'null'
        pool_item = {'rr_ldns_limit': limit, 'in_use': in_use, 'available': available, 
                     'a6_available':a6_available, 'ttl':ttl, 'QueryType':type, 'vs': vs, 'value':value}
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
        if region[i].has_key('pri'):
            pri = region[i]['pri']
        else:
            pri = 1
        if region[i].has_key('complename'):
            complename = region[i]['complename']
        else:
            complename = ()
        if region[i].has_key('childregion'):
            childregion = region[i]['childregion']
        else:
            childregion = []
        region_item = {'range': rang, 'pool': pool, 'pri':pri, 'complename': complename, 'childregion': childregion}
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
    global vs_conf, pool_conf, region_conf, wideip_conf
    vs_conf      = {}
    pool_conf    = {}
    region_conf  = {}
    wideip_conf  = {}

    parse_vs(config)
    parse_pool(config)
    parse_region(config)
    parse_wideip(config)
    return True


# clean DB for pharos
def cleanDB():
    tables = ["pool","pool_region","pool_vs","region_ip","region_region","vs","wideip_pool","datacenter"]
    for item in tables:
        sql = 'delete from ' + item
        db.execute(DNS, sql)
    return True


# save vs conf to db
def write_vs2DB():
    for vs_name in vs_conf:
        vs = vs_conf[vs_name]
        sql = 'insert into vs (name,address,address_type,in_use,no_check,available,type,itvl,timeout,retries,port,host,uri) values \
               (\"' + vs['host_name'] + '\", \"' + vs['vs_ip'] + '\", ' + str(vs['address_type']) + ', ' + str(vs['in_use']) + ', ' + \
               str(vs['no_check']) + ', ' + str(vs['available']) + ', ' +  str(vs['HC_type']) + ', ' + str(vs['itvl'] ) + ', ' + str(vs['timeout']) + \
               ', ' + str(vs['retries']) + ', ' +  str(vs['vs_port']) + ', \"' + vs['host'] + '\", \"' + vs['url'] + '\")'
        db.execute(DNS, sql)


# sava pool conf to db
def write_pool2DB():
    for pool_name in pool_conf:
        pool = pool_conf[pool_name]
        sql = 'insert into pool (name,rr_ldns_limit,in_use,available,a6_available,ttl,type,value) values (\"' + \
               pool_name + '\", ' + str(pool['rr_ldns_limit']) + ', ' + str(pool['in_use']) + ', ' + str(pool['available']) + \
               ', ' + str(pool['a6_available']) + ', ' + str(pool['ttl']) + ', ' + str(pool['QueryType']) + ', \"' +pool['value'] + '\")'
        db.execute(DNS, sql) 
        for vs in pool['vs']:
            vs_name = vs[0]
            vs_ratio= vs[1]
            sql = 'insert into pool_vs (pool_name,vs_address,ratio) values (\"' + pool_name + '\", \"' + vs_conf[vs_name]['vs_ip'] + '\", ' + str(vs_ratio) + ')'
            db.execute(DNS, sql) 


# save region config to db
def write_region2DB():
    for region_name in region_conf:
        region = region_conf[region_name]
        # for comple_region
        if region_name[0] == '!':
            sql = 'insert into comple_region (original_name,comple_name) values (\"' + region['complename'][0] + '\", \"' + region['complename'][1] + '\")'
            db.execute(DNS, sql) 

        for pool in region['pool']:
            pool_name = pool[0]
            pool_ratio = pool[1]
            sql = 'insert into pool_region (region_name,pool_name,score) values (\"' + region_name + '\", \"' + pool_name + '\", ' + str(pool_ratio) + ')'
            db.execute(DNS, sql) 

        # insert region_region for common region
        sql = 'insert into region_region (big_region,small_region,relation) values (\"'+region_name+'\", \"' + region_name + '\", 0)'
        db.execute(DNS, sql) 

        # insert region_region for big region
        if len(region['childregion']) != 0:
            for i in range(0, len(region['childregion'])):
                sql = 'insert into region_region (big_region,small_region,relation) values (\"'+region_name+'\", \"' + region['childregion'][i] + '\", 0)'
                db.execute(DNS, sql)

        for rang in region['range']:
            packedIP = socket.inet_aton(rang[0])
            ipstart = struct.unpack("!L", packedIP)[0]
            packedIP  = socket.inet_aton(rang[1])
            ipstop  = struct.unpack("!L", packedIP)[0]
            db.callproc(DNS, 'add_region_ip', [region_name, ipstart, ipstop, region['pri']])


# save wideip conf to db
def write_wideip2DB():
    for wideip_name in wideip_conf:
        wideip = wideip_conf[wideip_name]
        for pool in wideip['pool']:
            sql = 'insert into wideip_pool (wideip_name,pool_name, in_use) values (\"' + wideip['url'] + '\", \"' + pool + '\", ' + str(wideip['in_use']) + ')'
            db.execute(DNS, sql) 


# save configuration to db
def write2DB():
    write_vs2DB()
    write_pool2DB()
    write_region2DB()
    write_wideip2DB()
    return True


# copy file to pharos machine, initial DB, 
def initPharos():
    #logger.debug("#Deploy# copy %s to pharos %s...", DNS['Pharos_org'], DNS['DNS_HOST'])
    system_util.copy_file_2_server(DNS['DNS_HOST'], DNS['Pharos_org'], DNS['pharos_dst'])
    #logger.debug("#Deploy# copy %s to pharos %s...", DNS['dbinit_org'], DNS['DNS_HOST'])
    system_util.copy_file_2_server(DNS['DNS_HOST'], DNS['dbinit_org'], DNS['dbinit_dst'])
    #logger.debug("#Deploy# copy %s to pharos %s...", DNS['create_org'], DNS['DNS_HOST'])
    system_util.copy_file_2_server(DNS['DNS_HOST'], DNS['create_org'], DNS['create_dst'])
    #logger.debug("#Deploy# copy %s to pharos %s...", DNS['stored_org'], DNS['DNS_HOST'])
    system_util.copy_file_2_server(DNS['DNS_HOST'], DNS['stored_org'], DNS['stored_dst'])
    #logger.debug("#Deploy# copy %s to pharos %s...", DNS['proced_org'], DNS['DNS_HOST'])
    system_util.copy_file_2_server(DNS['DNS_HOST'], DNS['proced_org'], DNS['proced_dst'])

    #logger.debug("#Deploy# intial Databases...")
    db.execute(DNS, 'drop database dns_config;drop database dns_config2;drop database dns_config3;') 
    cmd = '/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/dns.sql'
    system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], cmd)
    system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], '/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/create_table.sql')
    system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], '/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/ph_stored_routines.sql')
    return True

def stopPharos():
    cmd = 'killall -9 pharos'
    system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], cmd)
    return True
 
def startPharos():
    cmd = '/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/callProcedure.sql '
    system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], cmd)

    cmd = '/home/admin/pharos/bin/pharos -c /home/admin/pharos/conf/pharos.conf '
    thread.start_new_thread(system_util.exe_cmd_via_ssh, (DNS['DNS_HOST'], cmd))
    return True


def restartPharos():
    stopPharos()
    startPharos()
def copyfile(src, dst):
    system_util.copy_file_2_server(DNS['DNS_HOST'], src, dst)
def exe_cmd(cmd):
    system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], cmd)

# 
# config = {'vs': {'vs_ip':1.1.1.1, 'address_type': 0, 'vs_port':53, 'host_name': 'cm6', 'in_use': 1, 'no_check': 1, 'available':1, 
#                  'HC_type':0, 'itvl':30, 'timeout':30, 'retries':3, 'host': 'cm6', 'url':'index'},
#           'pool': {'rr_ldns_limit':1, 'in_use': 1, 'available': 1, 'a6_available': 0, 'ttl':300, 'QueryType': 'A', 'vs':[]}, 
#           'region': {'range': [], 'pool':[]}, 
#           'wideip': {'url':'img01.taobaocdn.com.danuoyi.tbcache.com', 'pool': [], 'in_use': []}}
def deploy(config):
    logger.debug("# Test # Start to deploy...")

    if stopPharos() != True:
        return False
    logger.debug("#Deploy# Stop Pharos2 befor test Successful!")

    if cleanDB() != True:
        return False
    logger.debug("#Deploy# Clean DB Successful!")

    if parse(config) != True:
        return False

    # copy config file, initial db 
    if initPharos() != True:
        return False
    logger.debug('#Deploy# Copy config file to: ' + DNS['DNS_HOST'] + ', adn initial DB Successful')

    if write2DB() != True:
        return False
    logger.debug('#Deploy# Save Test config to :' + DNS['DNS_HOST'] + ' Successful!')

    if startPharos() != True:
        return False
    logger.debug("#Deploy# Start to run Pharos2...")

    logger.debug("#Deploy# wait 5 seconds to stable pharos...")
    time.sleep(5)

    return True


def checkDBRunning(ips):
    cmd = '/sbin/service mysqld status'
    for ip in ips:
        resp = system_util.exe_cmd_via_ssh(ip, cmd)
        if resp[0].find('running') == -1:
            return False
    return True

def installPharos():
    cmd = 'yum install t-pharos2 -b test -y'
    system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], cmd)


# do some prepare work before test
def setup():
    if DNS['Has_Setup'] == True:
        return True
    logger.debug("Test setup (check DB running, install pharos)")
    checkDBRunning([DNS['DNS_HOST']])
    installPharos()
    DNS['Has_Setup'] = True
    return True

def setDNS(dns_conf):
    if dns_conf.has_key('DNS_HOST'):
        DNS['DNS_HOST'] = dns_conf['DNS_HOST']

    if dns_conf.has_key('DB_HOST'):
        DNS['DB_HOST'] = dns_conf['DB_HOST']



