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
      'tcheck':{'master': 'master',
                'slave' :['slave1','slave2','slave3']},
      'vs'    :{'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6'},
                'vs2': {'vs_ip': '10.235.160.76', 'host_name':'vkvm160076.sqa.cm6'},
                'vs3': {'vs_ip': '10.235.160.86', 'host_name':'vkvm160086.sqa.cm6'}},
    }
def teardown_function(function):
    print ("teardown_function:%s" % function.__name__)


# 1 tcheck, 1 vs, 1 vs down
def test_1checker_1server_down_01():
    conf['tcheck'] = {'master': 'master','slave':['slave1']}
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.83', 'host_name':'vkvm160083.sqa.cm6'}}
    tcheck.deploy(conf)

    tcheck.stop_vs(['vs1'])
    tcheck.sleep(30)
    tcheck.check_db([('vs1', 0)])

    tcheck.start_vs(['vs1'])
    tcheck.check_db([('vs1', 1)])
    logger.debug("# Test # test stopped and success!!!")

# 1 tcheck, 3 vs, 1 vs down
def test_1checker_Nserver_1down_02():
    conf['tcheck'] = {'master': 'master','slave' :['slave1']}
    tcheck.deploy(conf)

    tcheck.stop_vs(['vs1'])
    tcheck.check_db([('vs1', 0), ('vs2', 1), ('vs3', 1)])

    tcheck.start_vs(['vs1'])
    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")




