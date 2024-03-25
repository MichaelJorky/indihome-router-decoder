#!/usr/bin/env python
# Usage:
# ./ext/ztekeygen.py
# MAC address: 8d719f807123
# Serial: ZTE123456789
# Factory SSID: ZTE_2.4G_G22e7F
# Factory WLAN Key: !@#$%12345
# Factory Username: admin
# Factory Password: Telkomdso123
# Hardware Version: V9.0
# Result: 0305ab0d9b90b918
#
# Example Decoder:
#
# PYTHONPATH=./zte-decoder
# python ./zte-decoder/unidecoder.py config/config.bin config/config.xml --key 0305ab0d9b90b918
#
# Example Encoder:
#
# PYTHONPATH=./zte-config-utility
# python ./zte-decoder/uniencoder.py config/config.xml config/new.config.bin --key 0305ab0d9b90b918 --signature "F609"

from hashlib import md5

l = lambda s: len(s).to_bytes(3, "little")
a = lambda s: s.encode("ascii")

mac      = int(input("MAC address: "), 16)
serial   = a(input("Serial: "))
ssid     = a(input("Factory SSID: "))
wlan_key = a(input("Factory WLAN Key: "))
username = a(input("Factory Username: "))
password = a(input("Factory Password: "))
mac_zte  = a("54BE53")
version  = a(input("Hardware Version: "))
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
