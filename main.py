#!/usr/bin/python2

from __future__ import print_function
from collections import Counter
import time
import subprocess
import re
import os.path
import operator

FOREMAN_HTTP_LOG = '/var/log/httpd/foreman-ssl_access_ssl.log'
PUPPET_HTTP_LOG = '/var/log/httpd/puppet_access_ssl.log'
OFFENDERS_LOG = '/var/log/offenders'
MOTD = '/etc/motd'

def header(service,location):
    if service == 'foreman':
        header = """
#########################
FOREMAN CHECK-INS
#########################
"""
        print('Between ' + foreman_start_date() + ' and ' + \
        foreman_end_date() + ':', file = open(location, 'a'))
    elif service == 'puppet':
        header = """
#########################
PUPPET CHECK-INS
#########################
"""
        print('Between ' + puppet_start_date() + ' and ' + \
        puppet_end_date() + ':', file = open(location, 'a'))
    return header

def date_header():
    header = """\n######################\n""" + \
    time.strftime('%Y-%m-%d %H:%M') + \
    """\n######################\n"""
    return header

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

def write_foreman(location):
    # write FOREMAN_COMMAND to file
    print(header('foreman', location), file = open(location, 'a'))
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
        print(value, file = open(location, 'a'))

def write_puppet(location):
    # write PUPPET_COMMAND to file
    print(header('puppet', location), file = open(location, 'a'))
    ips = []
    with open(PUPPET_HTTP_LOG, 'r') as file:
        log = file.readlines()
        for line in log:
            regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})',line)
            ips.append(regex[0])
    cnt = Counter()
    for word in ips:
        cnt[word] += 1
    sorted_x = sorted(cnt.items(), key=operator.itemgetter(1), reverse=True)
    for value in sorted_x:
        print(value, file = open(location, 'a'))
        
def create_file():
    # create log file
    with open(OFFENDERS_LOG, 'a') as file:
        file.close()

def create_motd():
    # create motd
    with open(MOTD, 'a') as file:
        file.close()

def write_output(location):
    print(write_foreman(location), file = open(location, 'a'))
    print(write_puppet(location), file = open(location, 'a'))

def main():
    if not os.path.exists(OFFENDERS_LOG):
        create_file()
    with open(OFFENDERS_LOG, 'a') as log:
        log.write(str(date_header())+ '\n')
        log.write(str(write_output(OFFENDERS_LOG))+ '\n')
#    if not os.path.exists('/etc/motd'):
#        create_motd()
#    with open(MOTD, 'w') as motd:
#        motd.write(str(write_output(MOTD)))

if __name__ == '__main__':
    main()