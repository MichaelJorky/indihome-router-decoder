"""Berbagai fungsi pembantu untuk membaca/menulis konfigurasi ZTE"""

from io import BytesIO
from os import stat
import struct

from . import constants

def read_header(infile, little_endian=False):
    """Mengharapkan berada pada posisi 0 dari file, mengembalikan ukuran header"""
    header_magic = struct.unpack('>4I', infile.read(16))
    if header_magic == constants.ZTE_MAGIC:
        # 128 byte header
        endian = '<' if little_endian else '>'
        header = struct.unpack(endian + '28I', infile.read(112))
        assert header[2] == 4
        header_length = header[13]
        signed_config_size = header[14]
        file_size = stat(infile.name).st_size
        assert header_length + signed_config_size == file_size, "ukuran file tidak cocok dengan header"
    else:
        # tidak ada header tambahan sehingga kembali ke awal file
        infile.seek(0)
    return infile.tell()


def read_signature(infile):
    """Mengharapkan berada di awal tanda tangan magic, mengembalikan
    (tanda tangan, byte yang dibaca)"""
    signature_header = struct.unpack('>3I', infile.read(12))
    signature = b''
    if signature_header[0] == constants.SIGNATURE_MAGIC:
        # _ = signature_header[1] # 0 ?
        signature_length = signature_header[2]
        signature = infile.read(signature_length)
    else:
        # tidak ada tanda tangan sehingga kembali ke awal file
        infile.seek(0)
    return signature


def read_payload(infile, raise_on_error=True):
    """Mengharapkan berada di awal payload magic"""
    payload_header = struct.unpack('>15I', infile.read(60))
    if payload_header[0] != constants.PAYLOAD_MAGIC:
        if raise_on_error:
            raise ValueError("Header payload tidak dimulai dengan payload magic.")
        else:
            return None
    return payload_header


def read_payload_type(infile, raise_on_error=True):
    """Mengharapkan berada di awal payload magic"""
    payload_header = read_payload(infile, raise_on_error)
    return payload_header[1] if payload_header is not None else None


# TODO: memisahkan fungsionalitas 'add_signature'
def add_header(payload, signature, version, include_header=False, little_endian=False):
    """Membuat payload 'penuh' dari (header), tanda tangan, dan payload"""
    full_payload = BytesIO()
    signature_length = len(signature)

    payload_data = payload.read()

    if include_header:
        full_payload_length = len(payload_data)
        if signature_length > 0:
            full_payload_length += 12 + signature_length
        full_payload.write(struct.pack('>4I', *constants.ZTE_MAGIC))
        header = [
            0, 0, 4, 0,
            0, 0, 0, 0,
            0, 0, 0, 64,
            version, 128, full_payload_length, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
        ]
        endian = '<' if little_endian else '>'
        full_payload.write(struct.pack(endian + '28I', *header))

    if signature_length > 0:
        signature_header = [
            constants.SIGNATURE_MAGIC,
            0,
            signature_length,
        ]
        full_payload.write(struct.pack('>3I', *signature_header))
        full_payload.write(signature)

    full_payload.write(payload_data)
    full_payload.seek(0)

    return full_payload
