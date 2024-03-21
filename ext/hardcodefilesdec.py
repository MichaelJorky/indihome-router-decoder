#!/usr/bin/python

import sys
from io import BytesIO
from hashlib import sha256
from Cryptodome.Cipher import AES

if len(sys.argv) != 2:
    print("No filename given")
    exit(0)
else:
    decfile = sys.argv[1]

plain_key = ''
plain_iv =  ''

print("Plain Key : " + plain_key)
print("Plain Iv  : " + plain_iv)
key = sha256(plain_key.encode("utf8")[:32]).digest()
iv = sha256(plain_iv.encode("utf8")).digest()
print("SHA Key   : " + key.hex())
print("SHA Iv    : " + iv.hex())
aes_cipher = AES.new(key[:32], AES.MODE_CBC, iv[:16])
data = open(decfile,"rb")
data.seek(72)
ciphertext = data.read()
salida = aes_cipher.decrypt(ciphertext)
print("First 16 bytes: " + salida.hex()[:32]) 
print("Hex 32    : " + salida.hex())
print("Raw 32    : " + str(salida))
