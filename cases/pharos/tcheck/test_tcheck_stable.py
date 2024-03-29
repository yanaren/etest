import pytest, time
import src.deploy.tcheck    as tcheck
import src.util.system_util as system_util
from   src.util.logger      import logger
from  src.deploy            import TCHECK, VS
conf = {}

def setup_module(module):
    print ("setup_module:%s" % module.__name__)
    tcheck.start_check()
def teardown_module(module):
    print ("teardown_module:%s" % module.__name__)
def setup_function(function):
    print ("setup_function:%s" % function.__name__)
    global conf
    conf = {
      'tcheck':{'master': 'master', 'slave':['slave1','slave2','slave3']},
      'vs':{'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6'},
            'vs2': {'vs_ip': '10.235.160.76', 'host_name':'vkvm160076.sqa.cm6'},
            'vs3': {'vs_ip': '10.235.160.86', 'host_name':'vkvm160086.sqa.cm6'}},
    }
def teardown_function(function):
    print ("teardown_function:%s" % function.__name__)


# 3 tcheck, 1 vs, master down
def test_3tcheck_1vs_masterdown_01():
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6'}}
    tcheck.deploy(conf)

    tcheck.stop_tcheck(['master'])
    tcheck.stop_vs(['vs1'])

    tcheck.sleep(90)
    tcheck.check_db([('vs1', 1)])
    logger.debug("# Test # test stopped and success!!!")

# 1 tcheck, 1 vs, 1 slave down
def test_1tcheck_1vs_1slavedown_02():
#def tcheck_1vs_1slavedown_02():
    conf['tcheck'] = {'master': 'master', 'slave': ['slave1']}
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6'}}
    tcheck.deploy(conf)

    tcheck.stop_tcheck(['slave1'])
    tcheck.stop_vs(['vs1'])
    tcheck.sleep(90)
    tcheck.check_db([('vs1', 1)])
    logger.debug("# Test # test stopped and success!!!")


# 3 tcheck, 1 vs, 1 slave down
def test_3tcheck_1vs_1slavedown_03():
    conf['tcheck'] = {'master': 'master','slave' :['slave1', 'slave2', 'slave3']}
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6'}}
    tcheck.deploy(conf)

    tcheck.stop_tcheck(['slave1'])
    tcheck.stop_vs(['vs1'])
    tcheck.check_db([('vs1', 0)])
    logger.debug("# Test # test stopped and success!!!")

# 3 tcheck, 1 vs, 2 slave down
def test_3tcheck_1vs_2slavedown_04():
    conf['tcheck'] = {'master': 'master','slave' :['slave1', 'slave2', 'slave3']}
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6'}}
    tcheck.deploy(conf)

    tcheck.stop_tcheck(['slave1', 'slave2'])
    tcheck.stop_vs(['vs1'])
    tcheck.sleep(90)
    tcheck.check_db([('vs1', 1)])
    logger.debug("# Test # test stopped and success!!!")

# 3 tcheck, 1 vs, 3 slave down
def test_3tcheck_1vs_3slavedown_05():
    conf['tcheck'] = {'master': 'master','slave' :['slave1', 'slave2', 'slave3']}
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6'}}
    tcheck.deploy(conf)

    tcheck.stop_tcheck(['slave1', 'slave2', 'slave3'])
    tcheck.stop_vs(['vs1'])
    tcheck.sleep(90)
    tcheck.check_db([('vs1', 1)])
    logger.debug("# Test # test stopped and success!!!")

# 1 host, 3 uri, should give warning.
#def test_tcheck_1host_3uri_06():
#    conf['tcheck'] = {'master': 'master','slave':['slave1', 'slave2', 'slave3']}
#    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11; /12; /13;'}}
#    tcheck.deploy(conf)
#
#    tcheck.check_db([('vs1', 0)])
#    logger.debug("# Test # test stopped and success!!!")

# 3 host, 1 uri, should give warning.
def test_tcheck_3host_1uri_07():
    conf['tcheck'] = {'master': 'master','slave':['slave1', 'slave2', 'slave3']}
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 0)])
    logger.debug("# Test # test stopped and success!!!")

# 3 host, 2 uri, should give warning.
def test_tcheck_3host_2uri_08():
    conf['tcheck'] = {'master': 'master','slave':['slave1', 'slave2', 'slave3']}
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11; /12;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 0)])
    logger.debug("# Test # test stopped and success!!!")

# 3 tcheck, 1 vs, tcheck restart 100 time
def test_tcheck_restart_100times_09():
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6'}}
    tcheck.deploy(conf)

    for i in range(0, 100):
        tcheck.stop_all_tcheck()
        tcheck.start_all_tcheck()

    tcheck.stop_vs(['vs1'])
    tcheck.check_db([('vs1', 0)])
    logger.debug("# Test # test stopped and success!!!")


# stable run in long time
def test_tcheck_long_run_10():
#def tcheck_long_run_10():
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/1; /2; /3;'},
                'vs2': {'vs_ip': '10.235.160.76', 'host_name':'vkvm160076.sqa.cm6; vkvm160076.sqa.cm6; vkvm160076.sqa.cm6;', 'HC_type':1, 'url': '/1; /2; /3;'},
                'vs3': {'vs_ip': '10.235.160.86', 'host_name':'vkvm160086.sqa.cm6; vkvm160086.sqa.cm6; vkvm160086.sqa.cm6;', 'HC_type':1, 'url': '/1; /2; /3;'}}
    tcheck.deploy(conf)
    
    start_time = time.time()
    for i in range(1, 300):
        tcheck.stop_vs(['vs1'])
        tcheck.check_db([('vs1', 0)])
        tcheck.start_vs(['vs1'])
        tcheck.check_db([('vs1', 1)])
    used_time = time.time() - start_time
    log_in = 'vs1(10.235.160.66) restart for 100 times and check 200 times, using time: ' + str(used_time) + ' seconds'
    logger.debug(log_in)
    logger.debug("# Test # test stopped and success!!!")


