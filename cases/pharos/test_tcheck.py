from   src.util.logger      import logger
import src.protocol.dns.dns as DNS
import src.deploy.pharos    as pharos
import src.util.system_util as system_util
import pytest
config = {}

def setup_module(module):
    print ("setup_module:%s" % module.__name__)
    #system_util.exe_cmd_via_ssh(DNS['DNS_HOST'], DNS['cmd_instal'])
    #pharos.setup()

def teardown_module(module):
    print ("teardown_module:%s" % module.__name__)
def setup_function(function):
    print ("setup_function:%s" % function.__name__)
    global config
    config={
        'tcheck':{'checker': ['master', 'slave1' ], "vs": ['vs1', 'vs2', 'vs3']},
        'vs'    :{'vs1': {'vs_ip': '10.235.160.93', 'host_name':'vkvm160093.sqa.cm6', 'HC_type':0},
                  'vs2': {'vs_ip': '10.235.160.83', 'host_name':'vkvm160083.sqa.cm6', 'HC_type':0},
                  'vs3': {'vs_ip': '10.235.160.73', 'host_name':'vkvm160073.sqa.cm6', 'HC_type':0}},
        'pool'  :{'WangTong_Beijing_Pool': {'rr_ldns_limit': 1, 'in_use':1, 'available':1, 'vs': [('vs1', 1), ('vs2', 1), ('vs3', 1)]}},
        'region':{'WangTong_Beijing_Region': {'range':[('10.235.160.53', '10.235.160.53')], 'pool': [('WangTong_Beijing_Pool', 100)]}},
        'wideip':{'wideip1': {'url':'img01.taobaocdn.com.danuoyi.tbcache.com', 'pool': ['WangTong_Beijing_Pool']}}
        }

def teardown_function(function):
    print ("teardown_function:%s" % function.__name__)




# N server work in any ratio, stop one server, check the ratio
def test_N_server_1server_down_01():
    dns   = {'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}] }
    check = { 'an_rdata': [(config['vs']['vs1']['vs_ip'], 0.33), (config['vs']['vs2']['vs_ip'], 0.33), (config['vs']['vs3']['vs_ip'], 0.33)] }
    pharos.setDNS({'DNS_HOST':'10.235.160.73', 'DB_HOST': '10.235.160.73'})
    pharos.deploy(config)
    assert  DNS.do_dns(config, dns, check, times=100)

    #pharos.stopvs(['vs1'])
    #check = { 'an_rdata': [('10.235.160.83', 0.5), ('10.235.160.73', 0.5)] }
    assert  DNS.do_dns(config, dns, check, times=100)
    logger.debug("# Test # test stopped and success!")


# 1 server only, stop it and the result should be empty
def test_1vs_down_02():
    config['pool']['WangTong_Beijing_Pool'] = {'rr_ldns_limit': 1, 'in_use':1, 'available':1, 'vs': [('vs1', 1)]}
    dns   = {'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}] }
    check = { 'an_rdata': [(config['vs']['vs1']['vs_ip'], 1)] }
    pharos.setDNS({'DNS_HOST':'10.235.160.73', 'DB_HOST': '10.235.160.73'})
    pharos.deploy(config)
    assert  DNS.do_dns(config, dns, check, times=100)

    #pharos.stopvs(['vs1'])
    #check = { 'ancount': 0}
    assert  DNS.do_dns(config, dns, check, times=100)
    logger.debug("# Test # test stopped and success!")


# 2 server works, stop 1, and the result should only one
def test_2vs_1down_03():
    config['pool']['WangTong_Beijing_Pool'] = {'rr_ldns_limit': 1, 'in_use':1, 'available':1, 'vs': [('vs1', 1), ('vs2', 2)]}
    dns   = {'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}] }
    check = { 'an_rdata': [(config['vs']['vs1']['vs_ip'], 0.33), (config['vs']['vs2']['vs_ip'], 0.67)] }
    pharos.setDNS({'DNS_HOST':'10.235.160.73', 'DB_HOST': '10.235.160.73'})
    pharos.deploy(config)
    assert  DNS.do_dns(config, dns, check, times=100)

    #pharos.stopvs(['vs1'])
    #check = { 'an_rdata': [(config['vs']['vs2']['vs_ip'], 1)]}
    assert  DNS.do_dns(config, dns, check, times=100)
    logger.debug("# Test # test stopped and success!")


# 3 server, 1 server disabled, and 1 server down, only one result.
def test_3vs_1down_1disable_04():
    config['vs']['vs2'] = {'vs_ip': '10.235.160.83', 'host_name':'vkvm160083.sqa.cm6', 'HC_type':0, 'in_use': 0}
    dns   = {'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}] }
    check = { 'an_rdata': [(config['vs']['vs1']['vs_ip'], 0.5), (config['vs']['vs3']['vs_ip'], 0.5)] }
    pharos.setDNS({'DNS_HOST':'10.235.160.73', 'DB_HOST': '10.235.160.73'})
    pharos.deploy(config)
    assert  DNS.do_dns(config, dns, check, times=100)

    #pharos.stopvs(['vs1'])
    #check = { 'an_rdata': [('10.235.160.73', 1)]}
    assert  DNS.do_dns(config, dns, check, times=100)
    logger.debug("# Test # test stopped and success!")


# 3 servers, 3 down, all consider avaliable
def test_3vs_3down_05():
    dns   = {'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}] }
    check = { 'an_rdata': [(config['vs']['vs1']['vs_ip'], 0.33), (config['vs']['vs2']['vs_ip'], 0.33), (config['vs']['vs3']['vs_ip'], 0.33)] }
    pharos.setDNS({'DNS_HOST':'10.235.160.73', 'DB_HOST': '10.235.160.73'})
    pharos.deploy(config)
    assert  DNS.do_dns(config, dns, check, times=100)

    #pharos.stopvs(['vs1', 'vs2', 'vs3'])
    assert  DNS.do_dns(config, dns, check, times=100)
    logger.debug("# Test # test stopped and success!")





