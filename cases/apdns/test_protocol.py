from   src.util.logger      import logger
import src.protocol.dns.dns as DNS
import src.sniffer.sniffer  as sniffer
from src.deploy             import DNS as PARA
import pytest

# READ ME: use below config example to edit your test case
#
# input={ 'DNS_HOST': DNS['DNS_HOST'], 'DNS_PORT': DNS['DNS_PORT'], 'DNS_TYPE': DNS['DNS_TYPE'], 'data': data}  or
# input={ 'DNS_HOST': DNS['DNS_HOST'], 'DNS_PORT': DNS['DNS_PORT'], 'DNS_TYPE': DNS['DNS_TYPE'], 'id': 1, 'qr': 0, 
#         'opcode':0,'aa': 0,'tc':0,'rd':1,'ra':0,'z':0,'rcode':0,'qdcount': 1,'ancount':0,'nscount':0,'arcount': 0, 
#         'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com', 'qd_qtype': 1, 'qd_qclass': 1}] },
#         'an':[{'an_rclass': 1, 'an_ttl':1, 'an_rrname': 'www.taobao.com', 'an_rdata': '1.1.1.1', 'an_type': 1}]
#
# check = { 'qdcount':>2, 'an_rclass':1, 'an_rdata': [('10.235.160.93', 0.5), ('10.235.160.83', 0.5)]}

def setup_module(module):
    print ("setup_module:%s" % module.__name__)
def teardown_module(module):
    print ("teardown_module:%s" % module.__name__)
def setup_function(function):
    #sniffer.capture('eth0', PARA['DNS_HOST'], '53 or 5333', 'udp', '~/project/etest/log/apdns/'+ function.__name__ +'.pcap')
    print ("setup_function:%s" % function.__name__)
def teardown_function(function):
    #sniffer.join()
    print ("teardown_function:%s" % function.__name__)


# test with raw socket
def test_raw_example():
    data = '\x08\xda\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x0f\x64\x6e\x73\x2d\x68\x65\x61\x6c\x74\x68\x63\x68\x65\x63\x6b\x06\x74\x61\x6f\x62\x61\x6f\x03\x63\x6f\x6d\x00\x00\x01\x00\x01'
    input = {'DNS_HOST':'8.8.8.8', 'data': data}
    check = { 'ancount': '>0'}
    assert DNS.do_dns(input, check, times=2)
    logger.debug("# Test # test stopped and success!")


# test a simple query
def test_A_01():
    input   = {'DNS_HOST':'8.8.8.8', 'qd':[{'qd_qname':'dns-healthcheck.taobao.com'}]}
    check = { 'ancount': '>0', 'an_rdata': [('127.0.0.1', 1)]}
    assert  DNS.do_dns(input, check, times=5)
    logger.debug("# Test # test stopped and success!")
    

