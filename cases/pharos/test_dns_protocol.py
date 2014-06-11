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
    config= {
            'vs'    :{'vs1': {'vs_ip': '10.235.160.93', 'host_name':'vkvm160093.sqa.cm6', 'host': 'vkvm160093.sqa.cm6'}},
            'pool'  :{'WangTong_Beijing_Pool': {'rr_ldns_limit': 1, 'in_use':1, 'available':1, 'ttl':300, 'QueryType':'A', 'vs': [('vs1', 1)]}},
            'region':{'WangTong_Beijing_Region': {'range':[('10.235.160.53', '10.235.160.53')], 'pool': [('WangTong_Beijing_Pool', 100)]}},
            'wideip':{'wideip1': {'url':'img01.taobaocdn.com.danuoyi.tbcache.com', 'pool': ['WangTong_Beijing_Pool']}}
            }
def teardown_function(function):
    print ("teardown_function:%s" % function.__name__)



def test_raw_query():
    data = '\xd7\x76\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x05\x69\x6d\x67\x30\x31\x09\x74\x61\x6f\x62\x61\x6f\x63\x64\x6e\x03\x63\x6f\x6d\x07\x64\x61\x6e\x75\x6f\x79\x69\x07\x74\x62\x63\x61\x63\x68\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01'
    check = { 'an_rdata': ['10.235.160.93'] }
    assert DNS.send_raw_dns(data, 'UDP', check)
    logger.debug("# Test # test stopped and success!")

def test_A():
    logger.debug("# Test # start to do the env deploy...")
    dns   = { 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}] }
    check = { 'an_rdata': [('10.235.160.93', 1)]}
    pharos.deploy(config)
    assert  DNS.do_dns(config, dns, check)
    

