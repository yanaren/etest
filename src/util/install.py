#!/usr/local/bin/python2.7
import json, socket, getpass
import src.util.system_util as system_util
from src.deploy import DNS, TCHECK

def deployssh():
    lip = socket.gethostbyname(socket.gethostname())
    user = getpass.getuser()
    print (user, lip)
    ips = ['10.101.81.12', '10.235.160.73', '10.235.160.83', '10.235.160.93']
    ips = ['10.101.81.12']
    for ip in ips:
        cmd = 'scp ~/.ssh/id_rsa.pub '+ user +'@' + ip + ':.ssh/id_rs.pub'
        system_util.execute_cmd(cmd)
        system_util.exe_cmd_via_comm_ssh(ip, 'cat /home/'+ user +'/.ssh/id_rs.pub >> /home/'+ user +'/.ssh/authorized_keys')
        system_util.exe_cmd_via_comm_ssh(ip, 'sudo cat /home/'+ user +'/.ssh/id_rs.pub >> /root/.ssh/authorized_keys')


deployssh()

#for ip in ['10.235.160.73', '10.235.160.83', '10.235.160.93']:
#    system_util.exe_cmd_via_ssh(ip, 'yum -y install gcc gcc-c++ make')
#    system_util.exe_cmd_via_ssh(ip, 'yum -y install pcre pcre-devel zlib zlib-devel openssl openssl-devel')
#    system_util.exe_cmd_via_ssh(ip, 'cd /home/junbao.kjb/servers/nginx')
#    system_util.exe_cmd_via_ssh(ip, 'wget http://nginx.org/download/nginx-1.2.0.tar.gz')
#    system_util.exe_cmd_via_ssh(ip, 'tar zxvf nginx-1.2.0.tar.gz; cd nginx-1.2.0; ./configure; make; make install;')
#    system_util.exe_cmd_via_ssh(ip, '/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf')
    
