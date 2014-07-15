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

def test_DNS_Header_Tc_1_117():
    #pharos.deploy(conf)
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




