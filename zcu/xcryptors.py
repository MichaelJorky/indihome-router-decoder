import struct
from io import BytesIO
from hashlib import sha256

from Cryptodome.Cipher import AES

from zcu.constants import PAYLOAD_MAGIC

class Xcryptor():
    """Enkripsi Tipe 2 Standar"""
    aes_cipher = None
    force_same_data_length = True

    def __init__(self, aes_key=None, chunk_size=65536, include_unencrypted_length=False):
        self.chunk_size = chunk_size
        self.include_unencrypted_length = include_unencrypted_length
        self.set_key(aes_key)

    def set_key(self, aes_key):
        if aes_key is None:
            self.aes_cipher = None
            return

        if not isinstance(aes_key, bytes):
            aes_key = aes_key.encode()

        aes_key = aes_key.ljust(16, b"\0")[:16]
        self.aes_cipher = AES.new(aes_key, AES.MODE_ECB)

    def read_chunks(self, infile):
        """membaca blok yang terenkripsi
        Sebuah 'blok' terdiri dari header 12 byte (3x4-byte INT) dan payload AES
        HEADER
            [XXXX] Panjang terdekripsi
            [XXXX] Panjang terenkripsi
            [XXXX] 0
        PAYLOAD
            [....] Chunks ZLIB
        """
        encrypted_data = BytesIO()
        total_dec_size = 0
        while True:
            chunk_size, dec_size, more_chunks = struct.unpack(">3I", infile.read(12))
            encrypted_data.write(infile.read(chunk_size))
            total_dec_size += dec_size
            if more_chunks == 0:  # tanda "lanjut" tidak diatur
                break
        encrypted_data.seek(total_dec_size)
        return encrypted_data

    def decrypt(self, infile):
        data = self.read_chunks(infile)
        data_size = data.tell()
        data.seek(0)
        res = BytesIO()
        res.write(self.aes_cipher.decrypt(data.read())[:data_size])
        res.seek(0)
        return res

    def create_header(self):
        unencrypted_length_to_use = 0
        if self.include_unencrypted_length:
            unencrypted_length_to_use = self.unencrypted_data_length
            if self.force_same_data_length:
                unencrypted_length_to_use = self.encrypted_data_length;

        header = struct.pack(
            ">6I",
            PAYLOAD_MAGIC,
            2,  # aes128 dalam mode ECB
            unencrypted_length_to_use,
            self.encrypted_data_length + 60 + 12,
            self.chunk_size,
            0)
        return header

    def encrypt(self, infile):
        """enkripsi dan tambahkan header

        Sebuah 'blok' terdiri dari header 60 byte (15x4-byte INT) diikuti oleh
        satu PAYLOAD section.

        HEADER
            [XXXX] Nomor Sihir '0x01020304'
            [XXXX] Tipe Payload, 2 = AES128ECB, 3 = AES256CBC(IV==Key), 4 = AES256CBC(IV!=Key)
            [XXXX] Panjang tidak terenkripsi
            [XXXX] ukuran 'blok' (termasuk header)
            [XXXX] ukuran Chunks
            [XXXX....] 40 byte padding
        PAYLOAD
            HEADER
                12 byte header
            AES
                'chunk size' payload
        """

        data = infile.read()

        unencrypted_data_length = len(data)
        self.unencrypted_data_length = unencrypted_data_length

        # diisi hingga perataan 16 byte
        if unencrypted_data_length % 16 > 0:
            data = data + (16 - unencrypted_data_length % 16)*b"\0"

        encrypted_data = self.aes_cipher.encrypt(data)
        encrypted_data_length = len(encrypted_data)
        self.encrypted_data_length = encrypted_data_length

        header = self.create_header()

        result = BytesIO()
        result.write(header)
        # 36 byte padding
        result.write(struct.pack(">9I", *(9 * [0])))
        # mini header untuk payload aes
        aes_header = struct.pack(
            ">3I",
            *(encrypted_data_length if self.force_same_data_length else unencrypted_data_length,
              encrypted_data_length,
              0)
        )
        result.write(aes_header)
        result.write(encrypted_data)
        result.seek(0)
        return result


class CBCXcryptor(Xcryptor):
    # enkripsi tipe 3/4, AES256CBC dengan kunci/IV yang ditetapkan dari hash SHA256
    force_same_data_length = False
    aes_key_str = None
    aes_iv_str = None

    def set_key(self, aes_key=None, aes_iv=None):
        if aes_key is None:
            self.aes_cipher = None
            return

        if isinstance(aes_key, bytes):
            self.aes_key_str = aes_key.decode()
        else:
            self.aes_key_str = aes_key

        if aes_iv is None:
            self.aes_iv_str = self.aes_key_str
        elif isinstance(aes_iv, bytes):
            self.aes_iv_str = aes_iv.decode()
        else:
            self.aes_iv_str = aes_iv

        key = sha256(self.aes_key_str.encode()).digest()
        iv = sha256(self.aes_iv_str.encode()).digest()
        self.aes_cipher = AES.new(key, AES.MODE_CBC, iv[:16])

    def read_chunks(self, infile):
        encrypted_data = BytesIO()
        total_dec_size = 0
        while True:
            dec_size, chunk_size, more_data = struct.unpack(">3I", infile.read(12))
            encrypted_data.write(infile.read(chunk_size))
            total_dec_size += dec_size
            if more_data == 0:
                break
        encrypted_data.seek(total_dec_size)
        return encrypted_data

    def create_header(self):
        header = struct.pack(
            ">6I",
            PAYLOAD_MAGIC,
            3 if (self.aes_key_str == self.aes_iv_str) else 4,  # aes dalam mode CBC
            self.encrypted_data_length if self.include_unencrypted_length else 0,
            0,
            0,
            0)
        return header
