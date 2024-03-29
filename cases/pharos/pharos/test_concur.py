from   src.util.logger            import logger
import src.protocol.alisocket     as DNS
import src.protocol.dns.DNSPacket as DNSPacket
import src.deploy.pharos          as pharos
import src.util.system_util       as system_util
import pytest, time

def test_1():
    data='\xd7\x76\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x05\x69\x6d\x67\x30\x31\x09\x74\x61\x6f\x62\x61\x6f\x63\x64\x6e\x03\x63\x6f\x6d\x07\x64\x61\x6e\x75\x6f\x79\x69\x07\x74\x62\x63\x61\x63\x68\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01\x05\x69\x6d\x67\x30\x31\x09\x74\x61\x6f\x62\x61\x6f\x63\x64\x6e\x03\x63\x6f\x6d\x07\x64\x61\x6e\x75\x6f\x79\x69\x07\x74\x62\x63\x61\x63\x68\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01'
    # timeout: ms, duration: s
    paras = {'srcip':'', 'srcport':'', 'dstip':'10.101.81.12', 'dstport':53, '4layertype':'UDP', 
             'timeout':20, 'bps':1000, 'concur':10, 'duration':10}
    
    result = DNS.send_multi_dns(data, paras)
