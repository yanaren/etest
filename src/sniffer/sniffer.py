import threading, subprocess
#import dpkt, pcap
t=None

def capture(card, host, port, pro, file):
    global t
    t = threading.Thread(target=cap, args=(card, host, port, pro, file))
    t.start()
    return t

def cap(card, host, port, pro, file):
    cmd = 'sudo tcpdump ' + pro + ' port ' + port + ' and host ' + host + ' -s0 -i ' + card + ' -w ' + file
    p=subprocess.Popen(['bash','-c',cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def join():
    #cmd = 'sudo killall -9 tcpdump'
    #popen=subprocess.Popen(['bash','-c',cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t.join()
