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
    print ''
    logger.debug("# Test # Setup Function:%s" % function.__name__)
    global conf
    conf = {
      'tcheck':{'master':'master','slave':['slave1','slave2','slave3']},
      'vs'    :{'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6;', 'HC_type':1},
                'vs2': {'vs_ip': '10.235.160.76', 'host_name':'vkvm160076.sqa.cm6;', 'HC_type':1},
                'vs3': {'vs_ip': '10.235.160.86', 'host_name':'vkvm160086.sqa.cm6;', 'HC_type':1}},
    }
def teardown_function(function):
    logger.debug("# Test # Teardown Function:%s" % function.__name__)


# 1 tcheck, 1 vs, 1 vs down
def test_1tcheck_1vs_down_01():
    conf['tcheck'] = {'master':'master','slave':['slave1']}
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66','host_name':'vkvm160066.sqa.cm6;','HC_type':1}}
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
    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")


# 3 tcheck, 1 vs, 1 vs down
def test_3tcheck_1vs_1down_05():
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6;', 'HC_type':1}}
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


# 1 tcheck, 1 vs, 1 uri no available
def test_1tcheck_1vs_1uri_1down_09():
    conf['tcheck'] = {'master': 'master','slave':['slave1']}
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 0)])
    logger.debug("# Test # test stopped and success!!!")

# 1 tcheck, 1 vs, 3 uri, 1 uri ok
def test_1tcheck_1vs_1uri_2down_10():
    conf['tcheck'] = {'master': 'master','slave':['slave1']}
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'available':0, 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11; /12; /1;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 1)])
    logger.debug("# Test # test stopped and success!!!")


# 1 tcheck, 1 vs, 3 uri, 3 uri ok
def test_1tcheck_1vs_3uri_0down_11():
    conf['tcheck'] = {'master': 'master','slave':['slave1']}
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'available':0, 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/1; /2; /3;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 1)])
    logger.debug("# Test # test stopped and success!!!")


# 1 tcheck, 1 vs, 3 uri, 3 unavailable
def test_1tcheck_1vs_3uri_3down_12():
    conf['tcheck'] = {'master': 'master','slave':['slave1']}
    conf['vs'] = {'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11; /12; /13;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 0)])
    logger.debug("# Test # test stopped and success!!!")

# 1 tcheck, 3 vs, 1 uri, all 1 unavailable
def test_1tcheck_3vs_1uri_1down_13():
    conf['tcheck'] = {'master': 'master','slave':['slave1']}
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11;'},
                'vs2': {'vs_ip': '10.235.160.76', 'host_name':'vkvm160076.sqa.cm6;', 'HC_type':1, 'url': '/11;'},
                'vs3': {'vs_ip': '10.235.160.86', 'host_name':'vkvm160086.sqa.cm6;', 'HC_type':1, 'url': '/11;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 0), ('vs2', 0), ('vs3', 0)])
    logger.debug("# Test # test stopped and success!!!")

# 1 tcheck, 3 vs, 3 uri, 1 or 2 down
def test_1tcheck_3vs_3uri_partdown_14():
    conf['tcheck'] = {'master': 'master','slave':['slave1']}
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'available':0, 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11; /1; /2;'},
                'vs2': {'vs_ip': '10.235.160.76', 'available':0, 'host_name':'vkvm160076.sqa.cm6; vkvm160076.sqa.cm6; vkvm160076.sqa.cm6;', 'HC_type':1, 'url': '/11; /12; /1;'},
                'vs3': {'vs_ip': '10.235.160.86', 'available':0, 'host_name':'vkvm160086.sqa.cm6; vkvm160086.sqa.cm6; vkvm160086.sqa.cm6;', 'HC_type':1, 'url': '/1; /12; /2;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")

# 1 tcheck, 3 vs, 3 uri, part or all down
def test_1tcheck_3vs_3uri_RSdown_15():
    conf['tcheck'] = {'master': 'master','slave':['slave1']}
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11; /1; /12;'},
                'vs2': {'vs_ip': '10.235.160.76', 'host_name':'vkvm160076.sqa.cm6; vkvm160076.sqa.cm6; vkvm160076.sqa.cm6;', 'HC_type':1, 'url': '/11; /12; /13;'},
                'vs3': {'vs_ip': '10.235.160.86', 'host_name':'vkvm160086.sqa.cm6; vkvm160086.sqa.cm6; vkvm160086.sqa.cm6;', 'HC_type':1, 'url': '/1; /12; /2;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 1), ('vs2', 0), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")


# 1 tcheck, 3 vs, 3 uri, all down
def test_1tcheck_3vs_3uri_3down_16():
    conf['tcheck'] = {'master': 'master','slave':['slave1']}
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11; /12; /13;'},
                'vs2': {'vs_ip': '10.235.160.76', 'host_name':'vkvm160076.sqa.cm6; vkvm160076.sqa.cm6; vkvm160076.sqa.cm6;', 'HC_type':1, 'url': '/11; /12; /13;'},
                'vs3': {'vs_ip': '10.235.160.86', 'host_name':'vkvm160086.sqa.cm6; vkvm160086.sqa.cm6; vkvm160086.sqa.cm6;', 'HC_type':1, 'url': '/11; /12; /13;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 0), ('vs2', 0), ('vs3', 0)])
    logger.debug("# Test # test stopped and success!!!")


# 3 tcheck, 1 vs, 3 uri, 1 down
def test_3tcheck_1vs_3uri_1down_17():
    conf['tcheck'] = {'master': 'master','slave':['slave1', 'slave2', 'slave3']}
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'available':0, 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11; /2; /3;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 1)])
    logger.debug("# Test # test stopped and success!!!")

# 3 tcheck, 1 vs, 3 uri, 3 unavailable
def test_3tcheck_1vs_3uri_3down_18():
    conf['tcheck'] = {'master': 'master','slave':['slave1', 'slave2', 'slave3']}
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11; /12; /13;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 0)])
    logger.debug("# Test # test stopped and success!!!")


