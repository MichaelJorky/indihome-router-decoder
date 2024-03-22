import socket
import sys

print('''[#] TCP Scan By Dunia MR [#]''')

def scanHost(ip, startPort, endPort):
    print('[-] Starting TCP Port Scan On Host %s' % ip)
    # Begin TCP scan on host
    tcp_scan(ip, startPort, endPort)
    print('[+] TCP Scan On Host %s Complete' % ip)


def scanRange(network, startPort, endPort):
    print('[-] Starting TCP Port Scan On Network %s.0' % network)
    for host in range(1, 255):
        ip = network + '.' + str(host)
        tcp_scan(ip, startPort, endPort)

    print('[+] TCP Scan On Network %s.0 Complete' % network)


def tcp_scan(ip, startPort, endPort):
    for port in range(startPort, endPort + 1):
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if not tcp.connect_ex((ip, port)):
                print('[+] %s:%d/TCP Open' % (ip, port))
                tcp.close()
        except Exception:
            pass
            

def main():
    socket.setdefaulttimeout(0.01)
    network = input("[+] Ip Address: ")
    startPort = int(input("[+] Start Port: "))
    endPort = int(input("[+] End Port: "))
    scanHost(network, startPort, endPort)

main()
end = input("Press Any Key To Close")
