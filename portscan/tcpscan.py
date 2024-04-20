import socket
import sys

print('''[#] Pemindaian TCP Oleh Dunia MR [#]''')

def scanHost(ip, startPort, endPort):
    print('[-] Memulai Pemindaian Port TCP Pada Host %s' % ip)
    # Mulai pemindaian TCP pada host
    tcp_scan(ip, startPort, endPort)
    print('[+] Pemindaian TCP Pada Host %s Selesai' % ip)


def scanRange(network, startPort, endPort):
    print('[-] Memulai Pemindaian Port TCP Pada Jaringan %s.0' % network)
    for host in range(1, 255):
        ip = network + '.' + str(host)
        tcp_scan(ip, startPort, endPort)

    print('[+] Pemindaian TCP Pada Jaringan %s.0 Selesai' % network)


def tcp_scan(ip, startPort, endPort):
    for port in range(startPort, endPort + 1):
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if not tcp.connect_ex((ip, port)):
                print('[+] %s:%d/TCP Terbuka' % (ip, port))
                tcp.close()
        except Exception:
            pass
            

def main():
    socket.setdefaulttimeout(0.01)
    network = input("[+] Alamat IP: ")
    startPort = int(input("[+] Port Awal: "))
    endPort = int(input("[+] Port Akhir: "))
    scanHost(network, startPort, endPort)

main()
end = input("Tekan Apapun Untuk Menutup")
