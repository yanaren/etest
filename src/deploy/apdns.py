import thread, socket, struct, time
import src.util.system_util as system_util
import src.util.db as db
from src.util.logger import logger
from src.deploy import DNS


def setDNS(dns_conf):
    if dns_conf.has_key('DNS_HOST'):
        DNS['DNS_HOST'] = dns_conf['DNS_HOST']

    if dns_conf.has_key('DNS_PORT'):
        DNS['DNS_PORT'] = dns_conf['DNS_PORT']

    if dns_conf.has_key('DB_HOST'):
        DNS['DB_HOST'] = dns_conf['DB_HOST']

