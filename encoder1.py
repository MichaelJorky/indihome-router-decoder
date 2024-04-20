""" Encoder oleh "Dunia MR" Tutorial Lengkap cek Di Channel Youtube https://www.youtube.com/@DuniaMR/videos """
import os
import sys
import io
import argparse
import linecache
from types import SimpleNamespace
import zcu
from zcu.xcryptors import Xcryptor, CBCXcryptor
from zcu.known_keys import run_any_keygen

def main():
    parser = argparse.ArgumentParser(description='Encode config.bin untuk Router ZTE', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', type=argparse.FileType('rb'), help='File konfigurasi mentah contohnya config.xml')
    parser.add_argument('outfile', type=argparse.FileType('wb'), help='File keluaran contohnya config.bin')
    parser.add_argument('--key', type=lambda x: x.encode(), default=b'', help="Kunci untuk enkripsi AES")
    parser.add_argument('--file', type=str, default='', help="file")
    parser.add_argument('--model', type=str, default='', help="Generate Kunci/IV dari nama model, mengimplikasikan tipe muatan 3")
    parser.add_argument('--serial', type=str, default='', help="Generate Kunci/IV dari nomor seri (router DIGImobil), mengimplikasikan tipe muatan 4")
    parser.add_argument("--mac", type=str, default="", help="Alamat MAC untuk generasi kunci berbasis TagParams")
    parser.add_argument("--longpass", type=str, default="", help="Kata sandi panjang dari TagParams (entri 4100) untuk generasi kunci")
    parser.add_argument('--signature', type=str, default='', help='String tanda tangan perangkat untuk penandatanganan, contoh "ZXHN F670L V9.0"')
    parser.add_argument("--try-all-known-keys", action="store_true", help="Coba dekripsi dengan semua kunci dan generator yang diketahui (default Tidak)")  
    parser.add_argument('--iv', type=lambda x: x.encode(), default=b'', help="IV untuk turunan kunci, beralih mode enkripsi ke AES256CBC")
    parser.add_argument('--use-signature-encryption', action='store_true', help='Generate Kunci/IV dari tanda tangan, mengimplikasikan tipe muatan 4. Gunakan ini jika Anda menggunakan --signature saat mendekode, atau output skrip dekode mengatakan "Menggunakan tanda tangan: <sesuatu>".')
    parser.add_argument('--chunk-size', type=int, default=65536, help='Ukuran potongan ZLIB (default 65536)')
    parser.add_argument('--payload-type', type=int, default=0, choices=[0, 1, 2, 3, 4, 5, 6], help='Tipe muatan (0=plain, 2=enkripsi kunci aes128ecb, 3=enkripsi model aes256cbc, 4=enkripsi tanda tangan/nomor seri aes256cbc)')
    parser.add_argument('--version', type=int, default=2, choices=[1, 2], help='Versi muatan (1=unknown, 2=unknown)')
    parser.add_argument("--include-header", action="store_true", help="Sertakan header? (default Tidak)")
    parser.add_argument("--little-endian-header", action="store_true", help="Apakah header little endian? (default Tidak)")
    parser.add_argument('--include-unencrypted-length', action='store_true', help='Sertakan panjang yang tidak terenkripsi dalam header (default Tidak)')
    parser.add_argument("--key-prefix", type=str, default='', help="Override awalan Kunci untuk generasi kunci berbasis Serial")
    parser.add_argument("--iv-prefix", type=str, default='', help="Override awalan IV untuk generasi kunci berbasis Serial")
    parser.add_argument("--key-suffix", type=str, default='', help="Override akhiran Kunci untuk generasi kunci berbasis Tanda tangan")
    parser.add_argument("--iv-suffix", type=str, default='', help="Override akhiran IV untuk generasi kunci berbasis Tanda tangan")

    args = parser.parse_args()

    infile = args.infile
    outfile = args.outfile
    key = args.key
    iv = args.iv
    payload_type = args.payload_type
    
    if args.model:
        payload_type = 3
        key = args.model
        iv = None
        
    elif args.serial:
        payload_type = 4
        params = SimpleNamespace(signature = args.signature, serial = args.serial)
        print("Menggunakan nomor seri: %s" % params.serial)
        if args.key_prefix:
            params.key_prefix = args.key_prefix if (args.key_prefix != 'NONE') else ''
            print("Menggunakan awalan kunci: %s" % params.key_prefix)
        if args.iv_prefix:
            params.iv_prefix = args.iv_prefix if (args.iv_prefix != 'NONE') else ''
            print("Menggunakan awalan IV: %s" % params.iv_prefix)
        key, iv = run_any_keygen(params,'serial')[:2]
    elif args.use_signature_encryption:
        payload_type = 4
        if not args.signature:
            print("Peringatan: Menggunakan enkripsi tanda tangan tapi tidak ada tanda tangan yang diberikan!")

        params = SimpleNamespace(signature=args.signature)
        print("Menggunakan tanda tangan: %s" % params.signature)
        if args.key_suffix:
            params.key_suffix = args.key_suffix if (args.key_suffix != 'NONE') else ''
            print("Menggunakan akhiran kunci: %s" % params.key_suffix)
        if args.iv_suffix:
            params.iv_suffix = args.iv_suffix if (args.iv_suffix != 'NONE') else ''
            print("Menggunakan akhiran IV: %s" % params.iv_suffix)     
        key, iv = run_any_keygen(params,'signature')[:2]

    elif args.iv:
        payload_type = 4
    elif args.key:
        payload_type = 2

    signature = args.signature
    if not key and signature:
        possible_key = zcu.known_keys.find_key(signature)
        if possible_key is not None:
            key = possible_key
            payload_type = 2
        if key:
            print("Menggunakan kunci '" + key + "' yang cocok dengan tanda tangan '" + signature + "'")

    if all(b == 0 for b in signature) and payload_type in (2, 4):
        print("Peringatan: Tidak ada tanda tangan yang diberikan!")

    if all(b == 0 for b in key) and (payload_type != 0 or signature):
        print("Peringatan: Tidak ada kunci yang diberikan!")

    data = zcu.compression.compress(infile, args.chunk_size)

    if payload_type == 2:
        encryptor = Xcryptor(key, chunk_size=args.chunk_size, include_unencrypted_length=args.include_unencrypted_length)
        data = encryptor.encrypt(data)
    elif payload_type in (3, 4):
        encryptor = CBCXcryptor(chunk_size=args.chunk_size, include_unencrypted_length=args.include_unencrypted_length)
        encryptor.set_key(aes_key=key, aes_iv=iv)
        data = encryptor.encrypt(data)

    version = (args.version >> 16) if args.little_endian_header else (args.version << 16)
    encoded = zcu.zte.add_header(
        data,
        signature.encode("utf8"),
        version,
        include_header=args.include_header,
        little_endian=args.little_endian_header,
    )
    outfile.write(encoded.read())
    print("Selesai!")


if __name__ == '__main__':
    main()
