#create by 2014.05
#author junbao.kjb
#
#DNS sender 
#

import ConfigParser, select, socket, json, time, os, re, struct, types
import src.protocol.alisocket     as alisocket
import src.util.data_util         as data_util
from   src.deploy                 import ENV, DNS
from   src.util.logger            import logger
from   src.protocol.dns.DNSPacket import DNSPacket


# input={ 'DNS_HOST': DNS['DNS_HOST'], 'DNS_PORT': DNS['DNS_PORT'], 'DNS_TYPE': DNS['DNS_TYPE'], 'data': data}  or
# input={ 'DNS_HOST': DNS['DNS_HOST'], 'DNS_PORT': DNS['DNS_PORT'], 'DNS_TYPE': DNS['DNS_TYPE'], 'id': 1, 'qr': 0, 
#         'opcode':0,'aa': 0,'tc':0,'rd':1,'ra':0,'z':0,'rcode':0,'qdcount': 1,'ancount':0,'nscount':0,'arcount': 0, 
#         'qd':[{'qd_qname':'img01.taobaocdn.com.danuoyi.tbcache.com', 'qd_qtype': 1, 'qd_qclass': 1}] },
#         'an':[{'an_rclass': 1, 'an_ttl':1, 'an_rrname': 'www.taobao.com', 'an_rdata': '1.1.1.1', 'an_type': 1}]
#
# check = { 'qdcount':>2, 'an_rclass':1, 'an_rdata': [('10.235.160.93', 0.5), ('10.235.160.83', 0.5)]}
def do_dns(input, check, times=1):
    RDATA_NUM={}; Total_DNS = 0; result = True
    resp = ''; server_ip = ''; server_port = 53; dns_type = 'UDP'
    if input.has_key('DNS_HOST'):
        server_ip=input['DNS_HOST']
    else:
        server_ip = DNS['DNS_HOST']
    if input.has_key('DNS_PORT'):
        server_port=input['DNS_PORT']
    else:
        server_port = DNS['DNS_PORT']
    if input.has_key('DNS_TYPE'):
        dns_type = input['DNS_TYPE']
    else:
        dns_type = DNS['DNS_TYPE']
    logger.debug('# Test # start to send DNS query to:' + server_ip + ':' + str(server_port) + ' for '+ str(times) + ' times...')

    # send DNS query for times
    for i in range(0, times):
        # send raw data
        if input.has_key('data'):
            resp = alisocket.send_packet(input['data'], ('', '', server_ip, server_port, dns_type))
        # send fromat dns data
        else:
            resp = send_dns(input)

        # decode DNS packet
        dns = DNSPacket(resp, dns_type)
        for item in check:
            # check an_rdata (special)
            if item == 'an_rdata':
                func = getattr(dns, 'get_'+item)
                ans = func()
                for data in ans:
                    if RDATA_NUM.has_key(data):
                        RDATA_NUM[data] += 1
                    else:
                        RDATA_NUM[data] = 1
            # simple logical with '> < !='
            else:
                if -1 != item.find('total_'):
                    continue

                func = getattr(dns, 'get_'+item)
                ans = func()
                if -1 == item.find('_'):
                    if type(check[item]) is str and check[item][0] == '>':
                        if check[item][1] == '=':
                            if ans < int(check[item][2:]):
                                result = False
                        elif ans <= int(check[item][1:]):
                            result = False
                    elif type(check[item]) is str and check[item][0] == '<':
                        if ans >= int(check[item][1:]):
                            result = False
                    elif type(check[item]) is str and check[item][0] == '!':
                        if ans == int(check[item][1:]):
                            result = False
                    elif type(check[item]) is str and check[item].find('|') != -1:
                        result = False
                        for tmp in check[item].split('|'):
                            if str(ans) == tmp:
                                result = True
                        if result == False:
                            print ans
                    elif ans != check[item]:
                        result = False
                #
                else:
                    if check[item] not in ans:
                        result = False
                    #for expect in check[item]:
                    #    try:
                    #        pos = ans.index(expect) 
                    #    except:
                    #        result = False
                if result == False:
                    logger.debug("# Test # result Error: result is not expected")
                    raise

    # if check an_rdata(ip addr etc.), give detail info
    if result != False and check.has_key('an_rdata'):
        msg = ''
        for item in RDATA_NUM:
            Total_DNS += RDATA_NUM[item]
            msg += '\n                               ' + item + ': ' + str(RDATA_NUM[item]) + ' times'
        for item in check['an_rdata']:
            tmp = RDATA_NUM[item[0]]/float(Total_DNS)
            if item[1] < tmp-0.1 or item[1] > tmp+0.1:
                logger.debug("# Test # result Error: %s has about %f in totally", item[0], tmp)
                result = False
        msg += '\n                               Result check Successful:' + str(check)
        logger.debug('# Test # DNS Response for query to: ' + server_ip + ':' + str(server_port) + msg)

    if result != False and check.has_key('total_rdata'):
        if type(check['total_rdata']) is str and check['total_rdata'][0] == '>':
            result = (Total_DNS > check['total_rdata'][1:])
        elif type(check['total_rdata']) is str and check['total_rdata'][0] == '<':
            result = (Total_DNS < check['total_rdata'][1:])
        else:
            result = (Total_DNS == check['total_rdata'])

    assert result



