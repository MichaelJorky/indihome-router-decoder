"""Ekstrak teks tanda tangan dari config.bin"""
import argparse

import zcu


def main():
    """fungsi utama"""
    parser = argparse.ArgumentParser(description='Ekstrak tanda tangan dari config.bin Router ZTE',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', type=argparse.FileType('rb'),
                        help='File konfigurasi (config.bin)')

    args = parser.parse_args()

    zcu.zte.read_header(args.infile)
    signature = zcu.zte.read_signature(args.infile)
    print(signature.decode('utf-8'))


if __name__ == '__main__':
    main()
