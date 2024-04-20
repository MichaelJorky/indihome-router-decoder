import hashlib
import re
import struct
import sys
import zlib

from argparse import ArgumentParser, ArgumentTypeError, FileType
from io import BytesIO

try:
	from Crypto.Cipher import AES
except:
	print('Perpustakaan "pycryptodome" tidak ditemukan.', file=sys.stderr)
	print('Silakan install menggunakan "pip install pycryptodome" sebelum menjalankan alat ini.', file=sys.stderr)
	exit(1)

# Putar kanan 32-bit
def rotr32(a, c):
    return ((a >> c) | (a << (32 - c))) & 0xFFFFFFFF

ROUND_CONSTANTS = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

def _sha256_raw_digest(message):
    """Memproses pesan SHA-256 yang sudah dipad"""
    digest = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]
    for chunk in range(0, len(message), 64):
        chunk = message[chunk : chunk + 64]
        w = list(struct.unpack('>' + 'I' * 16, chunk))
        for i in range(16, 64):
            s0 = rotr32(w[-15], 7) ^ rotr32(w[-15], 18) ^ (w[-15] >> 3)
            s1 = rotr32(w[-2], 17) ^ rotr32(w[-2], 19) ^ (w[-2] >> 10)
            w.append((w[-16] + s0 + w[-7] + s1) & 0xFFFFFFFF)
        a, b, c, d, e, f, g, h = digest
        for r_w, r_k in zip(w, ROUND_CONSTANTS):
            S1 = rotr32(e, 6) ^ rotr32(e, 11) ^ rotr32(e, 25)
            ch = (e & f) ^ ((e ^ 0xFFFFFFFF) & g)
            temp1 = (h + S1 + ch + r_k + r_w)
            S0 = rotr32(a, 2) ^ rotr32(a, 13) ^ rotr32(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj)
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF
        digest = [(x + y) & 0xFFFFFFFF for x, y in zip(digest, (a, b, c, d, e, f, g, h))]
    return struct.pack('>' + 'I' * 8, *digest)

def buggy_sha256(message):
    """
    Fungsi ini mengimplementasikan fungsi SHA-256 yang bermasalah yang tersedia di
    https://github.com/ilvn/SHA256/blob/d8d69dbfeeb68f31e74f8e24971332e996eed76b/mark2/sha256.c,
    pada komit tertentu.

    Fungsi ini digunakan oleh router ZTE Z3600P dalam perpustakaan libsha256.so, untuk
    mendapatkan kunci enkripsi dan IV konfigurasi.
    """
    last_chunk_len = len(message) % 64
    if last_chunk_len <= 55:
        return hashlib.sha256(message).digest()
    packed_len = struct.pack('>Q', 8 * len(message))
    if last_chunk_len == 56:
        return _sha256_raw_digest(message + packed_len)
    message += b'\x80' + b'\x00' * (64 - last_chunk_len - 1)
    message += message[-64 : -8] + packed_len
    return _sha256_raw_digest(message)

def chunk_reader(fin):
	has_next = True
	while has_next:
		header = fin.read(12)
		if len(header) != 12:
			raise IOError('Gagal membaca header chunk terenkripsi')
		unpacked_size, packed_size, has_next = struct.unpack('>III', header)
		chunk = fin.read(packed_size)
		if len(chunk) != packed_size:
			raise IOError('Gagal membaca konten chunk terenkripsi')
		yield chunk

def parse_serial(serial):
	serial = serial.upper()
	if not re.match(r'^ZTE[A-Z0-9]{8,32}$', serial):
		raise ArgumentTypeError('Serial tidak valid')
	return serial

def parse_mac(mac):
	mac = re.sub(r'[ :-]', '', mac).lower()
	if not re.match(r'^[0-9a-f]{12}$', mac):
		raise ArgumentTypeError('Alamat MAC tidak valid')
	return ':'.join([mac[0:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:12]])

def parse_password(pwd):
	if len(pwd) != 32:
		raise ArgumentTypeError('Kata sandi tidak valid - harus terdiri dari 32 karakter')
	return pwd

parser = ArgumentParser(
	description='Enkoder/decoder konfigurasi ZTE H3600P',
)
parser.add_argument('-e', '--encode', help='Konversi dari XML ke biner.', action='store_true')
parser.add_argument('-d', '--decode', help='Konversi dari biner ke XML.', action='store_true')

parser.add_argument('-s', '--serial', help="Nomor serial perangkat", type=parse_serial)
parser.add_argument('-m', '--mac', help="Alamat MAC perangkat", type=parse_mac)
parser.add_argument('-p', '--password', help="Frasa sandi enkripsi perangkat", type=parse_password)

parser.add_argument('input', help='File masukan. Default ke stdin.', nargs='?', type=FileType('rb'), default=sys.stdin.buffer)
parser.add_argument('output', help='File keluaran. Default ke stdout.', nargs='?', type=FileType('wb'), default=sys.stdout.buffer)