#DNS query format:
#-- ID             -- (16 bits)
#-- Flags          -- (16 bits: qr(15) + opcode(14-11) + aa(10) + tc(9) + rd(8) + ra(7) + z(6-4) + rcode(3-0))
#-- qd             -- (16 bits)
#-- an             -- (16 bits)
#-- ns             -- (16 bits)
#-- ar             -- (16 bits)
# input = {'DNS_HOST':'8.8.8.8', 'id': 1, 'qr':1, 'qd':[{'qd_qname':'www.taobao.com', 'qd_qtype':1}]}
def send_dns(input):
    # Parse dns query
    if input.has_key('DNS_HOST'):
        server_ip=input['DNS_HOST']
    else:
        server_ip = DNS['DNS_HOST']
    if input.has_key('DNS_PORT'):
        server_port=input['DNS_PORT']
    else:
        server_port = DNS['DNS_PORT']
    if input.has_key('DNS_TYPE'):
        sockettype = input['DNS_TYPE']
    else:
        sockettype = DNS['DNS_TYPE']
    if input.has_key('dnstype'):
        dns_type=input['dnstype']
    else:
        dns_type='UDP'
    if input.has_key('id'):
        id=input['id']
    else:
        id=int(data_util.gen_str("<d,4>"))
    if input.has_key('qr'):
        qr=input['qr']
    else:
        qr=0
    if input.has_key('opcode'):
        opcode=input['opcode']
    else:
        opcode=0
    if input.has_key('aa'):
        aa=input['aa']
    else:
        aa=0
    if input.has_key('tc'):
        tc=input['tc']
    else:
        tc=0
    if input.has_key('rd'):
        rd=input['rd']
    else:
        rd=1
    if input.has_key('ra'):
        ra=input['ra']
    else:
        ra=0
    if input.has_key('z'):
        z=input['z']
    else:
        z=0
    if input.has_key('rcode'):
        rcode=input['rcode']
    else:
        rcode=0
    if input.has_key('qdcount'):
        qdcount=input['qdcount']
    else:
        qdcount=1
    if input.has_key('ancount'):
        ancount=input['ancount']
    else:
        ancount=0
    if input.has_key('nscount'):
        nscount=input['nscount']
    else:
        nscount=0
    if input.has_key('arcount'):
        arcount=input['arcount']
    else:
        arcount=0
    
    data=''
    bytes=data_util.bitset(2, {'15-0':id})
    data+=data_util.bytes2str(bytes)
    bytes=data_util.bitset(2, {'15':qr, '14-11':opcode, '10':aa, '9':tc, '8':rd, '7':ra, '6-4':z, '3-0':rcode})
    data+=data_util.bytes2str(bytes)
    data+=data_util.bytes2str([(qdcount%256), (qdcount/256)])
    data+=data_util.bytes2str([(ancount%256), (ancount/256)])
    data+=data_util.bytes2str([(nscount%256), (nscount/256)])
    data+=data_util.bytes2str([(arcount%256), (arcount/256)])

    if input.has_key('qd'):
        qd=input['qd']
    else:
        qd={}

    for qd_item in qd:
        if qd_item.has_key('qd_qname'):
            qd_qname=qd_item['qd_qname']
        else:
            qd_qname='www.taobao.com'

        if qd_item.has_key('qd_qtype'):
            qd_qtype=qd_item['qd_qtype']
        else:
            qd_qtype=1

        if qd_item.has_key('qd_qclass'):
            qd_qclass=qd_item['qd_qclass']
        else:
            qd_qclass=1

        data += data_util.name2str(qd_qname)
        data+=data_util.bytes2str([(qd_qtype%256), (qd_qtype/256)])
        data+=data_util.bytes2str([(qd_qclass%256), (qd_qclass/256)])

    if input.has_key('an'):
        an=input['an']
    else:
        an={}

    for an_item in an:
        if an_item.has_key('an_rclass'):
            an_rclass=an_item['an_rclass']
        else:
            an_rclass=1
        if an_item.has_key('an_ttl'):
            an_ttl=an_item['an_ttl']
        else:
            an_ttl=1
        if an_item.has_key('an_rrname'):
            an_rrname=an_item['an_rrname']
        else:
            an_rrname='www.taobao.com'
        if an_item.has_key('an_rdata'):
            an_rdata=an_item['an_rdata']
        else:
            an_rrname='1.1.1.1'
        if an_item.has_key('an_type'):
            an_type=an_item['an_type']
        else:
            an_type=1
        data += data_util.name2str(qd_qname)
        data+=data_util.bytes2str([(qd_qtype%256), (qd_qtype/256)])
        data+=data_util.bytes2str([(qd_qclass%256), (qd_qclass/256)])

    #logger.debug("# Test # send DNS query to %s:%d", DNS['DNS_HOST'], DNS['DNS_PORT'])
    recd = alisocket.send_packet(data, ('', '', server_ip, server_port, dns_type))

    return recd

