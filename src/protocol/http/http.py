import getopt, socket, logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import binascii

default_dstIp='10.235.160.73'
BUFFER_SIZE=65536
default_dstPort=81
msg='GET /SingleExtension_RequestWithAbsentValue HTTP/1.1\r\n\
Accept-Encoding: identity\r\n\
host: macaroon.zymlinux.net\r\n\
user-agent: mockclient/0.1\r\n\
accept: */*\r\n\
\r\n'



def sendRawRequest(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((default_dstIp, default_dstPort))

    sock.send(msg)
    data = sock.recv(BUFFER_SIZE)
    sock.close()
    print data

def sendRequest(msg):
    print msg

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((default_dstIp, default_dstPort))

    hexMsg=''; Mssg=''
    for line in msg:
        for i in range(0, len(line)):
            a = binascii.b2a_hex(line[i])
            #num = hex(ord(line[i]))
            hexMsg+= a
            #Mssg+=a
    #ans=sr(IP(dst=default_dstIp)/TCP(dport=default_dstPort)/hexMsg, timeout=5)
    sock.send(hexMsg)
    data = sock.recv(BUFFER_SIZE)
    sock.close()
    print data
    print '------------'

sendRawRequest(msg)
#sendRequest(msg)
