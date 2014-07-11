from   httplib                    import HTTPConnection, OK
from   src.deploy                 import ENV, DNS, CMOS
from   src.util.logger            import logger
import src.protocol.dns.dns       as dns
import json, urllib


def do_dns(rt_data, dns_input, check, times):
    assert send_rt_data(rt_data)
    for ph in DNS['pharos']:
        DNS['DNS_HOST']    = DNS['pharos'][ph]['DNS_HOST']
        DNS['DNS_PORT']    = DNS['pharos'][ph]['DNS_PORT']
        DNS['DNS_TYPE']    = DNS['pharos'][ph]['DNS_TYPE']
        dns.do_dns(dns_input, check, times)

# send runtime info to CMOS device
def send_rt_data(rt_data):
    rep_json = "{}"
    ip    = CMOS['CMOS_HOST']
    port  = CMOS['CMOS_PORT']
    url   = '/'; method = 'POST'
    body  = json.dumps(rt_data)
    header= {'Content-Type':'application/json'}
    conn  = HTTPConnection(ip, port)
    logger.debug('# Test # Send runtime data to CMOS(' + ip + ' : ' + str(port) + ')...') 

    try:
        conn.request(method, url, body, header)
        rep = conn.getresponse()
        if rep.status != OK:
            raise Exception("%s:%s%s http response %s %s" % (ip, port, url, rep.status, rep.reason))
    except:
        raise Exception("Failed request To %s:%s%s" % (ip, port, url))
    finally:
        conn.close()
        return True

