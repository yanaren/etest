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


def test_A():
    logger.debug("# Test # start to do the env deploy...")
    dns   = { 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}] }
    check = { 'an_rdata': [('10.235.160.93', 1)]}
    pharos.deploy(config)
    assert  DNS.do_dns(config, dns, check)
    

