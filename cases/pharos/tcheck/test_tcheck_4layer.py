import pytest, time
import src.deploy.tcheck    as tcheck
import src.util.system_util as system_util
from   src.util.logger      import logger
from  src.deploy            import TCHECK, VS
conf = {}

def setup_module(module):
    logger.debug("# Test # Setup Module:%s" % module.__name__)
    tcheck.start_check()
def teardown_module(module):
    logger.debug("# Test # Teardown Module:%s" % module.__name__)
def setup_function(function):
    logger.debug("# Test # Setup Function:%s" % function.__name__)
    global conf
    conf = {
      'tcheck':{'master': 'master', 'slave':['slave1','slave2','slave3']},
      'vs':{'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6'},
            'vs2': {'vs_ip': '10.235.160.76', 'host_name':'vkvm160076.sqa.cm6'},
            'vs3': {'vs_ip': '10.235.160.86', 'host_name':'vkvm160086.sqa.cm6'}},
    }
def teardown_function(function):
    logger.debug("# Test # Teardown Function:%s" % function.__name__)


# 1 tcheck, 1 vs, 1 vs down
def test_1tcheck_1vs_down_01():
    conf['tcheck'] = {'master': 'master','slave':['slave1']}
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6'}}
    tcheck.deploy(conf)

    tcheck.stop_vs(['vs1'])
    tcheck.check_db([('vs1', 0)])

    tcheck.start_vs(['vs1'])
    tcheck.check_db([('vs1', 1)])
    logger.debug("# Test # test stopped and success!!!")

# 1 tcheck, 3 vs, 1 vs down
def test_1tcheck_3vs_1down_02():
    conf['tcheck'] = {'master': 'master','slave' :['slave1']}
    tcheck.deploy(conf)

    tcheck.stop_vs(['vs1'])
    tcheck.check_db([('vs1', 0), ('vs2', 1), ('vs3', 1)])

    tcheck.start_vs(['vs1'])
    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")

# 1 tcheck, 3 vs, 2 vs down
def test_1tcheck_3vs_2down_03():
    conf['tcheck'] = {'master': 'master','slave' :['slave1']}
    tcheck.deploy(conf)

    tcheck.stop_vs(['vs2', 'vs3'])
    tcheck.check_db([('vs1', 1), ('vs2', 0), ('vs3', 0)])

    tcheck.start_vs(['vs2', 'vs3'])
    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")


# 1 tcheck, 3 vs, 3 vs down
def test_1tcheck_3vs_3down_04():
    conf['tcheck'] = {'master': 'master','slave' :['slave1']}
    tcheck.deploy(conf)

    tcheck.stop_vs(['vs1', 'vs2', 'vs3'])
    tcheck.check_db([('vs1', 0), ('vs2', 0), ('vs3', 0)])

    tcheck.start_vs(['vs1', 'vs2', 'vs3'])
    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)], 70)
    logger.debug("# Test # test stopped and success!!!")


# 3 tcheck, 1 vs, 1 vs down
def test_3tcheck_1vs_1down_05():
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6'}}
    tcheck.deploy(conf)

    tcheck.stop_vs(['vs1'])
    tcheck.check_db([('vs1', 0)])

    tcheck.start_vs(['vs1'])
    tcheck.check_db([('vs1', 1)])
    logger.debug("# Test # test stopped and success!!!")


# 3 tcheck, 3 vs, 1 vs down
def test_3tcheck_3vs_1down_06():
    tcheck.deploy(conf)

    tcheck.stop_vs(['vs1'])
    tcheck.check_db([('vs1', 0), ('vs2', 1), ('vs3', 1)])

    tcheck.start_vs(['vs1'])
    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")

# 3 tcheck, 3 vs, 2 vs down
def test_3tcheck_3vs_2down_07():
    tcheck.deploy(conf)

    tcheck.stop_vs(['vs1', 'vs2'])
    tcheck.check_db([('vs1', 0), ('vs2', 0), ('vs3', 1)])

    tcheck.start_vs(['vs1', 'vs2'])
    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")

# 3 tcheck, 3 vs, 3 vs down
def test_3tcheck_3vs_3down_08():
    tcheck.deploy(conf)

    tcheck.stop_vs(['vs1', 'vs2', 'vs3'])
    tcheck.check_db([('vs1', 0), ('vs2', 0), ('vs3', 0)])

    tcheck.start_vs(['vs1', 'vs2', 'vs3'])
    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")


# 3 tcheck, 3 vs, 1 vs down, 1 tcheck ok
def test_3tcheck_3vs_1down_1TCOK_09():
    tcheck.deploy(conf)
    tcheck.stop_tcheck(['slave2', 'slave3'])

    tcheck.stop_vs(['vs1'])
    tcheck.sleep(60)
    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)])

    tcheck.start_vs(['vs1'])
    tcheck.sleep(60)
    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")

# 3 tcheck, 3 vs, 1 vs down, 1 tcheck ok
def test_3tcheck_3vs_1down_2TCOK_10():
    tcheck.deploy(conf)
    tcheck.stop_tcheck(['slave3'])

    tcheck.stop_vs(['vs1'])
    tcheck.check_db([('vs1', 0), ('vs2', 1), ('vs3', 1)])

    tcheck.start_vs(['vs1'])
    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")


# 3 tcheck, itvl=10, timeout=10, retries=2, 3 sec start
def test_3tcheck_10itvl_3start_11():
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6', \
                          'itvl': 60, 'timeout':10, 'retries':2}}
    tcheck.deploy(conf)

    tcheck.stop_vs(['vs1'])
    tcheck.check_db([('vs1', 1)])

    tcheck.start_vs(['vs1'])
    tcheck.check_db([('vs1', 1)])
    logger.debug("# Test # test stopped and success!!!")


# 3 tcheck, itvl=60, timeout=5, retries=2, 15 sec start
def test_3tcheck_60itvl_15start_12():
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6', \
                          'itvl': 60, 'timeout':5, 'retries':2}}
    tcheck.deploy(conf)

    tcheck.stop_vs(['vs1'])
    tcheck.sleep(15)
    
    tcheck.start_vs(['vs1'])
    tcheck.check_db([('vs1', 0), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")

# 3 tcheck, 1 vs, 1 vs down, itvl=10, timeout=10, retries=2
def test_3tcheck_itvl10_to10_13():
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6', \
                          'itvl': 10, 'timeout':10, 'retries':2}}
    tcheck.deploy(conf)

    tcheck.stop_vs(['vs1'])
    tcheck.sleep(10)
    # at 10 sec
    tcheck.check_vs([('vs1', 0), ('vs2', 1), ('vs3', 1)])

    tcheck.sleep(5)
    # at 15 sec
    tcheck.start_vs(['vs1'])
    tcheck.check_vs([('vs1', 0), ('vs2', 1), ('vs3', 1)])

    # at 20 sec
    tcheck.sleep(5)
    tcheck.check_vs([('vs1', 0), ('vs2', 1), ('vs3', 1)])

    # at 25 sec
    tcheck.sleep(5)
    tcheck.check_vs([('vs1', 0), ('vs2', 1), ('vs3', 1)])

    # at 30 sec
    tcheck.sleep(5)
    tcheck.check_vs([('vs1', 0), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")



