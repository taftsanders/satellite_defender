#!/usr/bin/python2

from collections import Counter
import time
import subprocess
import re
import os.path
import operator

FOREMAN_HTTP_LOG = '/var/log/httpd/foreman-ssl_access_ssl.log'
PUPPET_HTTP_LOG = '/var/log/httpd/puppet_access_ssl.log'
OFFENDERS_LOG = '/var/log/offenders'
FOREMAN_COMMAND = ['cat', FOREMAN_HTTP_LOG, '|', 'cut', '-d\' \'', '-f1',  '|', 'sort', '|', 'uniq -c']
FOREMAN_COMMAND2 = "cat " + FOREMAN_HTTP_LOG + " | cut -d' ' -f1 | sort | uniq -c"
PUPPET_COMMAND = ['cat', PUPPET_HTTP_LOG, '|', 'cut', '-d\' \'', '-f1',  '|', 'sort', '|', 'uniq -c']

def foreman_header():
    print("""
#########################
FOREMAN CHECK-INS
#########################
""")

def puppet_header():
    print("""
#########################
PUPPET CHECK-INS
#########################
""")

def date_header():
    print('')
    print('######################')
    print(time.strftime('%Y-%m-%d %H:%M'))
    print('######################')
    print('')

def foreman_start_date():
    # open file, grab first line date/time
    with open(FOREMAN_HTTP_LOG, 'r') as file:
        first_line = file.readline().strip()
        format = first_line.split()[3]
    return format[1:]

def foreman_end_date():
    # open file, grab last line date/time
    with open(FOREMAN_HTTP_LOG, 'r') as file:
        last_line = file.readlines()[-1].strip()
        format = last_line.split()[3]
    return format[1:]

def puppet_start_date():
    # open file, grab first line date/time
    with open(PUPPET_HTTP_LOG, 'r') as file:
        first_line = file.readline().strip()
        format = first_line.split()[3]
    return format[1:]

def puppet_end_date():
    # open file, grab last line date/time
    with open(PUPPET_HTTP_LOG, 'r') as file:
        last_line = file.readlines()[-1].strip()
        format = last_line.split()[3]
    return format[1:]

def write_foreman():
    # write FOREMAN_COMMAND to file
    foreman_header()
    print('')
    ips = []
    with open(FOREMAN_HTTP_LOG, 'r') as file:
        log = file.readlines()
        for line in log:
            regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})',line)
            ips.append(regex[0])
    cnt = Counter()
    for word in ips:
        cnt[word] += 1
    sorted_x = sorted(cnt.items(), key=operator.itemgetter(1), reverse=True)
    for value in sorted_x:
        print(value)

def write_puppet():
    # write PUPPET_COMMAND to file
    puppet_header()
    print('')
    ips = []
    with open(PUPPET_HTTP_LOG, 'r') as file:
        log = file.readlines()
        for line in log:
            regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})',line)
            ips.append(regex[0])
    cnt = Counter()
    for word in ips:
        cnt[word] += 1

def create_file():
    # create log file
    with open(OFFENDERS_LOG, 'w') as file:
        file.close()

def create_motd():
    # create motd
    with open('/etc/motd', 'w') as file:
        file.close()

def write_output():
    print('Between ' + foreman_start_date() + ' and ' + foreman_end_date() + ':')
    write_foreman()
    print('')
    print('Between ' + puppet_start_date() + ' and ' + puppet_end_date() + ':')
    write_puppet()

def main():
    if not os.path.exists(OFFENDERS_LOG):
        create_file()
    with open(OFFENDERS_LOG, 'a') as file:
        file.write(str(date_header()))
        file.write(str(write_output()))
    if not os.path.exists('/etc/motd'):
        create_motd()
    with open('/etc/motd', 'w') as file:
        file.write(str(write_output()))

main()