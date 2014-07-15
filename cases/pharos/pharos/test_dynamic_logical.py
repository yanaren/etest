from   src.util.logger      import logger
import src.protocol.dns.dns as DNS
import src.deploy.pharos    as pharos
import src.util.system_util as system_util
import pytest
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
          'vs'    :{'vs1':{'vs_ip':ip1,'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6', 'url':'/status'},
                    'vs2':{'vs_ip':ip2,'host_name':'vkvm160083.sqa.cm6', 'host': 'vkvm160083.sqa.cm6', 'url':'/status'},
                    'vs3':{'vs_ip':ip3,'host_name':'vkvm160093.sqa.cm6', 'host': 'vkvm160093.sqa.cm6', 'url':'/status'},},
          'pool'  :{'WangTong_Pool': {'ttl':300, 'QueryType':'A', 'vs': [('vs1', 1)]}},
          'region':{'WangTong_Region': {'range':[(laddr, laddr)],'pool': [('WangTong_Pool', 100)]}},
          'wideip':{'wideip1': {'url':'img01.taobaocdn.com.danuoyi.tbcache.com', 'pool': ['WangTong_Pool'], 'in_use':1}}
    }
def teardown_function(function):
    pass



def test_IP_Region_Pool_NoBigRegion_301():
    conf['pool'] = {'WangTong_Pool': {'rr_ldns_limit': 1,'QueryType':'A', 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    check = { 'an_rdata': [(ip1, 0.16), (ip2, 0.34), (ip3, 0.5)]}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)


def test_IP_MultiRegionAndBigRegion_302():
    conf['pool'] = {'WT_BJ_Pool': {'rr_ldns_limit': 1,'vs': [('vs1', 1)]},
                    'WT_TJ_Pool': {'rr_ldns_limit': 2, 'ttl':400, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 2)]},
                    'WT_Pool'   : {'rr_ldns_limit': 3, 'ttl':600, 'vs': [('vs3', 3)]},
                    'WT_SH_Pool': {'rr_ldns_limit': 1, 'ttl':600, 'vs': [('vs3', 3)]},
                    'WT_HN_Pool': {'rr_ldns_limit': 2, 'ttl':600, 'vs': [('vs1', 3), ('vs2', 3), ('vs3', 3)]}}

    conf['region']={'WT_BJ_Region': {'range':[(laddr, laddr)], 'pri': 1, 'pool': [('WT_BJ_Pool', 100), ('WT_TJ_Pool', 200)]},
                    'DX_SH_Region': {'range':[(laddr, laddr)], 'pri': 2, 'pool': [('WT_Pool', 100), ('WT_HN_Pool', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool', 'WT_TJ_Pool', 'WT_Pool', 'WT_SH_Pool', 'WT_HN_Pool']}}
    check = { 'an_rdata': [(ip1, 0.33), (ip2, 0.33), (ip3, 0.33),], 'ancount': '>=1'}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 1000)
    logger.debug(elog)


def test_CompleRegion_Matched_303():
    conf['vs']={'vs1': {'vs_ip': ip1, 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6'},
                'vs2': {'vs_ip': ip2, 'host_name':'vkvm160083.sqa.cm6', 'host': 'vkvm160083.sqa.cm6'}}
    conf['pool'] = {'WT_BJ_Pool':  {'rr_ldns_limit': 1,'vs': [('vs1', 10)]},
                    '!WT_BJ_Pool': {'rr_ldns_limit': 1,'vs': [('vs2', 10)]}}
    conf['region']={'WT_BJ_Region': {'range':[("192.168.1.1", "192.168.1.1")], 'pool': [('WT_BJ_Pool', 100)]},
                    'WT_SH_Region': {'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100)]}, 
                    '!WT_BJ_Region': {'complename': ('WT_BJ_Region', '!WT_BJ_Region'), 'pool': [('!WT_BJ_Pool', 200)]},}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool', '!WT_BJ_Pool']}}
    check = { 'an_rdata': [(ip2, 1)], 'ancount': 1, 'total_rdata': 100}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_CompleRegion_NotMatched_304():
    conf['pool'] = {'WT_BJ_Pool':  {'rr_ldns_limit': 1,'vs': [('vs1', 10)]},
                    '!WT_BJ_Pool': {'rr_ldns_limit': 1,'vs': [('vs2', 10)]}}
    conf['region']={'WT_BJ_Region': {'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100)]},
                    '!WT_BJ_Region': {'complename': ('WT_BJ_Region', '!WT_BJ_Region'), 'pool': [('!WT_BJ_Pool', 100)]},}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool', '!WT_BJ_Pool']}}
    check = { 'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 100}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 100)
    logger.debug("# Test # Test finished and result check successful...\n")


def test_CompleRegion_MatchedMultiPools_305():
    conf['pool'] = {'WT_BJ_Pool':  {'rr_ldns_limit': 1, 'vs': [('vs1', 10)]},
                    '!WT_BJ_Pool2': {'rr_ldns_limit': 1,'vs': [('vs2', 10)]},
                    '!WT_BJ_Pool3': {'rr_ldns_limit': 1,'vs': [('vs3', 10)]},
                    '!WT_BJ_Pool4': {'in_use': 0,       'vs': [('vs1', 10)]},
                    '!WT_BJ_Pool5': {'available': 0,    'vs': [('vs1', 10)]},}
    conf['region']={'WT_BJ_Region': {'range':[("192.168.1.1", "192.168.1.1")], 'pool': [('WT_BJ_Pool', 100)]},
                    'WT_SH_Region': {'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100)]},
                    '!WT_BJ_Region': {'complename': ('WT_BJ_Region', '!WT_BJ_Region'), 'pool': [('!WT_BJ_Pool2', 700), ('!WT_BJ_Pool3', 800), ('!WT_BJ_Pool4', 900), ('!WT_BJ_Pool5', 900)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool', '!WT_BJ_Pool2', '!WT_BJ_Pool3', '!WT_BJ_Pool4', '!WT_BJ_Pool5']}}

    check = { 'an_rdata': [(ip3, 1)], 'ancount': 1, 'total_rdata': 100}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)


def test_MultiCompleRegion_MatchedMultiPools_306():
    conf['pool'] = {'WT_BJ_Pool':   {'vs': [('vs1', 10)]},
                    '!WT_BJ_Pool2': {'vs': [('vs2', 10)]},
                    '!WT_BJ_Pool3': {'vs': [('vs3', 10)]},
                    '!WT_BJ_Pool4': {'vs': [('vs1', 10)]},
                    '!WT_BJ_Pool5': {'vs': [('vs1', 10)]}}
    conf['region']={'WT_BJ_Region': {'range':[("192.168.1.1", "192.168.1.1")], 'pool': [('WT_BJ_Pool', 1000)]},
                    'WT_TJ_Region': {'range':[("192.168.1.1", "192.168.1.1")], 'pool': [('WT_BJ_Pool', 1000)]},
                    'WT_SH_Region': {'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100)]},
                    'WT_HN_Region': {'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100)]},
                    '!WT_BJ_Region': {'complename': ('WT_BJ_Region', '!WT_BJ_Region'),'pool': [('!WT_BJ_Pool2', 700), ('!WT_BJ_Pool4', 600), ('!WT_BJ_Pool5', 100)]},
                    '!WT_TJ_Region': {'complename': ('WT_TJ_Region', '!WT_TJ_Region'),'pool': [('!WT_BJ_Pool2', 700), ('!WT_BJ_Pool3', 700), ('!WT_BJ_Pool5', 100)]} }
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool', '!WT_BJ_Pool2', '!WT_BJ_Pool3', '!WT_BJ_Pool4', '!WT_BJ_Pool5']}}
    check = { 'an_rdata': [(ip2, 0.5), (ip3, 0.5)], 'ancount': 1, 'total_rdata': 400}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 400)
    logger.debug(elog)


def test_Region_BigRegion_BigRegion_307():
    conf['pool'] = {'Pool1': {'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'ttl':600, 'vs': [('vs3', 1)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100)]},
                    'WT_Region': {'childregion': ['Region1'], 'pool': [('Pool2', 200)]},
                    'DX_Region': {'childregion': ['Region1', 'WT_Region'],'pool': [('Pool3', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool1', 'Pool2', 'Pool3']}}
    check = { 'an_rdata': [(ip3, 1)], 'ancount': 1, 'total_rdata': 200}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 200)
    logger.debug(elog)

def test_Topology_Wideip_NoIntersection_308():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs3', 1)]},
                    'Pool2': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 2)]},
                    'Pool3': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs1', 3)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs2', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pri': 1, 'pool': [('Pool1', 100), ('Pool2', 200)]},
                    'Region2': {'range':[(laddr, laddr)], 'pri': 2, 'pool': [('Pool3', 100), ('Pool4', 300)]},
                    'WT_Region': {'childregion': ['Region1']},
                    'DX_Region': {'childregion': ['Region2']}}
    conf['wideip']={'wideip1': {'pool': ['Pool5']}}
    check = { 'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 100}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_TopologyEmpty_WideipNotEmpty_309():
    conf['pool'] = {'WT_BJ_Pool': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 1)]},
                    'WT_TJ_Pool': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 2)]},
                    'WT_Pool':    {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs3', 3)]}}
    conf['region']={'WT_BJ_Region': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 200)]},
                    'WT_Region': {'childregion': ['WT_BJ_Region']}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool', 'WT_TJ_Pool', 'WT_Pool']}}
    check = { 'an_rdata': [(ip1, 0.33), (ip2, 0.33), (ip3, 0.33)], 'ancount': 1, 'total_rdata': 1000}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 1000)
    logger.debug(elog)


def test_WideipEmpty_TopologyNotEmpty_310():
    conf['pool'] = {'WT_BJ_Pool': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 1)]},
                    'WT_TJ_Pool': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 2)]},
                    'WT_Pool':    {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs1', 3), ('vs2', 3), ('vs3', 3)]}}
    conf['region']={'WT_BJ_Region': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 200)]},
                    'WT_Region': {'childregion': ['WT_BJ_Region']}}
    conf['wideip']={'wideip1': {'pool': []}}
    check = { 'ancount': 0, 'nscount': 1}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_Topology_Wideip_ParticalIntersection_311():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs3', 1)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 200), ('Pool3', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool2', 'Pool3', 'Pool4', 'Pool5']}}
    check = { 'an_rdata': [(ip3, 1)], 'ancount': 1, 'total_rdata': 100}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