# 3 tcheck, 3 vs, 3 uri, part unavailable
def test_3tcheck_3vs_3uri_partdown_19():
    conf['tcheck'] = {'master': 'master','slave':['slave1', 'slave2', 'slave3']}
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'available':0, 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/1; /12; /13;'},
                'vs2': {'vs_ip': '10.235.160.76', 'available':0, 'host_name':'vkvm160076.sqa.cm6; vkvm160076.sqa.cm6; vkvm160076.sqa.cm6;', 'HC_type':1, 'url': '/11; /1; /2;'},
                'vs3': {'vs_ip': '10.235.160.86', 'available':0, 'host_name':'vkvm160086.sqa.cm6; vkvm160086.sqa.cm6; vkvm160086.sqa.cm6;', 'HC_type':1, 'url': '/11; /2; /13;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")


# 3 tcheck, 3 vs, 3 uri, 3 unavailable
def test_3tcheck_3vs_3uri_3down_20():
    conf['tcheck'] = {'master': 'master','slave':['slave1', 'slave2', 'slave3']}
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11; /12; /13;'},
                'vs2': {'vs_ip': '10.235.160.76', 'host_name':'vkvm160076.sqa.cm6; vkvm160076.sqa.cm6; vkvm160076.sqa.cm6;', 'HC_type':1, 'url': '/11; /12; /13;'},
                'vs3': {'vs_ip': '10.235.160.86', 'host_name':'vkvm160086.sqa.cm6; vkvm160086.sqa.cm6; vkvm160086.sqa.cm6;', 'HC_type':1, 'url': '/11; /12; /13;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 0), ('vs2', 0), ('vs3', 0)])
    logger.debug("# Test # test stopped and success!!!")


# 3 tcheck, 3 vs, 3 uri, part vs unavailable
def test_3tcheck_3vs_3uri_partrsdown_21():
    conf['tcheck'] = {'master': 'master','slave':['slave1', 'slave2', 'slave3']}
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11; /12; /13;'},
                'vs2': {'vs_ip': '10.235.160.76', 'host_name':'vkvm160076.sqa.cm6; vkvm160076.sqa.cm6; vkvm160076.sqa.cm6;', 'HC_type':1, 'url': '/11; /1; /3;'},
                'vs3': {'vs_ip': '10.235.160.86', 'host_name':'vkvm160086.sqa.cm6; vkvm160086.sqa.cm6; vkvm160086.sqa.cm6;', 'HC_type':1, 'url': '/11; /2; /13;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 0), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")

# 3 tcheck, 3 vs, 3 uri, part vs part unavailable
def test_3tcheck_3vs_3uri_partdown_22():
    conf['tcheck'] = {'master': 'master','slave':['slave1', 'slave2', 'slave3']}
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'available':0, 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/1; /2; /3;'},
                'vs2': {'vs_ip': '10.235.160.76', 'available':0, 'host_name':'vkvm160076.sqa.cm6; vkvm160076.sqa.cm6; vkvm160076.sqa.cm6;', 'HC_type':1, 'url': '/11; /1; /3;'},
                'vs3': {'vs_ip': '10.235.160.86', 'available':0, 'host_name':'vkvm160086.sqa.cm6; vkvm160086.sqa.cm6; vkvm160086.sqa.cm6;', 'HC_type':1, 'url': '/11; /2; /13;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 1), ('vs2', 1), ('vs3', 1)])
    logger.debug("# Test # test stopped and success!!!")


# 206 response is consider vs ok
def test_206_response_23():
    conf['tcheck'] = {'master': 'master','slave':['slave1']}
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'available':0, 'host_name':'vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/206.html;'}}
    tcheck.deploy(conf)
    tcheck.start_206_tcheck(['slave1'])

    tcheck.check_db([('vs1', 1)])
    logger.debug("# Test # test stopped and success!!!")


# 3 tcheck, 1 vs, 3 uri, no space among uri
def test_3tcheck_1vs_3uri_nospace_24():
    conf['vs']={'vs1': {'vs_ip': '10.235.160.66', 'host_name':'vkvm160066.sqa.cm6; vkvm160066.sqa.cm6; vkvm160066.sqa.cm6;', 'HC_type':1, 'url': '/11;/12;/13;'}}
    tcheck.deploy(conf)

    tcheck.check_db([('vs1', 0)])
    logger.debug("# Test # test stopped and success!!!")

