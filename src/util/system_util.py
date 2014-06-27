'''
Created on 2013-2-5

@author:wangguangping
'''
import subprocess, time, hashlib, os, mmap


def execute_cmd(cmd):
    '''
    return: 
        return_code - (Integer) shell command exit status
        cmd_stdout: (String) command print in stdout
        cmd_stderr: (String) command print in stderr
    '''
    assert cmd not in ['', None]
    #logger.debug('Execute the command : %s', cmd)
    proc = subprocess.Popen(cmd, shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (cmd_stdout, cmd_stderr) = proc.communicate()
    #logger.debug('Execute the command Result: %s', cmd_stdout)
    return (proc.returncode, cmd_stdout, cmd_stderr)


def exe_cmd_via_ssh(ip, cmd):
    cmd_line = 'ssh root@%s "%s"' % (ip,cmd)
    proc = subprocess.Popen(cmd_line, shell=True, 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    returncode = proc.wait()
    output = proc.stdout.read().splitlines()
    #logger.debug('Return Code:%s' % returncode)
    #logger.debug('Output:%s' % ('\n'.join(output)))
    return output


def exe_cmd_via_comm_ssh(ip, cmd):
    cmd_line = 'ssh %s "%s"' % (ip,cmd)
    proc = subprocess.Popen(cmd_line, shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    returncode = proc.wait()
    output = proc.stdout.read().splitlines()
    return output


def exe_cmd_via_staff(ip, cmd):
    staff_cmd = 'staf %s process start SHELL COMMAND %s WAIT RETURNSTDOUT STDERRTOSTDOUT' % (ip, cmd)
    (returncode, output, stderr) = execute_cmd(staff_cmd)
    print 'Execute command: \"%s\" on host: \"%s\"' % (cmd, ip)
    return (returncode == 0)


def copy_file_2_server(ip, srcfile, dstfile):
    (_, username, _) = execute_cmd('whoami')
    if username[-1] == '\n':
        username = username[0:-1]
    cmd = 'scp %s root@%s:%s' % (srcfile, ip, dstfile)
    (returncode, output, stderr) = execute_cmd(cmd)
    return (returncode == 0)


def ping(host, count=5):
    '''
    parameters:
        host - host name or ip address of dest server
        count - ICMP packets count 
    return:
        True - Success, False - No reply or others
    '''
    return_code = execute_cmd('ping -c %d %s' % (count,host))[0]
    return True if return_code == 0 else False


def port_avaliable(host, port, retry=10):
    '''
    check port of host is opened
    return: 
        True - Success, False - No reply or others
    '''
    avaliable = False
    while retry > 0:
        try:
            return_code = execute_cmd('nc -w 5 -z %s %s' % (host,port))[0]
            if return_code == 0:
                avaliable = True
                break
        except Exception as inst:
            pass
        finally:
            time.sleep(1)
            retry -= 1
    return avaliable


def shasum_file(file_name):
    '''
    calculate and return sha256 checksum for file
    '''
    sha = hashlib.sha256()
    file_desp = file(file_name, 'rb')
    file_desp.seek(0)
    file_map = mmap.mmap(file_desp.fileno(), 0, prot=mmap.PROT_READ)
    while True:
        line = file_map.readline()
        if len(line) == 0:
            break
        sha.update(line)
    file_desp.close()
    return sha.hexdigest()


def md5sum_file(file_name):
    '''
    calculate and return md5 checksum for file
    '''
    cs = hashlib.md5()
    file_desp = file(file_name, 'rb')
    file_desp.seek(0)
    file_map = mmap.mmap(file_desp.fileno(), 0, mmap.MAP_PRIVATE, mmap.PROT_READ)
    while True:
        line = file_map.readline()
        if len(line) == 0:
            break
        cs.update(line)
    file_desp.close()
    return cs.hexdigest()


# condition time wait, max wait, every min wait check.
def timer_wait(sleep_time_span, max_sleep_time, condition):
    sleep_time = 0
    while sleep_time < max_sleep_time:
        if condition(sleep_time):
            return True
        else:
            sleep_time += sleep_time_span
            time.sleep(sleep_time_span)
    return False


