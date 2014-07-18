from   src.util.logger      import logger
import src.protocol.dns.dns as DNS
import src.deploy.pharos    as pharos
import src.util.system_util as system_util
import pytest, time
conf = {}
ip1  = '10.235.160.73'
ip2  = '10.235.160.83'
ip3  = '10.235.160.93'
laddr= '10.235.160.53'
dns  = {'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}] }
elog = '# Test # Test finished and result check successful...\n'
dnsip= '10.101.81.12'

def setup_module(module):
    print ("setup_module:%s" % module.__name__)
def teardown_module(module):
    print ("teardown_module:%s" % module.__name__)
def setup_function(function):
    print ("setup_function:%s" % function.__name__)
    global conf
    conf= {
          'vs'    :{'vs1':{'vs_ip':ip1,'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6', 'url':'/status'}},
          'pool'  :{'WT_BJ_Pool': {'ttl':300, 'vs': [('vs1', 1)]}},
          'region':{'WT_BJ_Region': {'range':[(laddr, laddr)],'pool': [('WT_BJ_Pool', 100)]}},
          'wideip':{'wideip1': {'url':'img01.taobaocdn.com.danuoyi.tbcache.com', 'pool': ['WT_BJ_Pool']}}
    }
def teardown_function(function):
    pass


def test_Pharos_AccessLog_Absolute_Path_201():
    pharos.deploy(conf)
    pharos.copyfile('config/pharos/pharos_access_absolute.conf', '/home/admin/pharos/conf/pharos.conf')
    pharos.stopPharos()
    system_util.exe_cmd_via_ssh(dnsip,'rm -rf /home/admin/pharos/logs/access.log')
    pharos.startPharos()
    time.sleep(2)
    output = system_util.exe_cmd_via_ssh(dnsip,'ls -h /home/admin/pharos/logs/access.log')
    assert (output == ['/home/admin/pharos/logs/access.log'])
    logger.debug(elog)

def test_Pharos_AccessLog_Cronolog_Path_202():
    pharos.copyfile('config/pharos/pharos_access_cronolog.conf', '/home/admin/pharos/conf/pharos.conf')
    pharos.stopPharos()
    system_util.exe_cmd_via_ssh(dnsip,'rm -rf /home/admin/pharos/logs/access*')
    pharos.startPharos()
    time.sleep(5)

    output1 = system_util.exe_cmd_via_ssh(dnsip,'ls -h /home/admin/pharos/logs/access* | wc -l')
    dns   = { 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = { 'ancount': 1, 'an_rdata': [(ip1, 1)], 'total_rdata': 10}
    for i in range(0, 5):
        DNS.do_dns(dns, check, 10)
        time.sleep(1)
    output2 = system_util.exe_cmd_via_ssh(dnsip,'ls -h /home/admin/pharos/logs/access* | wc -l')
    assert (int(output1[0]) + 5 == int(output2[0])) or (int(output1[0]) + 6 == int(output2[0]))
    logger.debug(elog)

def test_Pharos_AccessLog_Sys_203():
    pharos.copyfile('config/pharos/pharos_access_syslog.conf', '/home/admin/pharos/conf/pharos.conf')
    pharos.restartPharos()
    output = system_util.exe_cmd_via_ssh(dnsip,'sudo tail messages -n 20 | grep "/home/admin/pharos/bin/pharos -c /home/admin/pharos/conf/pharos.conf"| wc -l')
    assert output != ['0']
    logger.debug(elog)

def test_Pharos_ErrorLog_Absolute_Path_204():
    pharos.copyfile('config/pharos/pharos_error_absolute.conf', '/home/admin/pharos/conf/pharos.conf')
    pharos.stopPharos()
    system_util.exe_cmd_via_ssh(dnsip,'rm -rf /home/admin/pharos/logs/error*')
    pharos.startPharos()
    time.sleep(2)
    output = system_util.exe_cmd_via_ssh(dnsip,'ls -h /home/admin/pharos/logs/error.log')
    assert (output == ['/home/admin/pharos/logs/error.log'])
    logger.debug(elog)

def test_Pharos_ErrorLog_Cronolog_Path_205():
    pharos.copyfile('config/pharos/pharos_error_cronolog.conf', '/home/admin/pharos/conf/pharos.conf')
    pharos.stopPharos()
    system_util.exe_cmd_via_ssh(dnsip,'rm -rf /home/admin/pharos/logs/error*')
    pharos.startPharos()
    time.sleep(5)
    
    output1 = system_util.exe_cmd_via_ssh(dnsip,'ls -h /home/admin/pharos/logs/error* | wc -l')
    dns   = { 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = { 'ancount': 1, 'an_rdata': [(ip1, 1)], 'total_rdata': 10}
    for i in range(0, 5):
        DNS.do_dns(dns, check, 10)
        time.sleep(1)
    output2 = system_util.exe_cmd_via_ssh(dnsip,'ls -h /home/admin/pharos/logs/error* | wc -l')
    assert (int(output1[0]) + 5 == int(output2[0])) or (int(output1[0]) + 6 == int(output2[0]))
    logger.debug(elog)

def test_Pharos_ErrorLog_Sys_206():
    pharos.copyfile('config/pharos/pharos_error_syslog.conf', '/home/admin/pharos/conf/pharos.conf')
    pharos.restartPharos()
    output = system_util.exe_cmd_via_ssh(dnsip,'sudo tail messages -n 20 | grep "/home/admin/pharos/bin/pharos -c /home/admin/pharos/conf/pharos.conf"| wc -l')
    assert output != ['0']
    logger.debug(elog)


def test_Pharos_Start_Stop_207():
    for i in range(50):
        pharos.restartPharos()
    dns   = { 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = { 'ancount': 1, 'an_rdata': [(ip1, 1)], 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_Pharos_Reload_208():
    pharos.deploy(conf)
    dns   = { 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = { 'ancount': 1, 'an_rdata': [(ip1, 1)], 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

    pharos.cleanDB()
    pharos.initPharos()
    conf['wideip']= {'wideip1': {'url':'img02.taobaocdn.com.danuoyi.tbcache.com', 'pool': ['WT_BJ_Pool']}}
    cmd = 'ls -lt /home/admin/pharos/logs/error*.log --time-style=full-iso | sed -n "1p" | awk "{print $7}"'
    pharos.parse(conf)
    pharos.write2DB()
    output1 = system_util.exe_cmd_via_ssh(dnsip, cmd)
    system_util.exe_cmd_via_ssh(dnsip, '/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/callProcedure.sql')
    output2 = system_util.exe_cmd_via_ssh(dnsip,'/home/admin/pharos/bin/ctrl-pharos reload')
    time.sleep(2)
    output3 = system_util.exe_cmd_via_ssh(dnsip, cmd)
    assert output1 == output3

    dns   = { 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = { 'rcode': 3 }
    DNS.do_dns(dns, check, 10)
    dns   = { 'qd':[{'qd_qname':'img02.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = { 'ancount': 1, 'an_rdata': [(ip1, 1)], 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_Pharos_Port_Set_53_209():
    pharos.deploy(conf)
    pharos.copyfile('config/pharos/pharos_port52.conf', '/home/admin/pharos/conf/pharos.conf')
    pharos.restartPharos()
    time.sleep(5)
    dns   = { 'DNS_PORT':52, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = { 'ancount': 1, 'an_rdata': [(ip1, 1)], 'total_rdata': 10 }
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_Pharos_Port_Set_65535_210():
    pharos.deploy(conf)
    pharos.copyfile('config/pharos/pharos_port65535.conf', '/home/admin/pharos/conf/pharos.conf')
    pharos.restartPharos()
    time.sleep(5)
    dns   = { 'DNS_PORT':65535, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = { 'ancount': 1, 'an_rdata': [(ip1, 1)], 'total_rdata': 10 }
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)


# threads set 0 will default 8
def test_Pharos_Threads_Set_0_211():
    #pharos.deploy(conf)
    pharos.copyfile('config/pharos/pharos_threads0.conf', '/home/admin/pharos/conf/pharos.conf')
    pharos.restartPharos()
    time.sleep(5)
    output = system_util.exe_cmd_via_ssh(dnsip, 'ps -ef | grep pharos | grep -v grep | grep -v admin')
    output = system_util.exe_cmd_via_ssh(dnsip, 'pstree -c '+ output[0].split()[1] +' | wc -l')
    print output
    assert output == ['8']

def test_Pharos_Threads_Set_16_212():
    pharos.copyfile('config/pharos/pharos_threads16.conf', '/home/admin/pharos/conf/pharos.conf')
    pharos.restartPharos()
    time.sleep(5)
    output = system_util.exe_cmd_via_ssh(dnsip, 'ps -ef | grep pharos | grep -v grep | grep -v admin')
    output = system_util.exe_cmd_via_ssh(dnsip, 'pstree -c '+ output[0].split()[1] +' | wc -l')
    assert output == ['16']

# threads set 65535 will default 4
def test_Pharos_Threads_Set_65535_213():
    pharos.copyfile('config/pharos/pharos_threads65535.conf', '/home/admin/pharos/conf/pharos.conf')
    pharos.restartPharos()
    time.sleep(5)
    output = system_util.exe_cmd_via_ssh(dnsip, 'ps -ef | grep pharos | grep -v grep | grep -v admin')
    output = system_util.exe_cmd_via_ssh(dnsip, 'pstree -c '+ output[0].split()[1] +' | wc -l')
    assert output == ['4']


def test_CName_Recursion_214():
    url1 = 'img01.taobaocdn.com.danuoyi.tbcache.com'
    conf['pool'] = {'WT_BJ_Pool': {'QueryType':'CName', 'value':url1},
                    'WT_BJ_HD_Pool': {'vs': [('vs1', 1)]}}
    conf['region']= {'WT_BJ_Region': {'range':[(laddr, laddr)],'pool': [('WT_BJ_Pool', 300), ('WT_BJ_HD_Pool', 200)]}}
    conf['wideip']= {'wideip1': {'pool': ['WT_BJ_Pool']},
                     'wideip2': {'url':url1, 'pool': ['WT_BJ_HD_Pool']}}
    pharos.deploy(conf)
    dns   = { 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = { 'ancount': 0, 'rcode': 0}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)