def test_Topology_Wideip_ParticalIntersection_top2_312():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs3', 1)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs2', 1)]},
                    'Pool6': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs3', 2)]},
                    'Pool7': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1)]},
                    'Pool8': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs2', 2)]},
                    'Pool9': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs3', 2)]},
                    'Pool10':{'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 200), ('Pool3', 200), ('Pool4', 200), ('Pool5', 200), ('Pool6', 200), ('Pool7', 200), ('Pool8', 200), ('Pool9', 200), ('Pool10', 200)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool2', 'Pool3', 'Pool4', 'Pool5', 'Pool6', 'Pool7', 'Pool8', 'Pool9', 'Pool10']}}
    check = { 'an_rdata': [(ip1, 0.33), (ip2, 0.33), (ip3, 0.33)], 'ancount': 1, 'total_rdata': 1000}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 1000)
    logger.debug(elog)

# NoError -- rcode = 0
def test_Wideip_NotUseful_Pool_313():
    conf['vs']={'vs1': {'vs_ip': ip1, 'in_use':0, 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6'},
                'vs2': {'vs_ip': ip2, 'in_use':0, 'host_name':'vkvm160083.sqa.cm6', 'host': 'vkvm160083.sqa.cm6'},
                'vs3': {'vs_ip': ip3, 'in_use':0, 'host_name':'vkvm160093.sqa.cm6', 'host': 'vkvm160093.sqa.cm6'}}
    conf['pool'] = {'WT_BJ_Pool': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 1)]},
                    'WT_TJ_Pool': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 2)]},
                    'WT_Pool': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs3', 3)]}}
    conf['region']={'WT_BJ_Region': {'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100)]},
                    'WT_Region': {'childregion': ['WT_BJ_Region'], 'pool':[('WT_TJ_Pool', 1), ('WT_Pool', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool', 'WT_TJ_Pool', 'WT_Pool']}}
    check = { 'ancount': 0, 'nscount':1, 'rcode':0}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_NotChooseDisabledPool_314():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'in_use':0, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'available':0, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs3', 1)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 100), ('Pool3', 100)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool1', 'Pool2', 'Pool3', 'Pool4', 'Pool5']}}
    check = { 'an_rdata': [(ip3, 1)], 'ancount': 1, 'total_rdata': 100 }
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 100)
    logger.debug(elog)

# NXDOMAIN -- rcode = 3
def test_Wideip_Disabled_315():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs3', 1)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 100), ('Pool3', 100)]}}
    conf['wideip']={'wideip1': {'in_use':0, 'pool': ['Pool1', 'Pool2', 'Pool3', 'Pool4', 'Pool5']}}
    check = { 'ancount': 0, 'nscount':1, 'rcode':3}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_NoAvailablePool_316():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'in_use':0, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'in_use':0, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':3, 'in_use':0, 'ttl':600, 'vs': [('vs3', 1)]},
                    'Pool4': {'rr_ldns_limit':1, 'available':0, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'in_use':0, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 100), ('Pool3', 100)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool1', 'Pool2', 'Pool3']}}
    check = { 'ancount': 0, 'nscount':1, 'rcode':3}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_AvailablePool_ClientIPNoRegionMatched_317():
    conf['pool'] = {'WT_BJ_Pool': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 10)]},
                    'WT_BJ_Pool2':{'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 20)]}}
    conf['region']={'WT_BJ_Region': {'range':[("192.168.1.1","192.168.1.1"),("192.168.1.2","192.168.1.2")],'pool':[('Pool1', 100)]},
                    'Region1': {'range':[(laddr, laddr)], 'pool': []}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool', 'WT_BJ_Pool2']}}
    check = { 'an_rdata': [(ip1, 0.5), (ip2, 0.5)]}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 500)
    logger.debug(elog)

def test_WideipDisabled_PoolDisabled_318():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'in_use':0, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'in_use':0, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':3, 'in_use':0, 'ttl':600, 'vs': [('vs3', 1)]},
                    'Pool4': {'rr_ldns_limit':1, 'in_use':0, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'in_use':0, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 100), ('Pool3', 100)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool1', 'Pool2', 'Pool3', 'Pool4', 'Pool5']}}
    check = { 'ancount': 0, 'nscount':1, 'rcode':3}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_WideipDisabled_PoolEnabled_319():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs3', 1)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 100), ('Pool3', 100)]}}
    conf['wideip']={'wideip1': {'in_use':0, 'pool': ['Pool1', 'Pool2', 'Pool3', 'Pool4', 'Pool5']}}
    check = { 'ancount': 0, 'nscount':1, 'rcode':3}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)

