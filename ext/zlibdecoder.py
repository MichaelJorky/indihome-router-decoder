"""Dekripsi config.bin menjadi config.zlib"""
import argparse

import zcu

from zcu.xcryptors import Xcryptor


def main():
    """fungsi utama"""
    parser = argparse.ArgumentParser(description='Dekripsi config.bin dari Router ZTE',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', type=argparse.FileType('rb'),
                        help='File konfigurasi terenkripsi (config.bin)')
    parser.add_argument('outfile', type=argparse.FileType('wb'),
                        help='File keluaran (config.zlib)')
    parser.add_argument('--key', type=lambda x: x.encode(), default=b'',
                        help="Kunci untuk dekripsi AES")
    args = parser.parse_args()

    key = args.key.ljust(16, b'\0')[:16]

    infile = args.infile
    outfile = args.outfile

    zcu.zte.read_header(infile)
    zcu.zte.read_signature(infile)
    zcu.zte.read_payload(infile)

    decryptor = Xcryptor(key)
    decrypted = decryptor.decrypt(infile)

    outfile.write(decrypted.read())


if __name__ == '__main__':
    main()
