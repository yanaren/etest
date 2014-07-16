# create by 2014.05
# author junbao.kjb
# low level socket for dns

import socket, time, os, struct, datetime, select
import src.util.logger    as logger
import src.util.data_util as data_util
import src.protocol.dns.DNSPacket as DNSPacket


RECVBUFFER = 4096


def send_packet(data, para):
    recived='Ali_test_fail'

    # Parse config
    server_ip = para[2]
    server_port = para[3]
    sockettype = para[4]

    socket_type=socket.SOCK_DGRAM
    if sockettype != 'UDP':
        socket_type = socket.SOCK_STREAM
        bytes=data_util.bitset(2, {'15-0':len(data)})
        data=data_util.bytes2str(bytes) + data

    try:
        sock = socket.socket(socket.AF_INET, socket_type)
    except socket.error, e:
        logger.logger.debug('create socket return error. errno = %d, errmsg = %s' % (e.args[0], e.args[1]))

    try:
        sock.settimeout(10)
        #sock.setblocking(0)
        # connect to server
        sock.connect((server_ip, server_port))
        sock.send(data)
        
        # set timeout as 2 for the socket
        while recived == 'Ali_test_fail':
            recived = sock.recv(RECVBUFFER)
    except socket.error, e:
        logger.logger.debug('connect server failed. errno = %d, errmsg = %s' % (e.args[0], e.args[1]))
    sock.close()

    return recived


# dns concurrent test
def send_multi_dns(data, para):
    bps      = para['bps']
    concur   = para['concur']
    duration = para['duration']*1000
    t_bps    = bps/10
    dns_fail = 0
    dns_sent = 0

    m_start = datetime.datetime.now()
    m_stop  = datetime.datetime.now()
    m_inter = int((m_stop-m_start).total_seconds()*1000)
    send_start = datetime.datetime.now()
    send_mode = True

    while m_inter < duration:
        if send_mode:
            t_bps    = bps/10
            t_start = datetime.datetime.now()
            t_stop  = datetime.datetime.now()
            t_inter = int((t_stop-t_start).total_seconds()*100)
            while t_inter < 100 and t_bps > 0:
                result = send_dns(data, para)
                dns_sent += 1
                if result != 'Ali_test_fail':
                    pass
                    #res = DNSPacket.DNSPacket(result, 'UDP')
                    #print res.get_an_rdata()
                else:
                    dns_fail += 1
                t_stop  = datetime.datetime.now()
                t_bps -= 1
                t_inter = int((t_stop-t_start).total_seconds()*100)
            send_mode = False
        else:
            now  = datetime.datetime.now()
            if 100 <= int((now-send_start).total_seconds()*1000):
                send_mode = True
                send_start = datetime.datetime.now()

        m_stop  = datetime.datetime.now()
        m_inter = int((m_stop-m_start).total_seconds()*1000)

    log1 = 'Total DNS Sent: ' + str(dns_sent) + ', speed is: ' + str(float(dns_sent)/para['duration']) + 'bps\n'
    log2 = 'Total Successful:'+ str(dns_sent - dns_fail)+', sucessful ratio is: ' \
            + str(float(dns_sent-dns_fail)/para['duration']) + 'bps'
    print log1 + log2

def send_dns(data, para):
    recived='Ali_test_fail'

    # Parse config
    source_ip = para['srcip']
    server_ip = para['dstip']
    server_port = para['dstport']
    sockettype = para['4layertype']
    timeout = (para['timeout'])

    socket_type=socket.SOCK_DGRAM
    if sockettype != 'UDP':
        socket_type = socket.SOCK_STREAM
        bytes=data_util.bitset(2, {'15-0':len(data)})
        data=data_util.bytes2str(bytes) + data

    try:
        sock = socket.socket(socket.AF_INET, socket_type)
    except socket.error, e:
        logger.logger.debug('create socket return error. errno = %d, errmsg = %s' % (e.args[0], e.args[1]))

    try:
        #sock.setblocking(0)
        sock.connect((server_ip, server_port))
        sock.send(data)

        t_start = datetime.datetime.now()
        t_stop  = datetime.datetime.now()
        t_inter = int((t_stop-t_stop).total_seconds()*1000)
        while t_inter < timeout and recived == 'Ali_test_fail':
            try:
                recived = sock.recv(RECVBUFFER)
            except:
                pass
            t_stop  = datetime.datetime.now()
            t_inter = int((t_stop-t_start).total_seconds()*1000)
        #ready = select.select([sock], [], [], timeout)
        #while recived == 'Ali_test_fail':
        #while [] == ready[0]:
        #   recived = sock.recv(RECVBUFFER)
        #   ready = select.select([sock], [], [], timeout)
    except socket.error, e:
        logger.logger.debug('connect server failed. errno = %d, errmsg = %s' % (e.args[0], e.args[1]))
    sock.close()

    return recived