def test_Wideip_NotFound_ReturnEmpty_320():
    conf['pool'] = {'WT_BJ_Pool': {'rr_ldns_limit':1, 'vs': [('vs1', 10), ('vs2', 20), ('vs3', 50)]}}
    conf['region']={'WT_BJ_Region': {'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool']}}
    dns  = {'qd':[{'qd_qname':'img01.taobaocdn.com'}] }
    check = { 'ancount': 0, 'qdcount':1, 'rcode':5}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 10)
    logger.debug(elog)


def test_CName_Pool_A_321():
    url1 = 'img.img01.taobaocdn.com.danuoyi.tbcache.com'
    conf['vs']={'vs1': {'vs_ip': ip1, 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6'}}
    conf['pool'] = {'WT_BJ_Pool': {'QueryType':'CName', 'value':'img.img01.taobaocdn.com.danuoyi.tbcache.com'},
                   'WT_BJ_Pool2': {'vs': [('vs1', 1)]}}
    conf['region']={'WT_BJ_Region': {'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool']},
                    'wideip2': {'url':url1, 'pool': ['WT_BJ_Pool2']}}
    check = { 'an_rdata': [(ip1, 0.5), (url1, 0.5)], 'ancount': 2, 'total_rdata': 400}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 200)
    logger.debug(elog)


