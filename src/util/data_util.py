# coding=utf-8
'''
'''
import re, struct
import string
import random


def gen_str(str_line):
    '''
    Format: <type, length>, e.g. <l,5>, <cd,10>, <a,20>

    w == whitespace -- a string containing all ASCII whitespace
              = ' \t\n\r\v\f'
    l == ascii_lowercase -- a string containing all ASCII lowercase letters
              = 'abcdefghijklmnopqrstuvwxyz'
    u == ascii_uppercase -- a string containing all ASCII uppercase letters
              = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    c == char(ascii_letters) -- a string containing all ASCII letters
              = ascii_lowercase + ascii_uppercase
    d == digits -- a string containing all ASCII decimal digits
              = '0123456789'
    h == hexdigits -- a string containing all ASCII hexadecimal digits
              = digits + 'abcdef' + 'ABCDEF'
    o == octdigits -- a string containing all ASCII octal digits
              = '01234567'
    p == punctuation -- a string containing all ASCII punctuation characters
              = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    a == all(printable) -- a string containing all ASCII characters
              considered printable = digits + ascii_letters + punctuation
               + whitespace
    '''
    pat = re.compile('<[wlucdhopa]+,[0-9]+>')
    return pat.sub(__cast_pattern, str_line)


def __cast_pattern(matched_pattern):
    seed_types = {
        'w': string.whitespace,
        'l': string.ascii_lowercase,
        'u': string.ascii_uppercase,
        'c': string.ascii_letters,
        'd': string.digits,
        'h': string.hexdigits,
        'o': string.octdigits,
        'p': string.punctuation,
        'a': string.printable
    }
    pat = re.compile('[wlucdhopa]+')
    types = list(pat.findall(matched_pattern.group())[0])
    pat = re.compile('[0-9]+')
    length = int(pat.findall(matched_pattern.group())[0])
    seeds = ''.join(seed_types[t] for t in types)
    return ''.join(random.choice(seeds) for _ in range(length))


#def gen_file_in_size(file_size, file_name=None,
#                     head_content='head', end_content='end'):
    '''
    generate a file with assigned size in M
    '''
#    file_name = file_name if file_name else str(file_size) + 'M.txt'
#    file_util.create_file(file_name)
#    tmp_file = open(file_name, 'w')
#    tmp_file.write(head_content)
#    tmp_file.seek(file_size * 1024 * 1024 - len(end_content))
#    tmp_file.write(end_content)
#    tmp_file.close()
#    return file_name


def string2hex():
    str1=sys.argv[1]
    if len(str1)%2 == 1:
        print 'the input is not right, you must input ...'


    bytes=len(str1)/2
    str2=''
    for i in range(0, bytes):
        str2=str2 + '0x' + str1[2*i:2*i+2] + ', '

# {'15-8':24, '7':1, '6-0':6} --> [134, 24]
def bitset(bytecount, bits={}):
    bytes=[0]*bytecount
    for part in bits:
       if part.find('-') != -1:
           begin=string.atoi(part[part.find('-')+1:])
           end  =string.atoi(part[0:part.find('-')])
           for j in range(begin, end+1):
               if 0 != ((bits[part] & 0x01<<(j-begin))):
                   bytes[j/8] += (0x01 << j%8)
       else:
           pos = int(part)
           bytes[pos/8] += ((bits[part] << pos%8)%256)

    return bytes
 
 
# [134, 24] -> \x18\x86
def bytes2str(bytes):
    result=''
    bytescount=len(bytes)
    for i in range(0, bytescount):
        tmp = str(hex(bytes[bytescount-i-1]))
        result += struct.pack('B', bytes[bytescount-i-1])

    return result


# '3223e4522435' -> '\x32\x23\xe4\x52\x24\x35'
def hexs2str(data):
    if (len(data))%2 != 0:
        raise
    result = ''
    i=0
    while i<len(data):
        result += struct.pack('B', int(data[i:i+2], 16))
        i +=2
    return result


#  www.taobao.com  ->  \x03www\x06taobao\x03com\x00
def name2str(name):
    result=''
    namelist=name.split('.')
    for item in namelist:
        result+=bytes2str([len(item)])
        result+=item
    result+=hexs2str('00')
    return result


