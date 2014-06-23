from   src.util.logger      import logger
import src.protocol.dns.dns as DNS
import src.deploy.apdns     as apdns
import src.util.system_util as system_util
import pytest

def setup_module(module):
    print ("setup_module:%s" % module.__name__)
def teardown_module(module):
    print ("teardown_module:%s" % module.__name__)
def setup_function(function):
    print ("setup_function:%s" % function.__name__)
def teardown_function(function):
    print ("teardown_function:%s" % function.__name__)


# test with raw socket
def test_raw_example():
    data = '\xd7\x76\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x05\x69\x6d\x67\x30\x31\x09\x74\x61\x6f\x62\x61\x6f\x63\x64\x6e\x03\x63\x6f\x6d\x07\x64\x61\x6e\x75\x6f\x79\x69\x07\x74\x62\x63\x61\x63\x68\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01'
    check = { 'ancount': '>0'}
    assert DNS.do_dns(data, check, times=50)
    logger.debug("# Test # test stopped and success!")


# test a simple A type query
def test_A_01():
    dns   = {'DNS_HOST': '8.8.8.8', 'qd':[{'qd_qname':'dns-healthcheck.taobao.com'}]}
    check = { 'ancount': '>0', 'an_rdata': [('127.0.0.1', 1)]}
    assert  DNS.do_dns(dns, check, times=100)
    logger.debug("# Test # test stopped and success!")
    

