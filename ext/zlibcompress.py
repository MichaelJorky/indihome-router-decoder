"""Mengompres config.xml menjadi config.zlib"""
import argparse

import zcu


def main():
    """fungsi utama"""
    parser = argparse.ArgumentParser(description='Mengompres config.xml dari Router ZTE',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', type=argparse.FileType('rb'),
                        help='File konfigurasi mentah (config.xml)')
    parser.add_argument('outfile', type=argparse.FileType('wb'),
                        help='File output (config.zlib)')
    args = parser.parse_args()

    infile = args.infile
    outfile = args.outfile

    compressed = zcu.compression.compress(infile, 65536)

    outfile.write(compressed.read())


if __name__ == '__main__':
    main()
