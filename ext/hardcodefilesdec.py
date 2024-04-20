import sys
from io import BytesIO
from hashlib import sha256
from Cryptodome.Cipher import AES

# Memeriksa apakah argumen berupa nama file
if len(sys.argv) != 2:
    print("Tidak ada nama file yang diberikan")
    exit(0)
else:
    decfile = sys.argv[1]

plain_key = ''
plain_iv =  ''

# Menampilkan kunci dan IV dalam bentuk plain
print("Kunci Plain : " + plain_key)
print("IV Plain    : " + plain_iv)

# Mengonversi kunci dan IV menjadi SHA256
key = sha256(plain_key.encode("utf8")[:32]).digest()
iv = sha256(plain_iv.encode("utf8")).digest()

# Menampilkan hasil SHA256 dari kunci dan IV
print("SHA Kunci   : " + key.hex())
print("SHA IV      : " + iv.hex())

# Membuat objek AES Cipher
aes_cipher = AES.new(key[:32], AES.MODE_CBC, iv[:16])

# Membuka file dan membaca data
data = open(decfile,"rb")
data.seek(72)
ciphertext = data.read()

# Mendekripsi teks sandi dan menampilkan hasilnya
salida = aes_cipher.decrypt(ciphertext)
print("16 byte pertama: " + salida.hex()[:32]) 
print("Hex 32         : " + salida.hex())
print("Raw 32         : " + str(salida))
