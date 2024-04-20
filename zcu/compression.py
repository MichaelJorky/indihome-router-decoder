"""Fungsi pembantu kompresi dan dekompresi"""

import struct
import zlib
from io import BytesIO

from . import constants


def decompress(infile):
    """Mendekompresi sebuah blok, mengembalikan data dan crc
    Sebuah 'blok' terdiri dari header 12 byte (3x4-byte INT) dan payload ZLIB
    HEADER
        [XXXX] Panjang blok yang telah didekompresi (bytes)
        [XXXX] Panjang blok yang terkompresi (bytes)
        [XXXX] 0 jika blok terakhir selain itu kumulatif panjang blok terkompresi
    PAYLOAD
        [....] Potongan ZLIB
    """
    decompressed_data = BytesIO()
    crc = 0
    while True:
        aes_header = struct.unpack('>3I', infile.read(12))
        decompressed_length = aes_header[0]
        compressed_length = aes_header[1]
        compressed_chunk = infile.read(compressed_length)
        crc = zlib.crc32(compressed_chunk, crc)
        decompressed_chunk = zlib.decompress(compressed_chunk)
        assert decompressed_length == len(decompressed_chunk)
        decompressed_data.write(decompressed_chunk)
        if aes_header[2] == 0:
            break
    decompressed_data.seek(0)
    return (decompressed_data, crc)


def compress_helper(infile, chunk_size):
    """Fungsi pembantu kompresi, mengonsumsi segmen-segmen ukuran chunk_size dari infile"""
    # panjang terkompresi kumulatif termasuk header payload 60-byte
    # ini adalah jumlah kumulatif byte yang terkompresi TIDAK TERMASUK blok terakhir
    cumulative_compressed_length = 60
    total_uncompressed_length = 0
    crc = 0

    compressed_data = BytesIO()
    while True:
        data = infile.read(chunk_size)
        uncompressed_length = len(data)
        if uncompressed_length == 0:
            break

        total_uncompressed_length += uncompressed_length

        compressed_chunk = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
        crc = zlib.crc32(compressed_chunk, crc) & 0xffffffff

        if uncompressed_length < chunk_size:
            more_chunks = 0
        else:
            # increment cumulative length if not last block
            cumulative_compressed_length += len(compressed_chunk) + 12
            more_chunks = cumulative_compressed_length

        chunk_header = struct.pack('>3I',
                                   uncompressed_length,
                                   len(compressed_chunk),
                                   more_chunks)

        compressed_data.write(chunk_header)
        compressed_data.write(compressed_chunk)

    compressed_data.seek(0)
    stats = {
        'crc': crc,
        'uncompressed_size': total_uncompressed_length,
        'compressed_size': cumulative_compressed_length,
    }

    if chunk_size < 65536: # ingin ukuran terkompresi penuh di header dalam beberapa kasus
        stats['compressed_size'] += len(compressed_chunk) + 12

    return (compressed_data, stats)


def compress(infile, chunk_size):
    """Mengompres dan menambahkan header

    Sebuah 'blok' terdiri dari header 60 byte (15x4-byte INT) diikuti oleh
    >=1 PAYLOAD section(s).

    HEADER
        [XXXX] Angka magis '0x04030201'
        [XXXX] Tipe payload, 0 = ZLIB
        [XXXX] Total panjang yang sudah didekompresi
        [XXXX] Ukuran terkompresi kumulatif* (*tidak selalu)
        [XXXX] Ukuran chunk yang telah didekompresi
        [XXXX] CRC dari data terkompresi
        [XXXX] CRC dari 24 byte pertama header
        [XXXX....] 32 byte padding
    PAYLOAD
        HEADER
            12 byte header
        ZLIB
            payload byte variabel
    """
    compressed_data, stats = compress_helper(infile, chunk_size)

    header = struct.pack('>6I',
                         constants.PAYLOAD_MAGIC,
                         0,  # tidak ada enkripsi, hanya kompresi zlib
                         stats['uncompressed_size'],
                         stats['compressed_size'],
                         chunk_size,
                         stats['crc'])
    payload = BytesIO()
    payload.write(header)
    payload.write(struct.pack('>I', zlib.crc32(header) & 0xffffffff))
    payload.write(struct.pack('>8I', *(0, 0, 0, 0, 0, 0, 0, 0)))
    payload.write(compressed_data.read())
    payload.seek(0)

    return payload
