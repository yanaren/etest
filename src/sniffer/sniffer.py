import threading, subprocess
from src.util import system_util
#import dpkt, pcap

def capture(card, host, port, pro, file):
    t = threading.Thread(target=cap, args=(card, host, port, pro, file))
    t.start()
    t.join()
def cap(card, host, port, pro, file):
    cmd = 'sudo tcpdump -U ' + pro + ' port ' + port + ' and host ' + host + ' -s0 -i ' + card + ' -w ' + file + ' &'
    subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #system_util.execute_cmd(cmd)
    

def end():
    cmd = 'sudo killall tcpdump'
    subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
