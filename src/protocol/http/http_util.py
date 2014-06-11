'''
Created on 2013-3-18

@author: renyong
'''
import urllib2
from alitest import logger
import urllib
import json
from httplib import HTTPConnection, OK
import alitest
import time
# from http.client import HTTPConnection, OK python3.2


def http_request_post(ip, port, url, params, headers):
    rep_json = "{}"
    conn = HTTPConnection(ip, port)
    try:
        conn.request('POST', url, params, headers)
        rep = conn.getresponse()
        if rep.status == OK:
            # logger.debug("http rep content [%s]" % rep.read().decode())
            rep_json = json.loads(rep.read().decode())
        else:
            raise Exception("%s:%s%s http response %s %s" % (
                ip, port, url, rep.status, rep.reason))
    except:
        raise Exception("Failed request To %s:%s%s" % (ip, port, url))
    finally:
        conn.close()
        return rep_json


def do_request(url, headers={}, form=None):
    data = urllib.urlencode(form) if form is not None else None
    req = urllib2.Request(url, data=data)
    for key in headers.keys():
        req.add_header(key, headers[key])
    resp = urllib2.urlopen(req, timeout=alitest.DEFAULT_HTTP_CONN_TIMEOUT)
    return resp


def download_file(url, lfile_name, headers={}):
    req = urllib2.Request(url)
    for key in headers.keys():
        req.add_header(key, headers[key])
    resp = urllib2.urlopen(req, timeout=alitest.DEFAULT_HTTP_CONN_TIMEOUT)
    file_size = int(resp.info().getheaders("Content-Length")[0])
    
    lf = open(lfile_name, 'wb')
    dl_size = 0
    block = 1024
    while True:
        buffer = resp.read(block)
        if not buffer:
            break
        dl_size += len(buffer)
        lf.write(buffer)
    lf.close()
    if file_size != dl_size:
        raise Exception("File %s size does not match (%s:%s)" % (url, file_size, dl_size))
    return dl_size



def wait_http_conn_success(ip, port, retry=3):
    '''
    retry n times to make sure http connection is ok
    max waiting time == retry * (2+alitest.DEFAULT_HTTP_CONN_TIMEOUT)
    '''
    conn_succ = False
    while retry > 0:
        try:
            url = 'http://%s:%s' % (ip, port)
            resp = do_request(url)
            if resp.getcode() == 200:
                conn_succ = True
                break
        except:
            pass
        finally:
            time.sleep(2)
            retry -= 1
    # after waiting for a long time, connection should be ok
    return conn_succ


def retrieve_cookies(resp):
    cookies = []
    info = resp.info()
    ck_headers = info.getheaders('set-cookie')
    for header in ck_headers:
        kv_pairs = header.split(';')
        cookie = {'name': '', 'value': '',
                  'domain': '', 'path': '/',
                  'expires': '', 'size': '0'}
        for k_v in kv_pairs:
            k_v = k_v.strip()
            if k_v.find('=') > -1:
                key = k_v.split('=')[0]
                value = k_v.split('=')[1]
                if key.lower() == 'domain':
                    cookie['domain'] = value
                elif key.lower() == 'path':
                    cookie['path'] = value
                elif key.lower() == 'expires':
                    cookie['expires'] = value
                elif key.lower() == 'path':
                    cookie['path'] = value
                else:
                    cookie['name'] = key
                    cookie['value'] = value
                    cookie['size'] = len(key) + len(value)
        cookies.append(cookie)

    logger.debug('Found cookies: %s', cookies)
    return cookies


def curl(host, port=80, headers={}):
    url = 'http://%s:%s' % (host, port)
    resp = do_request(url, headers)
    return resp


if __name__ == "__main__":
    pass
