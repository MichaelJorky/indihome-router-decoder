import socket
from IPy import IP

print('''[#] Pemindaian Multi TCP Oleh Dunia MR [#]''')

def scan(target):
    converted_ip = check_ip(target)
    print('\n' + '[Memindai Target] ' + str(target))
    for port in range(1, 8500):
        scan_port(converted_ip, port)


def check_ip(ip):
    try:
        IP(ip)
        return(ip)
    except ValueError:
        return socket.gethostbyname(ip)


def get_banner(s):
    return s.recv(1024)


def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.1)
        sock.connect((ipaddress, port))
        try:
            banner = get_banner(sock)
            print('[+] Port Terbuka ' + str(port) + ' : ' + str(banner.decode().strip('\n')))
        except:
            print('[+] Port Terbuka ' + str(port)) 
    except:
        pass

if __name__ == "__main__":
    targets = input('[+] Masukkan Target yang Akan Dipindai (Pisahkan Target yang Berbeda dengan Koma): ')

    if ',' in targets:
        for ip_add in targets.split(','):
            scan(ip_add.strip(' '))
    else:
        scan(targets)