parser.add_argument('--decrypt-only', help='Hanya lakukan dekripsi, tanpa dekompresi.', action='store_true')
parser.add_argument('--compress-only', help='Hanya kompres, tanpa enkripsi.', action='store_true')

args = parser.parse_args()

if not (args.encode ^ args.decode):
	print('Harus melakukan enkode atau dekode.', file=sys.stderr)
	exit(1)

if args.decode:
	if not args.password or not args.mac or not args.serial:
		print('Serial, MAC, atau kata sandi hilang yang diperlukan untuk dekripsi', file=sys.stderr)
		exit(0)

	key = args.password + args.serial + 'Mcd5c46e'
	key = buggy_sha256(key.encode('ascii'))

	iv = 'G21b667b' + args.mac + args.password
	iv = buggy_sha256(iv.encode('ascii'))[:16]

	print('Kunci yang dihasilkan:', file=sys.stderr)
	print(f'  - Kunci AES: {key.hex()}', file=sys.stderr)
	print(f'  - IV AES:    {iv.hex()}', file=sys.stderr)

	print('Dekripsi dimulai', file=sys.stderr)

	header = args.input.read(0x3C)
	if len(header) != 0x3C:
		print('Tidak dapat membaca header file terenkripsi', file=sys.stderr)
		exit(1)

	magic, fmt = struct.unpack('>II', header[0:8])
	if magic != 0x01020304 or fmt != 4:
		print('Header file terenkripsi salah', file=sys.stderr)
		exit(1)

	compressed_config = args.output if args.decrypt_only else BytesIO()
	try:
		for chunk in chunk_reader(args.input):
			print(f' - Chunk: {len(chunk)} byte', file=sys.stderr)
			chunk = AES.new(key, AES.MODE_CBC, iv=iv).decrypt(chunk)
			compressed_config.write(chunk)
	except Exception as e:
		print(f'Kesalahan saat mendekripsi file: {e}', file=sys.stderr)
		exit(1)

	if not args.decrypt_only:
		compressed_config.seek(0)

		print('Dekompresi dimulai', file=sys.stderr)

		header = compressed_config.read(0x3C)
		if len(header) != 0x3C:
			print('Tidak dapat membaca header file terkompresi', file=sys.stderr)
			exit(1)

		magic, fmt, dec_size, _, _, correct_crc, header_crc = struct.unpack('>IIIIIII', header[0:28])
		if magic != 0x01020304 or fmt != 0:
			print('Header file terkompresi salah. Apakah kunci AES benar?', file=sys.stderr)
			exit(1)

		if zlib.crc32(header[0:24]) != header_crc:
			print('CRC header file terkompresi buruk. Apakah kunci AES benar?', file=sys.stderr)
			exit(1)

		total_size = 0
		calculated_crc = 0
		try:
			for chunk in chunk_reader(compressed_config):
				print(f' - Chunk: {len(chunk)} byte', file=sys.stderr)
				calculated_crc = zlib.crc32(chunk, calculated_crc)
				chunk = zlib.decompress(chunk)
				total_size += len(chunk)
				args.output.write(chunk)
		except Exception as e:
			print(f'Kesalahan saat mendekompresi file: {e}', file=sys.stderr)
			exit(1)

		print(f'Panjang yang diharapkan: {dec_size}, panjang yang diproses: {total_size}', file=sys.stderr)
		if total_size != dec_size:
			print('Dekompresi gagal - ukuran tidak sesuai', file=sys.stderr)
			exit(1)

		print(f'CRC yang diharapkan: {correct_crc:08x}, CRC yang dihitung: {calculated_crc:08x}', file=sys.stderr)
		if correct_crc != calculated_crc:
			print('Dekompresi gagal - CRC buruk', file=sys.stderr)
			exit(1)
else:
	print('Kompresi dimulai', file=sys.stderr)

	plain = args.input.read()
	compressed = zlib.compress(plain, level=9)
	print(f'Dikompresi dari {len(plain)} menjadi {len(compressed)} byte', file=sys.stderr)

	calculated_crc = zlib.crc32(compressed)
	print(f'CRC data: {calculated_crc:08x}', file=sys.stderr)

	header = struct.pack('>IIIIII',
		0x01020304,		# Magic (diperiksa)
		0,				# Versi (diperiksa)
		len(plain),		# Panjang tidak terkompresi (diabaikan)
		len(compressed),# Panjang terkompresi (diabaikan)
		len(plain),		# Memori yang diperlukan per chunk (digunakan untuk malloc)
		calculated_crc	# CRC data (diperiksa)
	)

	header_crc = zlib.crc32(header)
	print(f'CRC header: {header_crc:08x}', file=sys.stderr)
	header += struct.pack('>I', header_crc) + b'\x00' * (0x3C - 28)

	chunk = struct.pack('>III', len(plain), len(compressed), 0) + compressed

	result = header + chunk

	args.output.write(result)

print('Operasi berhasil', file=sys.stderr)
