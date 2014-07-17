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

def setup_module(module):
    print ("setup_module:%s" % module.__name__)
def teardown_module(module):
    print ("teardown_module:%s" % module.__name__)
def setup_function(function):
    print ("setup_function:%s" % function.__name__)
    global conf
    conf= {
          'vs'    :{'vs1':{'vs_ip':ip1,'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6', 'url':'/status'}},
          'pool'  :{'WT_BJ_Pool': {'ttl':300, 'QueryType':'A', 'vs': [('vs1', 1)]}},
          'region':{'WT_BJ_Region': {'range':[(laddr, laddr)],'pool': [('WT_BJ_Pool', 100)]}},
          'wideip':{'wideip1': {'url':'img01.taobaocdn.com.danuoyi.tbcache.com', 'pool': ['WT_BJ_Pool']}}
    }
def teardown_function(function):
    pass


def test_DNS_QType_A_101():
    pharos.deploy(conf)
    dns   = { 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = { 'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 100}
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)


#IPv6 is 28
def test_DNS_QType_AAAA_102():
    ipv6 = '2001:4860:4801:2:3900:6006:1300:b075'
    conf['vs']={'vs1': {'vs_ip': ipv6, 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6', 'address_type':28}}
    conf['pool'] = {'WT_BJ_Pool': {'QueryType':'AAAA', 'vs': [('vs1', 1)]}}
    conf['region']= {'WT_BJ_Region': {'range':[(laddr, laddr)],'pool': [('WT_BJ_Pool', 100)]}}
    conf['wideip']= {'wideip1': {'url':'img01.taobaocdn.com.danuoyi.tbcache.com', 'pool': ['WT_BJ_Pool'], 'in_use':1}}
    pharos.deploy(conf)

    dns   = { 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com', 'qd_qtype':28}]}
    check = { 'an_rdata': [(ipv6, 1)], 'ancount': 1, 'total_rdata': 100}
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_DNS_QType_NS_103():
    pharos.copyfile('config/pharos/NS_SOA_DB_Data.sql', '/home/admin/pharos/conf/NS_SOA_DB_Data.sql')
    pharos.exe_cmd('/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/NS_SOA_DB_Data.sql')
    pharos.restartPharos()
    time.sleep(5)
    dns   = { 'qd':[{'qd_qname':'danuoyi.tbcache.com', 'qd_qtype':2}]}
    check = { 'an_rdata': [('danuoyins6.tbcache.com', 1)], 'ancount': 1, 'total_rdata': 100}
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_DNS_QType_SOA_104():
    conf['pool'] = {'WT_BJ_Pool': {'QueryType':'SOA', 'vs': [('vs1', 1)]}}
    conf['vs']={'vs1': {'vs_ip': ip1, 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6', 'address_type':6}}
    conf['region']= {'WT_BJ_Region': {'range':[(laddr, laddr)],'pool': [('WT_BJ_Pool', 100)]}}
    conf['wideip']= {'wideip1': {'url':'img01.taobaocdn.com.danuoyi.tbcache.com', 'pool': ['WT_BJ_Pool']}}
    pharos.deploy(conf)
    dns   = { 'qd':[{'qd_qname':'danuoyi.tbcache.com', 'qd_qtype':6}]}
    check = { 'an_type': 6, 'an_prins':'danuoyins1.tbcache.com', 'an_respmail':'root.taobao.com', 'ancount': 1 }
    DNS.do_dns(dns, check, 1)
    logger.debug(elog)


def test_DNS_QType_CNAME_105():
    url1 = 'cname.taobaocdn.com.danuoyi.tbcache.com'
    conf['pool'] = {'WT_BJ_Pool': {'QueryType':'CName', 'value':url1},
                    'WT_BJ_HD_Pool': {'vs': [('vs1', 1)]}}
    conf['region']= {'WT_BJ_Region': {'range':[(laddr, laddr)],'pool': [('WT_BJ_Pool', 100)]}}
    conf['wideip']= {'wideip1': {'pool': ['WT_BJ_Pool']},
                     'wideip2': {'url':url1, 'pool': ['WT_BJ_HD_Pool']}}
    pharos.deploy(conf)
    dns   = { 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com', 'qd_qtype':5}]}
    check = { 'ancount': 1, 'an_type': 5, 'an_rdata': [(url1, 1)], 'total_rdata': 10 }
    DNS.do_dns(dns, check, 10)
    dns   = { 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = { 'ancount': 2, 'an_rdata': [(ip1, 0.5), (url1, 0.5)], 'total_rdata': 200 }
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)


# SRV type 33
def test_DNS_QType_SRV_106():
    url1 = '_ftp._TCP.img01.taobaocdn.com.danuoyi.tbcache.com'
    conf['vs'] = {}
    conf['pool'] = {'WangTong_Beijing_SRV_Pool': {'QueryType':'SRV'}}
    conf['region']= {'WT_BJ_Region': {'range':[(laddr, laddr)],'pool':[('WangTong_Beijing_SRV_Pool', 100)]}}
    conf['wideip']= {'wideip1': {'url':url1, 'pool': ['WangTong_Beijing_SRV_Pool']}}
    pharos.deploy(conf)
    pharos.copyfile('config/pharos/NS_SOA_DB_Data.sql', '/home/admin/pharos/conf/NS_SOA_DB_Data.sql')
    pharos.copyfile('config/pharos/callProcedure.sql', '/home/admin/pharos/conf/callProcedure.sql')
    pharos.exe_cmd('/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/NS_SOA_DB_Data.sql')
    pharos.exe_cmd('/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/callProcedure.sql ')
    pharos.restartPharos()
    time.sleep(5)

    dns   = { 'qd':[{'qd_qname':url1, 'qd_qtype':33}]}
    check = { 'ancount': 4, 'an_rdata': [('host1.taobao.com', 0.25), ('host2.taobao.com', 0.25), ('host3.taobao.com', 0.25), ('host1.tb.com', 0.25)], 'total_rdata': 400 }
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_DNS_QType_PTR_107():
    pharos.deploy(conf)
    dns   = { 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com', 'qd_qtype':12}]}
    check = { 'ancount': 0, 'rcode':0, 'nscount':1}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

# use 107 config
def test_DNS_Multi_Query_One_Packet_108():
    #pharos.deploy(conf)
    dns   = {'qdcount':2, 'qd':[{'qd_qname':'img02.taobaocdn.com.danuoyi.tbcache.com',}, {'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = { 'ancount': 0, 'qdcount':2, 'rcode':0, 'nscount':0}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Multi_Query_Multi_Type_109():
    #pharos.deploy(conf)
    dns   = {'qdcount':2, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com','qd_qtype':1}, {'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com', 'qd_qtype':6}]}
    check = { 'ancount': 0, 'qdcount':2, 'rcode':0, 'nscount':0}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)


def test_DNS_Header_ID_0_110():
    #pharos.deploy(conf)
    dns   = {'id':0, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_ID_65535_111():
    #pharos.deploy(conf)
    dns   = {'id':65535, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_Set_Qr_112():
    #pharos.deploy(conf)
    dns   = {'qr':1, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'ancount':0, 'rcode':0}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_Opcode_0_113():
    #pharos.deploy(conf)
    dns   = {'opcode':0, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_Opcode_4_114():
    #pharos.deploy(conf)
    dns   = {'opcode':4, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'ancount':0, 'rcode':4}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_Opcode_15_115():
    #pharos.deploy(conf)
    dns   = {'opcode':15, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'ancount':0, 'rcode':4}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_AA_1_116():
    #pharos.deploy(conf)
    dns   = {'aa':1, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'rcode':0, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

# send tc=1, reply tc shouldnot 1 bug
def test_DNS_Header_Tc_1_117():
    pharos.deploy(conf)
    dns   = {'tc':1, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'rcode':0, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_Tc_0_118():
    #pharos.deploy(conf)
    dns   = {'tc':0, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'rcode':0, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_Z_0_119():
    #pharos.deploy(conf)
    dns   = {'z':0, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'rcode':0, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_Z_7_120():
    #pharos.deploy(conf)
    dns   = {'z':7, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'rcode':0, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_AN_1_121():
    #pharos.deploy(conf)
    dns   = {'ancount':1, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'rcode':0, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_NS_1_122():
    #pharos.deploy(conf)
    dns   = {'nscount':1, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'rcode':0, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_AR_1_123():
    #pharos.deploy(conf)
    dns   = {'arcount':1, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'rcode':1}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_Noquery_Noqd_124():
    #pharos.deploy(conf)
    dns   = {'qdcount':0, 'qd':[{'qd_qname':''}]}
    check = {'rcode':0, 'ancount': 0, 'qdcount': 0}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_Noquery_Noqd_125():
    #pharos.deploy(conf)
    dns   = {'qdcount':1, 'qd':[]}
    check = {'rcode':1}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_query2_qd1_126():
    #pharos.deploy(conf)
    dns   = {'qdcount':1, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'},{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'rcode':0, 'qdcount':1}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_query1_qd2_127():
    #pharos.deploy(conf)
    dns   = {'qdcount':2, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'rcode':1, 'qr':1}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_Qclass_128():
    #pharos.deploy(conf)
    dns   = {'qclass':17, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'rcode':0, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Header_Qtype0_129():
    #pharos.deploy(conf)
    dns   = {'qtype':0, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'rcode':0, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Qname_Error_130():
    #pharos.deploy(conf)
    data='\xd7\x76\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x05\x69\x6d\x67\x30\x31\x09\x74\x61\x6f\x62\x61\x6f\x63\x64\x6e\x03\x63\x6f\x6d\x07\x64\x61\x6e\x75\x6f\x79\x69\x07\x74\x62\x63\x61\x63\x68\x65\x05\x63\x6f\x6d\x00\x00\x01\x00\x01'
    check = {'rcode':1}
    dns   = {'data':data}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Long_Qname_131():
    #pharos.deploy(conf)
    data='\xd7\x76\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\xff\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\xff\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61\x05\x69\x6d\x67\x30\x31\x09\x74\x61\x6f\x62\x61\x6f\x63\x64\x6e\x03\x63\x6f\x6d\x07\x64\x61\x6e\x75\x6f\x79\x69\x07\x74\x62\x63\x61\x63\x68\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01'
    check = {'rcode':1}
    dns   = {'data':data}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Extensive_Domain_132():
    conf['wideip']={'wideip1': {'url': '*.danuoyi.tbcache.com', 'pool': ['WT_BJ_Pool']}}
    pharos.deploy(conf)
    dns  = {'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}] }
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)

    dns  = {'qd':[{'qd_qname':'*.danuoyi.tbcache.com'}] }
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)

    dns  = {'qd':[{'qd_qname':'danuoyi.tbcache.com'}] }
    check = {'rcode':0, 'ancount':0}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

# edns    
def test_DNS_EDNS_133():
    conf['region']={'WT_BJ_Region': {'range':[('10.1.1.1', '10.1.1.1')], 'pool': [('WT_BJ_Pool', 100)]}}
    #pharos.deploy(conf)
    data='\x78\x08\x01\x00\x00\x01\x00\x00\x00\x00\x00\x01\x05\x69\x6d\x67\x30\x31\x09\x74\x61\x6f\x62\x61\x6f\x63\x64\x6e\x03\x63\x6f\x6d\x07\x64\x61\x6e\x75\x6f\x79\x69\x07\x74\x62\x63\x61\x63\x68\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01\x00\x00\x29\x10\x00\x00\x00\x00\x00\x00\x0c\x00\x08\x00\x08\x00\x01\x20\x00\x0a\x01\x01\x01'
    dns  = {'data':data}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)

def test_DNS_Error_Qname_134():
    pharos.deploy(conf)
    data='\xd7\x76\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x05\x69\x6d\x67\x30\x31\x09\x74\x61\x6f\x62\x61\x6f\x63\x64\x6e\x03\x63\x6f\x6d\x07\x64\x61\x6e\x75\x6f\x79\x69\x07\x74\x62\x63\x61\x63\x68\x65\x03\x63\x6f\x6d\x00\x00\x01\x00'
    check = {'rcode':1}
    dns   = {'data':data}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_NXDOMAIN_135():
    #pharos.deploy(conf)
    dns  = {'qd':[{'qd_qname':'img02.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'rcode':3,  'ancount': 0}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

# error
def test_DNS_Qtype_NoImpl_136():
    #pharos.deploy(conf)
    dns   = {'opcode':1, 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'rcode':4}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_REFUSED_137():
    #pharos.deploy(conf)
    dns  = {'qd':[{'qd_qname':'img02.taobaocdn.com.danuoyi.tbcache1.com'}]}
    check = {'rcode':5,  'ancount': 0}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Extensive_Domain_138():
    conf['vs']={'vs1': {'vs_ip': ip1, 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6'},
                'vs2': {'vs_ip': ip2, 'host_name':'vkvm160083.sqa.cm6', 'host': 'vkvm160083.sqa.cm6'}}
    conf['pool'] = {'WT_BJ_Pool': {'rr_ldns_limit':1,'vs': [('vs1', 1)]},
                    'WT_BJ_HD_Pool': {'rr_ldns_limit':1,'vs': [('vs2', 1)]}}
    conf['region']={'WT_BJ_Region': {'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100), ('WT_BJ_HD_Pool', 100)]}}
    conf['wideip']={'wideip1': {'url':'aa.img.tbcdn.com.danuoyi.tbcache.com', 'pool': ['WT_BJ_Pool']},
                    'wideip2': {'url':'*.img.tbcdn.com.danuoyi.tbcache.com',  'pool': ['WT_BJ_HD_Pool']}}
    pharos.deploy(conf)
    dns =  {'qd':[{'qd_qname':'aa.img.tbcdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

#use 138 config
def test_DNS_Extensive_Domain_139():
    dns =  {'qd':[{'qd_qname':'bb.img.tbcdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip2, 1)], 'ancount': 1, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)


def test_DNS_Extensive_Domain_140():
    dns =  {'qd':[{'qd_qname':'aa.bb.cc.img.tbcdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip2, 1)], 'ancount': 1, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Extensive_Domain_141():
    dns =  {'qd':[{'qd_qname':'bb.aa.img.tbcdn.com.danuoyi.tbcache.com'}]}
    check = {'ancount': 0, 'rcode': 3}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Extensive_Domain_142():
    dns =  {'qd':[{'qd_qname':'*.img.tbcdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip2, 1)], 'ancount': 1, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Extensive_Domain_143():
    dns =  {'qd':[{'qd_qname':'aa.*.img.tbcdn.com.danuoyi.tbcache.com'}]}
    check = {'ancount': 0, 'rcode': 3}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Extensive_Domain_144():
    dns =  {'qd':[{'qd_qname':'aa.*.bb.img.tbcdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip2, 1)], 'ancount': 1, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_TCP_QType_A_145():
    pharos.deploy(conf)
    dns   = {'SOCKET_TYPE': 'TCP', 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 1}
    DNS.do_dns(dns, check, 1)
    logger.debug(elog)

def test_DNS_TCP_QType_AAAA_146():
    ipv6 = '2001:4860:4801:2:3900:6006:1300:b075'
    conf['vs']={'vs1': {'vs_ip': ipv6, 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6', 'address_type':28}}
    conf['pool'] = {'WT_BJ_Pool': {'QueryType':'AAAA', 'vs': [('vs1', 1)]}}
    conf['region']= {'WT_BJ_Region': {'range':[(laddr, laddr)],'pool': [('WT_BJ_Pool', 100)]}}
    conf['wideip']= {'wideip1': {'url':'img01.taobaocdn.com.danuoyi.tbcache.com', 'pool': ['WT_BJ_Pool'], 'in_use':1}}
    pharos.deploy(conf)
    dns   = {'SOCKET_TYPE': 'TCP', 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com', 'qd_qtype':28}]}
    check = { 'an_rdata': [(ipv6, 1)], 'ancount': 1, 'total_rdata': 1}
    DNS.do_dns(dns, check, 1)
    logger.debug(elog)

def test_DNS_TCP_QType_NS_147():
    pharos.copyfile('config/pharos/NS_SOA_DB_Data.sql', '/home/admin/pharos/conf/NS_SOA_DB_Data.sql')
    pharos.exe_cmd('/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/NS_SOA_DB_Data.sql')
    pharos.restartPharos()
    time.sleep(5)
    dns   = { 'SOCKET_TYPE': 'TCP', 'qd':[{'qd_qname':'danuoyi.tbcache.com', 'qd_qtype':2}]}
    check = { 'an_rdata': [('danuoyins6.tbcache.com', 1)], 'ancount': 1, 'total_rdata': 100}
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_DNS_TCP_QType_SOA_148():
    conf['pool'] = {'WT_BJ_Pool': {'QueryType':'SOA', 'vs': [('vs1', 1)]}}
    conf['vs']={'vs1': {'vs_ip': ip1, 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6', 'address_type':6}}
    conf['region']= {'WT_BJ_Region': {'range':[(laddr, laddr)],'pool': [('WT_BJ_Pool', 100)]}}
    conf['wideip']= {'wideip1': {'url':'img01.taobaocdn.com.danuoyi.tbcache.com', 'pool': ['WT_BJ_Pool']}}
    pharos.deploy(conf)
    dns   = { 'SOCKET_TYPE': 'TCP', 'qd':[{'qd_qname':'danuoyi.tbcache.com', 'qd_qtype':6}]}
    check = { 'an_type': 6, 'an_prins':'danuoyins1.tbcache.com', 'an_respmail':'root.taobao.com', 'ancount': 1 }
    DNS.do_dns(dns, check, 1)
    logger.debug(elog)

def test_DNS_TCP_QType_CNAME_149():
    url1 = 'cname.taobaocdn.com.danuoyi.tbcache.com'
    conf['pool'] = {'WT_BJ_Pool': {'QueryType':'CName', 'value':url1},
                    'WT_BJ_HD_Pool': {'vs': [('vs1', 1)]}}
    conf['region']= {'WT_BJ_Region': {'range':[(laddr, laddr)],'pool': [('WT_BJ_Pool', 100)]}}
    conf['wideip']= {'wideip1': {'pool': ['WT_BJ_Pool']},
                     'wideip2': {'url':url1, 'pool': ['WT_BJ_HD_Pool']}}
    pharos.deploy(conf)
    dns   = { 'SOCKET_TYPE': 'TCP', 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com', 'qd_qtype':5}]}
    check = { 'ancount': 1, 'an_type': 5, 'an_rdata': [(url1, 1)], 'total_rdata': 10 }
    DNS.do_dns(dns, check, 10)
    dns   = { 'SOCKET_TYPE': 'TCP', 'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}]}
    check = { 'ancount': 2, 'an_rdata': [(ip1, 0.5), (url1, 0.5)], 'total_rdata': 200 }
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)


def test_DNS_TCP_QType_SRV_150():
    url1 = '_ftp._TCP.img01.taobaocdn.com.danuoyi.tbcache.com'
    conf['vs'] = {}
    conf['pool'] = {'WangTong_Beijing_SRV_Pool': {'QueryType':'SRV'}}
    conf['region']= {'WT_BJ_Region': {'range':[(laddr, laddr)],'pool':[('WangTong_Beijing_SRV_Pool', 100)]}}
    conf['wideip']= {'wideip1': {'url':url1, 'pool': ['WangTong_Beijing_SRV_Pool']}}
    pharos.deploy(conf)
    pharos.copyfile('config/pharos/NS_SOA_DB_Data.sql', '/home/admin/pharos/conf/NS_SOA_DB_Data.sql')
    pharos.copyfile('config/pharos/callProcedure.sql', '/home/admin/pharos/conf/callProcedure.sql')
    pharos.exe_cmd('/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/NS_SOA_DB_Data.sql')
    pharos.exe_cmd('/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/callProcedure.sql ')
    pharos.restartPharos()
    time.sleep(5)

    dns   = { 'SOCKET_TYPE': 'TCP', 'qd':[{'qd_qname':url1, 'qd_qtype':33}]}
    check = { 'ancount': 4, 'an_rdata': [('host1.taobao.com', 0.25), ('host2.taobao.com', 0.25), ('host3.taobao.com', 0.25), ('host1.tb.com', 0.25)], 'total_rdata': 400 }
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_DNS_Response_EX_512_151():
    ip1 = "2001:4860:4801:2:3900:6006:1300:b075";
    ip2 = "2001:4860:4801:2:3900:6006:1300:b076";
    ip3 = "2001:4860:4801:2:3900:6006:1300:b077";
    ip4 = "2001:4860:4801:2:3900:6006:1300:b078";
    ip5 = "2001:4860:4801:2:3900:6006:1300:b079";
    ip6 = "2001:4860:4801:2:3900:6006:1300:b07a";
    ip7 = "2001:4860:4801:2:3900:6006:1300:b07b";
    ip8 = "2001:4860:4801:2:3900:6006:1300:b07c";
    ip9 = "2001:4860:4801:2:3900:6006:1300:b07d";
    ip10 = "2001:4860:4801:2:3900:6006:1300:b07e";
    ip11 = "2001:4860:4801:2:3900:6006:1300:b17e";
    ip12 = "2001:4860:4801:2:3900:6006:1300:b27e";
    ip13 = "2001:4860:4801:2:3900:6006:1300:b37e";
    ip14 = "2001:4860:4801:2:3900:6006:1300:b47e";
    ip15 = "2001:4860:4801:2:3900:6006:1300:b57e";
    ip16 = "2001:4860:4801:2:3900:6006:1300:b67e";
    ip17 = "2001:4860:4801:2:3900:6006:1300:b77e";
    ip18 = "2001:4860:4801:2:3900:6006:1300:b87e";
    ip19 = "2001:4860:4801:2:3900:6006:1300:b97e";
    ip20 = "2001:4860:4801:2:3900:6006:1300:ba7e";

    conf['vs'] ={'vs1':{'vs_ip':ip1,'host_name':ip1, 'host': ip1, 'url':'/status', 'address_type':28},
                 'vs2':{'vs_ip':ip2,'host_name':ip2, 'host': ip2, 'url':'/status', 'address_type':28},
                 'vs3':{'vs_ip':ip3,'host_name':ip3, 'host': ip3, 'url':'/status', 'address_type':28},
                 'vs4':{'vs_ip':ip4,'host_name':ip4, 'host': ip4, 'url':'/status', 'address_type':28},
                 'vs5':{'vs_ip':ip5,'host_name':ip5, 'host': ip5, 'url':'/status', 'address_type':28},
                 'vs6':{'vs_ip':ip6,'host_name':ip6, 'host': ip6, 'url':'/status', 'address_type':28},
                 'vs7':{'vs_ip':ip7,'host_name':ip7, 'host': ip7, 'url':'/status', 'address_type':28},
                 'vs8':{'vs_ip':ip8,'host_name':ip8, 'host': ip8, 'url':'/status', 'address_type':28},
                 'vs9':{'vs_ip':ip9,'host_name':ip9, 'host': ip9, 'url':'/status', 'address_type':28},
                 'vs10':{'vs_ip':ip10,'host_name':ip10, 'host': ip10, 'url':'/status', 'address_type':28},
                 'vs11':{'vs_ip':ip11,'host_name':ip11, 'host': ip11, 'url':'/status', 'address_type':28},
                 'vs12':{'vs_ip':ip12,'host_name':ip12, 'host': ip12, 'url':'/status', 'address_type':28},
                 'vs13':{'vs_ip':ip13,'host_name':ip13, 'host': ip13, 'url':'/status', 'address_type':28},
                 'vs14':{'vs_ip':ip14,'host_name':ip14, 'host': ip14, 'url':'/status', 'address_type':28},
                 'vs15':{'vs_ip':ip15,'host_name':ip15, 'host': ip15, 'url':'/status', 'address_type':28},
                 'vs16':{'vs_ip':ip16,'host_name':ip16, 'host': ip16, 'url':'/status', 'address_type':28},
                 'vs17':{'vs_ip':ip17,'host_name':ip17, 'host': ip17, 'url':'/status', 'address_type':28},
                 'vs18':{'vs_ip':ip18,'host_name':ip18, 'host': ip18, 'url':'/status', 'address_type':28},
                 'vs19':{'vs_ip':ip19,'host_name':ip19, 'host': ip19, 'url':'/status', 'address_type':28},
                 'vs20':{'vs_ip':ip20,'host_name':ip20, 'host': ip20, 'url':'/status', 'address_type':28}}
    conf['pool'] = {'WT_BJ_Pool': {'QueryType':'AAAA', 'rr_ldns_limit':30, 'vs': [('vs1', 1), ('vs2', 1), ('vs3', 1), ('vs4', 1), ('vs5', 1), ('vs6', 1), ('vs7', 1), ('vs8', 1), ('vs9', 1), ('vs10', 1), ('vs11', 1), ('vs12', 1), ('vs13', 1), ('vs14', 1), ('vs15', 1), ('vs16', 1), ('vs17', 1), ('vs18', 1), ('vs19', 1), ('vs20', 1)]}}
    conf['region']= {'WT_BJ_Region': {'range':[(laddr, laddr)],'pool': [('WT_BJ_Pool', 100)]}}
    conf['wideip']= {'wideip1': {'url':'img01aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.taobaocdn.com.danuoyi.tbcache.com', 'pool': ['WT_BJ_Pool']}}
    pharos.deploy(conf)

    dns = {'qd':[{'qd_qname':'img01aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.taobaocdn.com.danuoyi.tbcache.com', 'qd_qtype':28}]}
    check = { 'tc':1 }
    result = False
    for i in range(0, 10):
        try:
            DNS.do_dns(dns, check, 10)
            result = True
        except:
            pass
    assert result

    dns = { 'SOCKET_TYPE': 'TCP', 'qd':[{'qd_qname':'img01aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.taobaocdn.com.danuoyi.tbcache.com', 'qd_qtype':28}]}
    check = { 'an_name':'img01aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.taobaocdn.com.danuoyi.tbcache.com', 'tc':0, 'rcode':0, 'ancount': '>=1' }
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)
 
def test_DNS_TCP_EDNS_152():
    conf['region']={'WT_BJ_Region': {'range':[('10.1.1.1', '10.1.1.1')], 'pool': [('WT_BJ_Pool', 100)]}}
    pharos.deploy(conf)
    data = '\xc8\x32\x01\x00\x00\x01\x00\x00\x00\x00\x00\x01\x05\x69\x6d\x67\x30\x31\x09\x74\x61\x6f\x62\x61\x6f\x63\x64\x6e\x03\x63\x6f\x6d\x07\x64\x61\x6e\x75\x6f\x79\x69\x07\x74\x62\x63\x61\x63\x68\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01\x00\x00\x29\x10\x00\x00\x00\x00\x00\x00\x0c\x00\x08\x00\x08\x00\x01\x20\x00\x0a\x01\x01\x01'
    dns  = {'SOCKET_TYPE': 'TCP', 'data':data}
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)

def test_DNS_Extensive_Domain_SRV_153():
    url1 = '_ftp._tcp.aa.img.tbcdn.com.danuoyi.tbcache.com'
    url2 = '_ftp._tcp.*.img.tbcdn.com.danuoyi.tbcache.com'
    conf['vs'] = {}
    conf['pool'] = {'WangTong_Beijing_SRV_Pool': {'QueryType':'SRV'},
                    'WangTong_Beijing_HaiDian_Pool': {'QueryType':'SRV'}}
    conf['region']= {'WT_BJ_Region': {'range':[(laddr, laddr)],'pool':[('WangTong_Beijing_SRV_Pool', 100), ('WangTong_Beijing_HaiDian_Pool', 100)]}}
    conf['wideip']= {'wideip1': {'url':url1, 'pool': ['WangTong_Beijing_SRV_Pool']},
                     'wideip2': {'url':url2, 'pool': ['WangTong_Beijing_HaiDian_Pool']}}
    pharos.deploy(conf)
    pharos.copyfile('config/pharos/NS_SOA_DB_Data.sql', '/home/admin/pharos/conf/NS_SOA_DB_Data.sql')
    pharos.copyfile('config/pharos/callProcedure.sql', '/home/admin/pharos/conf/callProcedure.sql')
    pharos.exe_cmd('/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/NS_SOA_DB_Data.sql')
    pharos.exe_cmd('/usr/bin/mysql -uroot -pwelcome < /home/admin/pharos/conf/callProcedure.sql ')
    pharos.restartPharos()
    time.sleep(5)

    dns   = { 'qd':[{'qd_qname':'_ftp._tcp.aa.img.tbcdn.com.danuoyi.tbcache.com', 'qd_qtype':33}]}
    check = { 'ancount': 4, 'an_rdata': [('host1.taobao.com', 0.25), ('host2.taobao.com', 0.25), ('host3.taobao.com', 0.25), ('host1.tb.com', 0.25)], 'total_rdata': 400 }
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_DNS_Extensive_Domain_SRV_154():
    dns   = { 'qd':[{'qd_qname':'_ftp._tcp.bb.img.tbcdn.com.danuoyi.tbcache.com', 'qd_qtype':33}]}
    check = { 'ancount': 1, 'an_rdata': [('host3.tb.com', 1)], 'total_rdata': 100 }
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_DNS_Extensive_Domain_SRV_155():
    dns   = { 'qd':[{'qd_qname':'_ftp._tcp.aa.bb.cc.img.tbcdn.com.danuoyi.tbcache.com', 'qd_qtype':33}]}
    check = { 'ancount': 1, 'an_rdata': [('host3.tb.com', 1)], 'total_rdata': 100 }
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_DNS_Extensive_Domain_SRV_156():
    dns   = { 'qd':[{'qd_qname':'_ftp._tcp.bb.aa.img.tbcdn.com.danuoyi.tbcache.com', 'qd_qtype':33}]}
    check = { 'ancount': 1, 'an_rdata': [('host3.tb.com', 1)], 'total_rdata': 100 }
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_DNS_Extensive_Domain_SRV_157():
    dns   = { 'qd':[{'qd_qname':'_ftp._tcp.*.img.tbcdn.com.danuoyi.tbcache.com', 'qd_qtype':33}]}
    check = { 'ancount': 1, 'an_rdata': [('host3.tb.com', 1)], 'total_rdata': 100 }
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_DNS_Extensive_Domain_SRV_158():
    dns   = { 'qd':[{'qd_qname':'_ftp._tcp.aa.*.img.tbcdn.com.danuoyi.tbcache.com', 'qd_qtype':33}]}
    check = { 'ancount': 1, 'an_rdata': [('host3.tb.com', 1)], 'total_rdata': 100 }
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_DNS_Extensive_Domain_SRV_159():
    dns   = { 'qd':[{'qd_qname':'_ftp._tcp.aa.*.bb.img.tbcdn.com.danuoyi.tbcache.com', 'qd_qtype':33}]}
    check = { 'ancount': 1, 'an_rdata': [('host3.tb.com', 1)], 'total_rdata': 100 }
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)


def test_DNS_Qname_Case_Sensitivity_160():
    conf['wideip']={'wideip1': {'url': 'img01.taobaoCDN.com.danuoyi.tbcAche.com', 'pool': ['WT_BJ_Pool']}}
    pharos.deploy(conf)
    dns  = {'qd':[{'qd_qname':'IMG01.taobaocdn.com.danuoyI.tbcache.COM'}] }
    check = {'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 10}
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_DNS_Qname_empty_SOA_161():
    conf['vs'] ={'vs1':{'vs_ip':ip1,'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6', 'url':'/status'},
                 'vs2':{'vs_ip':ip2,'host_name':'vkvm160083.sqa.cm6', 'host': 'vkvm160083.sqa.cm6', 'url':'/status'},
                 'vs3':{'vs_ip':ip3,'host_name':'vkvm160093.sqa.cm6', 'host': 'vkvm160093.sqa.cm6', 'url':'/status'}}
    conf['pool'] = {'WT_BJ_Pool': {'QueryType':'SOA', 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 5)]}}
    pharos.deploy(conf)
    dns   = { 'qd':[{'qd_qname':'.', 'qd_qtype':6}]}
    check = { 'rcode': 5, 'qr':1}
    DNS.do_dns(dns, check, 1)
    logger.debug(elog)