# CNAME is 5, 
def test_CName_Pool_CName_322():
    url1 = 'cname.taobaocdn.com.danuoyi.tbcache.com'
    conf['vs']={'vs1': {'vs_ip': ip1, 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6'}}
    conf['pool'] = {'WT_BJ_Pool': {'QueryType':'CName', 'value':url1},
                    'WT_BJ_HD_Pool': {'vs': [('vs1', 1)]}}
    conf['region']={'WT_BJ_Region': {'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100), ('WT_BJ_HD_Pool', 100)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool']},
                    'wideip2': {'url':url1, 'pool': ['WT_BJ_HD_Pool']}}
    dns  = {'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com', 'qd_qtype':5}] }
    check = { 'an_rdata': [(url1, 1)], 'ancount': 1, 'total_rdata': 20}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 20)
    check = { 'an_rdata': [(ip1, 0.5), (url1, 0.5)], 'ancount': 2, 'total_rdata': 40}
    dns  = {'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com'}] }
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 20)
    logger.debug(elog)

def test_Wideip_NoUseful_Pool_323():
    conf['vs']={'vs1': {'vs_ip': ip1, 'available':0, 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6'},
                'vs2': {'vs_ip': ip2, 'available':0, 'host_name':'vkvm160083.sqa.cm6', 'host': 'vkvm160083.sqa.cm6'},
                'vs3': {'vs_ip': ip3, 'available':0, 'host_name':'vkvm160093.sqa.cm6', 'host': 'vkvm160093.sqa.cm6'}}
    conf['pool'] = {'WT_BJ_Pool': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 1)]},
                    'WT_TJ_Pool': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 2)]},
                    'WT_Pool': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs3', 3)]}}

    conf['region']={'WT_BJ_Region':{'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100)]},
                    'WT_Region': {'childregion':['WT_BJ_Region'], 'pool': [('WT_TJ_Pool', 1), ('WT_Pool', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool', 'WT_TJ_Pool', 'WT_Pool']}}
    check = { 'an_rdata': [(ip3, 1)], 'ancount': 1, 'total_rdata': 20}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 20)
    logger.debug(elog)

def test_IP_BigRegion_MultiPool_324():
    conf['pool'] = {'WT_BJ_Pool': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 1)]},
                    'WT_TJ_Pool': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 2)]},
                    'WT_Pool': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs3', 3)]}}
    conf['region']={'WT_BJ_Region':{'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100)]},
                    'WT_Region': {'childregion':['WT_BJ_Region'], 'pool': [('WT_TJ_Pool', 1), ('WT_Pool', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool', 'WT_TJ_Pool', 'WT_Pool']}}
    check = { 'an_rdata': [(ip3, 1)], 'ancount': 1, 'total_rdata': 20}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 20)
    logger.debug(elog)

def test_IP_MultiBigRegion_325():
    conf['pool'] = {'WT_BJ_Pool': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 1)]},
                    'WT_TJ_Pool': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 2)]},
                    'WT_Pool': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs3', 3)]},
                    'WT_SH_Pool': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs3', 3)]},
                    'WT_HN_Pool': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 3), ('vs2', 3), ('vs3', 3)]}}
    conf['region']={'WT_BJ_Region':{'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100)]},
                    'WT_Region': {'childregion':['WT_BJ_Region'], 'pool': [('WT_TJ_Pool', 1), ('WT_Pool', 300)]},
                    'WT_Region2':{'childregion':['WT_BJ_Region'], 'pool': [('WT_SH_Pool', 1), ('WT_HN_Pool', 1000)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool', 'WT_TJ_Pool', 'WT_Pool', 'WT_SH_Pool', 'WT_HN_Pool']}}
    check = { 'an_rdata': [(ip1, 0.33), (ip2, 0.33), (ip3, 0.33)], 'ancount': '>=1'}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 1000)
    logger.debug(elog)

def test_ExpectedVSCountMoreThanActualVSCount_326():
    conf['pool'] = {'WT_BJ_Pool': {'rr_ldns_limit':100, 'vs': [('vs1', 10)]}}
    conf['region']={'WT_BJ_Region':{'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool']}}
    check = { 'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 20}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 20)
    logger.debug(elog)

def test_CName_Pool_A_327():
    conf['vs']={'vs1': {'vs_ip': ip1, 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6'}}
    conf['pool'] = {'WT_BJ_Pool': {'rr_ldns_limit':1,'ttl':300,'QueryType':'CName','value':'img01.taobaocdn.com.danuoyi.tbcache.com'},
                    'WT_BJ_Pool2':{'rr_ldns_limit':2,'ttl':400, 'vs': [('vs1', 1)]}}
    conf['region']={'WT_BJ_Region':{'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100), ('WT_BJ_Pool2', 200)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool', 'WT_BJ_Pool2']}}
    check = { 'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 20}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 20)
    logger.debug(elog)

def test_Response_CName_With_CName_Pool_328():
    url1 = 'cname1.taobaocdn.com.danuoyi.tbcache.com'
    url2 = 'cname2.taobaocdn.com.danuoyi.tbcache.com'
    conf['pool'] = {'WT_BJ_Pool':{'rr_ldns_limit':1,'ttl':300,'QueryType':'CName','value':url1},
                    'WT_TJ_Pool':{'rr_ldns_limit':2,'ttl':400,'QueryType':'CName','value':url2},
                    'WT_Pool': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs3', 3)]}}
    conf['region']={'WT_BJ_Region':{'range':[(laddr, laddr)], 'pool': [('WT_BJ_Pool', 100), ('WT_TJ_Pool', 100), ('WT_Pool', 100)]},
                    'WT_Region':{'childregion':['WT_BJ_Region'], 'pool': [('WT_TJ_Pool', 1),('WT_Pool', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Pool']},
                    'wideip2': {'url':url1, 'pool': ['WT_TJ_Pool']},
                    'wideip3': {'url':url2, 'pool': ['WT_Pool']}}
    check = { 'an_rdata': [(ip3, 0.33), (url1, 0.33), (url2, 0.33)], 'ancount': 3, 'total_rdata': 60}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 20)
    logger.debug(elog)

def test_Topology_Wideip_OnlyOneAvailable_329():
    conf['vs']={'vs1': {'vs_ip': ip1, 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6'},
                'vs2': {'vs_ip': ip2, 'in_use':0, 'host_name':'vkvm160083.sqa.cm6', 'host': 'vkvm160083.sqa.cm6'},
                'vs3': {'vs_ip': ip3, 'available':0, 'host_name':'vkvm160093.sqa.cm6', 'host': 'vkvm160093.sqa.cm6'}}
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs1', 1), ('vs2', 1), ('vs3', 1)]},
                    'Pool3': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 0), ('vs3', 1000)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 200), ('Pool3', 200)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool2', 'Pool3', 'Pool4', 'Pool5']}}
    check = { 'an_rdata': [(ip1, 1)], 'ancount': 1, 'total_rdata': 20}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 20)
    logger.debug(elog)

def test_Ratio_NoVSAvailable_330():
    conf['vs']={'vs1': {'vs_ip': ip1, 'available':0, 'host_name':'vkvm160073.sqa.cm6', 'host': 'vkvm160073.sqa.cm6'},
                'vs2': {'vs_ip': ip2, 'available':0, 'host_name':'vkvm160083.sqa.cm6', 'host': 'vkvm160083.sqa.cm6'},
                'vs3': {'vs_ip': ip3, 'available':0, 'host_name':'vkvm160093.sqa.cm6', 'host': 'vkvm160093.sqa.cm6'}}
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 1), ('vs3', 1)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 200), ('Pool3', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool2', 'Pool3', 'Pool4', 'Pool5']}}
    check = { 'an_rdata': [(ip1, 0.33), (ip2, 0.33), (ip3, 0.33)], 'ancount': '>=1'}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 1000)
    logger.debug(elog)

def test_Ratio_OneVS_RatioEqual_331():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 1), ('vs3', 1)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 200), ('Pool3', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool2', 'Pool3', 'Pool4', 'Pool5']}}
    check = { 'an_rdata': [(ip1, 0.33), (ip2, 0.33), (ip3, 0.33)], 'ancount': '>=1'}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 1000)
    logger.debug(elog)

def test_Ratio_TwoVS_RatioEqual_332():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 30), ('vs2', 30), ('vs3', 30)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 200), ('Pool3', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool2', 'Pool3', 'Pool4', 'Pool5']}}
    check = { 'an_rdata': [(ip1, 0.33), (ip2, 0.33), (ip3, 0.33)], 'ancount': '>=1'}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 1000)
    logger.debug(elog)

