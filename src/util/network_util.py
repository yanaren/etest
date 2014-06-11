import re
import socket

def get_ips(input,sep=r'\s'):
    output = []
    ip_regex = '^[^\d]*(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(25[0-5]|\d|[1-9]\d|1\d\d|2[0-4]\d))[^\d]*$'
    for part in re.split(sep, input):
        match = re.match(ip_regex, part)
        if match:
            res = match.group(1)
            if validate_ip(res):
                output.append(res)
    return output


def validate_ip(ip):
    if ip == '0.0.0.0':
        return False
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except:
        return False

#print get_ips('0.0.0.0 1.2.3.4 255.0.0.0 0.0.0.255 '
#              'xxxx8.8.8.8yyy 1.2.3. 2.3.4.512')
