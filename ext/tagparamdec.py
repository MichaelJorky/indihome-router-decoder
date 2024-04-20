import sys
from io import BytesIO
from hashlib import sha256
from Cryptodome.Cipher import AES

plain_key = ''
plain_iv =  ''

print("Kunci Teks Biasa: " + plain_key)
print("IV Teks Biasa   : " + plain_iv)
key = sha256(plain_key.encode("utf8")[:32]).digest()
iv = sha256(plain_iv.encode("utf8")[:32]).digest()
print("SHA Kunci    : " + key.hex())
print("SHA IV       : " + iv.hex())
print()
data = open("paramtag","rb")
data.seek(20)
tagn = 0
while True:
  data.seek(4,1)
  n = data.read(1)
  if n.hex() == "14":
      x = 16
  elif n.hex() == "24":
      x = 32
  elif n.hex() == "34":
      x = 48
  elif n.hex() == "94":
      x = 16 * 9
  else:
      exit(0)
  tagn = tagn + 1
  print("ID Tag      : " + str(tagn))
  print("Panjang Tag : " + n.hex())
  data.seek(5,1)
  ciphertext = data.read(x)
  aes_cipher = AES.new(key[:32], AES.MODE_CBC, iv[:16])
  salida = aes_cipher.decrypt(ciphertext)
  print("Hex 32      : " + salida.hex())
  print("Teks Asli 32: " + salida.decode('ascii'))
  try:
    w = salida.decode('ascii').replace("\x00","",-1)
    b_array = bytearray.fromhex(str(w))
    print("ASCII       : " + b_array.decode())
  except:
    pass
  data.seek(2,1)
  print()