def test_Ratio_TwoVS_RatioNotEqual_333():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1000), ('vs2', 1), ('vs3', 201)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 200), ('Pool3', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool2', 'Pool3', 'Pool4', 'Pool5']}}
    check = { 'an_rdata': [(ip1, 0.82), (ip2, 0.01), (ip3, 0.17)], 'ancount': '>=1'}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 1000)
    logger.debug(elog)

def test_Ratio_ThreeVS_RatioNotEqual_334():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs1', 300), ('vs2', 300), ('vs3', 300)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 200), ('Pool3', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool2', 'Pool3', 'Pool4', 'Pool5']}}
    check = { 'an_rdata': [(ip1, 0.33), (ip2, 0.33), (ip3, 0.33)], 'ancount': '1|2|3', 'total_rdata': 3000}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 1000)
    logger.debug(elog)

def test_Ratio_TenVS_RatioNotEqual_335():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':10,'ttl':600, 'vs': [('vs1', 200), ('vs2', 100), ('vs3', 300)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 200), ('Pool3', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool2', 'Pool3', 'Pool4', 'Pool5']}}
    check = { 'an_rdata': [(ip1, 0.33), (ip2, 0.3), (ip3, 0.37)], 'ancount': '1|2|3', 'total_rdata': '<3000'}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 1000)
    logger.debug(elog)

