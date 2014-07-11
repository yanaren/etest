from   src.util.logger          import logger
import src.protocol.dns.runtime as     DNS
import src.deploy.runtime       as     runtime
import src.util.system_util     as     system_util
import pytest
conf = {}

def setup_module(module):
    print ("setup_module:%s" % module.__name__)
def teardown_module(module):
    print ("teardown_module:%s" % module.__name__)
def setup_function(function):
    print ("setup_function:%s" % function.__name__)
    global conf
    conf= {
          'vs'    :{'vs1': {'vs_ip': '10.235.160.73', 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6'},
                    'vs2': {'vs_ip': '10.235.160.83', 'host_name':'vkvm160083.sqa.cm6', 'host': 'vkvm160083.sqa.cm6'},
                    'vs3': {'vs_ip': '10.235.160.93', 'host_name':'vkvm160093.sqa.cm6', 'host': 'vkvm160093.sqa.cm6'}},
          'pool'  :{'WangTong_Pool': {'rr_ldns_limit': 1, 'available':1, 'ttl':300, 'QueryType':'A', 'vs': [('vs1', 1)]}},
          'region':{'WangTong_Region': {'range':[('10.235.160.53', '10.235.160.53')], 'pool': [('WangTong_Pool', 100)]}},
          'wideip':{'wideip1': {'url':'img01.taobaocdn.com.danuoyi.tbcache.com', 'pool': ['WangTong_Pool']}}
    }
def teardown_function(function):
    print ("teardown_function:%s" % function.__name__)


def test_A():
    conf['pool'] = {'WangTong_Pool': {'rr_ldns_limit': 2, 'vs': [('vs1', 1), ('vs2', 1)]}}
    dns  = {'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check= {'an_rdata': [('10.235.160.83', 0.5)]}
    data = {'10.235.160.0':{'10.235.160.53':1,'10.235.160.63':2}, 
            '10.235.161.0':{'10.235.160.13':3,'10.235.160.23':4} }
    runtime.deploy(conf)
    DNS.do_dns(data, dns, check, 100)

def test_vs_diff_ratio():
    conf['pool'] = {'WangTong_Pool': {'rr_ldns_limit':2, 'vs': [('vs1', 2), ('vs2', 2), ('vs3', 2)]}}
    dns  = {'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check= {'an_rdata': [('10.235.160.83', 0.3), ('10.235.160.93', 0.3)]}
    data = {'10.235.160.0':{'10.235.160.53':1,'10.235.160.63':2},   
            '10.235.161.0':{'10.235.160.13':3,'10.235.160.23':4} }
    runtime.deploy(conf)
    DNS.do_dns(data, dns, check, 100)


