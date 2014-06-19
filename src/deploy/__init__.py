import os
from src.util.logger import logger
try:
    import simplejson as json
except ImportError:
    import json

conf_file = ''

class RuntimeConfig(object):
    _instance = None
    config = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RuntimeConfig, cls).__new__(cls, *args, **kwargs)

            if 'alitest_configuration' not in os.environ:
                raise IOError('please set Testing Configuration first')

            conf_file = os.environ.get('alitest_configuration')
            logger.debug("# testing configuration file:%s", conf_file)

            cls.load_json_file(conf_file)
            logger.debug("# testing configuration:%s", cls.config)
        return cls._instance

    @classmethod
    def load_json_file(cls, file_name):
        if not os.path.exists(os.path.abspath(file_name)):
            raise Exception("Maybe %s is not a file" % file_name)
        file_object = open(file_name, 'r')
        file_content = file_object.read()
        cls.config = json.loads(file_content)


CONFIG=RuntimeConfig().config

if CONFIG.has_key('environment'):
    ENV   = CONFIG['environment']
if CONFIG.has_key('dns'):
    DNS   = CONFIG['dns']
    DB    = DNS
if CONFIG.has_key('tcheck'):
    TCHECK= CONFIG['tcheck']
    DB    = {}
if CONFIG.has_key('vs'):
    VS    = CONFIG['vs']
