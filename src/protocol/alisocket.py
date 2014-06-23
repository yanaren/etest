# create by 2014.05
# author junbao.kjb
# low level socket for dns

import socket, time, os, struct
import src.util.logger    as logger
import src.util.data_util as data_util


RECVBUFFER = 2048


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