def test_NoDuplicatedVSReturned_336():
    conf['pool'] = {'Pool1': {'rr_ldns_limit':1, 'ttl':300, 'vs': [('vs1', 2)]},
                    'Pool2': {'rr_ldns_limit':2, 'ttl':400, 'vs': [('vs2', 1)]},
                    'Pool3': {'rr_ldns_limit':3, 'ttl':600, 'vs': [('vs1', 300), ('vs2', 300), ('vs3', 300)]},
                    'Pool4': {'rr_ldns_limit':1, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]},
                    'Pool5': {'rr_ldns_limit':2, 'ttl':600, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'Region1': {'range':[(laddr, laddr)], 'pool': [('Pool1', 100), ('Pool2', 200), ('Pool3', 300)]}}
    conf['wideip']={'wideip1': {'pool': ['Pool2', 'Pool3', 'Pool4', 'Pool5']}}
    check = { 'an_rdata': [(ip1, 0.33), (ip2, 0.33), (ip3, 0.33)], 'ancount': 3, 'total_rdata': 3}
    pharos.deploy(conf)
    for i in range(0,10):
        DNS.do_dns(dns, check, 1)
    logger.debug(elog)

def test_Pool_Limit_Equalto_VS_337():
    conf['pool'] = {'WT_BJ_Poo1': {'rr_ldns_limit':3, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 5)]}}
    conf['region']={'WT_BJ_Region': {'range':[(laddr, laddr)], 'pool': [('WT_BJ_Poo1', 100)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Poo1']}}
    check = { 'an_rdata': [(ip1, 0.33), (ip2, 0.33), (ip3, 0.33)], 'ancount': 3, 'total_rdata': 3}
    pharos.deploy(conf)
    for i in range(0,10):
        DNS.do_dns(dns, check, 1)
    logger.debug(elog)

def test_Pool_Limit_Equalto_VS_Same_Pri_338():
    conf['pool'] = {'WT_BJ_Poo1': {'rr_ldns_limit':3, 'vs': [('vs1', 1), ('vs2', 1), ('vs3', 1)]}}
    conf['region']={'WT_BJ_Region': {'range':[(laddr, laddr)], 'pool': [('WT_BJ_Poo1', 100)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Poo1']}}
    check = { 'an_rdata': [(ip1, 0.33), (ip2, 0.33), (ip3, 0.33)], 'ancount': 3, 'total_rdata': 3}
    pharos.deploy(conf)
    for i in range(0,10):
        DNS.do_dns(dns, check, 1)
    logger.debug(elog)

def test_Pool_Limit_NoEqual_VS_339():
    conf['pool'] = {'WT_BJ_Poo1': {'rr_ldns_limit':3, 'vs': [('vs1', 1), ('vs2', 2), ('vs3', 3)]}}
    conf['region']={'WT_BJ_Region': {'range':[(laddr, laddr)], 'pool': [('WT_BJ_Poo1', 100)]}}
    conf['wideip']={'wideip1': {'pool': ['WT_BJ_Poo1']}}
    check = { 'an_rdata': [(ip1, 0.3), (ip2, 0.33), (ip3, 0.36)], 'ancount': '1|2|3'}
    pharos.deploy(conf)
    DNS.do_dns(dns, check, 1000)
    logger.debug(elog)




