import sys
from io import BytesIO
from io import StringIO
from hashlib import sha256
from Cryptodome.Cipher import AES
import zcu

if len(sys.argv) != 2:
    print("Tidak ada nama file yang diberikan")
    exit(0)
else:
    decfile = sys.argv[1]

plain_key = ''
plain_iv =  ''

print("Kunci Biasa : " + plain_key)
print("IV Biasa    : " + plain_iv)
key = sha256(plain_key.encode("utf8")).digest()
iv = sha256(plain_iv.encode("utf8")).digest()
print("SHA Kunci   : " + key.hex())
print("SHA IV      : " + iv.hex())
aes_cipher = AES.new(key[:32], AES.MODE_CBC, iv[:16])
data = open(decfile,"rb")
data.seek(72)
ciphertext = data.read()
salida = aes_cipher.decrypt(ciphertext)
fileobj = BytesIO(salida)
zcu.zte.read_payload_type(fileobj, raise_on_error=False)
res, _ = zcu.compression.decompress(fileobj)
print(res.read().decode())
