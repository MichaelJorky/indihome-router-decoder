"""Mengambil info dari config.bin"""
import argparse

import zcu


def print_payload_info(infile):
    """berharap berada di awal dari magic payload"""
    zcu.zte.read_header(infile)
    signature = zcu.zte.read_signature(infile)
    payload_header = zcu.zte.read_payload(infile)
    assert payload_header[0] == zcu.constants.PAYLOAD_MAGIC
    payload_start = infile.tell()
    payload_type = payload_header[1]
    if payload_type == 0:
        payload_type_friendly = "(ZLIB)"
    elif payload_type == 1:
        payload_type_friendly = "(ZLIB+CRC)"
    elif payload_type == 2:
        payload_type_friendly = "(ZLIB+AES128ECB)"
    elif payload_type == 3:
        payload_type_friendly = "(ZLIB+AES256CBCSAMEIV)"
    elif payload_type == 4:
        payload_type_friendly = "(ZLIB+AES256CBCDIFFIV)"
    else:
        payload_type_friendly = "(UNKNOWN)"

    payload_length = payload_header[2]
    penultimate_chunk = payload_header[3]
    payload_chunk_size = payload_header[4]
    payload_crc = payload_header[5]
    payload_header_crc = payload_header[6]

    if len(signature) > 0:
        print("Tanda Tangan:         ", signature.decode('utf-8'))

    print("Tipe Payload:      ", payload_type, payload_type_friendly)
    print("Mulai Payload:     ", payload_start)
    print("Ukuran Dekompresi: ", payload_length, "bytes")
    print("Chunk kedua terakhir:    ", penultimate_chunk)
    print("Ukuran Chunk:        ", payload_chunk_size, "bytes")
    print("CRC Payload:       ", payload_crc)
    print("CRC Header:        ", payload_header_crc)


def main():
    """fungsi utama"""
    parser = argparse.ArgumentParser(description='Baca config.bin untuk Router ZTE',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', type=argparse.FileType('rb'),
                        help='File konfigurasi mentah (config.xml)')
    args = parser.parse_args()

    print_payload_info(args.infile)


if __name__ == '__main__':
    main()
