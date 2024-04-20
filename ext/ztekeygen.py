#!/usr/bin/env python
# Penggunaan:
# ./ext/ztekeygen.py
# Alamat MAC: 8d719f807123
# Serial: ZTE123456789
# SSID Pabrik: ZTE_2.4G_G22e7F
# Kunci WLAN Pabrik: !@#$%12345
# Nama Pengguna Pabrik: admin
# Kata Sandi Pabrik: Telkomdso123
# Versi Perangkat Keras: V9.0
# Hasil: 0305ab0d9b90b918
#
# Contoh Pemecah:
#
# PYTHONPATH=./zte-decoder
# python ./zte-decoder/decoder3.py config/config.bin config/config.xml --key 0305ab0d9b90b918
#
# Contoh Pemulai:
#
# PYTHONPATH=./zte-config-utility
# python ./zte-decoder/encoder1.py config/config.xml config/new.config.bin --key 0305ab0d9b90b918 --signature "F609"

from hashlib import md5

l = lambda s: len(s).to_bytes(3, "little")
a = lambda s: s.encode("ascii")

mac      = int(input("Alamat MAC: "), 16)
serial   = a(input("Serial: "))
ssid     = a(input("SSID Pabrik: "))
wlan_key = a(input("Kunci WLAN Pabrik: "))
username = a(input("Nama Pengguna Pabrik: "))
password = a(input("Kata Sandi Pabrik: "))
mac_zte  = a("54BE53")
version  = a(input("Versi Perangkat Keras: "))
zero     = a("0")

print(md5(
    b"\x01\x00\x00\x06\x00\x00" + (mac).to_bytes(6, "big") + \
    b"\x01\x01\x00\x06\x00\x00" + (mac + 1).to_bytes(6, "big") + \
    b"\x01\x02\x00\x06\x00\x00" + (mac + 2).to_bytes(6, "big") + \
    b"\x01\x03\x00\x06\x00\x00" + (mac + 3).to_bytes(6, "big") + \
    b"\x02\x00\x00" + l(serial)   + serial + \
    b"\x04\x00\x00" + l(ssid)     + ssid + \
    b"\x05\x10\x00" + l(wlan_key) + wlan_key + \
    b"\x06\x01\x00" + l(username) + username + \
    b"\x07\x01\x00" + l(password) + password + \
    b"\x03\x00\x00" + l(mac_zte)  + mac_zte + \
    b"\x08\x06\x00" + l(version)  + version + \
    b"\x08\x07\x00" + l(zero)     + zero
).hexdigest()[:16])
