""" Decoder oleh "Dunia MR" Tutorial Lengkap cek Di Channel Youtube https://www.youtube.com/@DuniaMR/videos """
import struct
import sys
import argparse
import zcu
from zcu import constants
from types import SimpleNamespace
from zcu.xcryptors import Xcryptor, CBCXcryptor
from zcu.known_keys import serial_keygen, signature_keygen

def main():
    parser = argparse.ArgumentParser(description="Dekode config.bin dari Router ZTE", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("infile", type=argparse.FileType("rb"), help="File konfigurasi terenkripsi contoh: config.bin")
    parser.add_argument("outfile", type=argparse.FileType("wb"), help="File output contoh: config.xml")
    parser.add_argument("--key", type=lambda x: x.encode(), default=b"", help="Kunci untuk dekripsi AES")
    parser.add_argument('--file', type=str, default='', help="file")
    parser.add_argument('--model', type=str, default='', help="Model perangkat untuk derivasi kunci Tipe-3")
    parser.add_argument("--serial", type=str, default="", help="Nomor seri untuk pembangkitan kunci Tipe-4 (router digimobil/tagparams berbasis)")
    parser.add_argument("--mac", type=str, default="", help="Alamat MAC untuk pembangkitan kunci berbasis TagParams")
    parser.add_argument("--longpass", type=str, default="", help="Kata sandi panjang dari TagParams (entri 4100) untuk pembangkitan kunci")
    parser.add_argument("--signature", type=str, default="", help="Penyediaan/penggantian tanda tangan untuk pembangkitan kunci Tipe-4")
    parser.add_argument("--try-all-known-keys", action="store_true", help="Coba dekripsi dengan semua kunci dan generator yang diketahui (default Tidak)")
    parser.add_argument("--key-prefix", type=str, default='', help="Mengganti awalan kunci untuk pembangkitan kunci berbasis Serial/TagParams")
    parser.add_argument("--iv-prefix", type=str, default='', help="Mengganti awalan IV untuk pembangkitan kunci berbasis Serial/TagParams")
    parser.add_argument("--key-suffix", type=str, default='', help="Mengganti akhiran kunci untuk pembangkitan kunci berbasis Signature")
    parser.add_argument("--iv-suffix", type=str, default='', help="Mengganti akhiran IV untuk pembangkitan kunci berbasis Signature")
    args = parser.parse_args()

    infile = args.infile
    outfile = args.outfile
    
    header_magic = struct.unpack('>4I', infile.read(16))
    if header_magic == constants.ZTE_MAGIC:
        header = struct.unpack('>28I', infile.read(112))
    else:
        infile.seek(0)

    signature = zcu.zte.read_signature(infile).decode()
    if signature:
        print("Tanda Tangan Yang Terdeteksi: %s" % signature)
    payload_type = zcu.zte.read_payload_type(infile)
    print("Tipe Payload Yang Terdeteksi: %d" % payload_type)
    
    decryptor = CBCXcryptor("")
    if args.mac:
        decryptor.set_key(args.mac)
    if args.serial:
        decryptor.set_key(args.serial)

    params = SimpleNamespace()
    if args.signature:
        params.signature = args.signature
    else:
        params.signature = signature
    
    if args.key:
        params.key = args.key
    if args.model:
        params.model = args.model
    if args.serial:
        params.serial = args.serial if (args.serial != 'NONE') else ''
    if args.mac:
        params.mac = args.mac if (args.mac != 'NONE') else ''
    if args.longpass:
        params.longPass = args.longpass if (args.longpass != 'NONE') else ''
    if args.key_prefix:
        params.key_prefix = args.key_prefix if (args.key_prefix != 'NONE') else ''
    if args.key_suffix:
        params.key_suffix = args.key_suffix if (args.key_suffix != 'NONE') else ''
    if args.iv_prefix:
        params.iv_prefix = args.iv_prefix if (args.iv_prefix != 'NONE') else ''
    if args.iv_suffix:
        params.iv_suffix = args.iv_suffix if (args.iv_suffix != 'NONE') else ''

    matched = None
    if payload_type == 0:
        pass
    elif payload_type == 1:
        pass
    elif payload_type == 2:
        keys = []
        if hasattr(params, 'key'):
            keys.append(params.key)
        elif hasattr(params, 'signature'):
            found_key = zcu.known_keys.find_key(params.signature)
            if (found_key is not None) and (found_key not in keys):
                keys.append(found_key)
        if args.try_all_known_keys:
            for key in zcu.known_keys.get_all_keys():
                if key not in keys:
                    keys.append(key)

        if not len(keys):
            error("Tidak Ada --key yang Ditentukan Atau Ditemukan Melalui Tanda Tangan, dan Tidak Mencoba Semua Kunci yang Diketahui!")
            return 1

        for key in keys:
            if len(keys) > 1:
                print("Mencoba Kunci: %s" % key)

            decryptor = Xcryptor(key)
    elif payload_type == 3:
        models = []
        if hasattr(params, 'model'):
            models.append(params.model)

        if args.try_all_known_keys:
            models.extend(zcu.known_keys.get_all_models())

        if not len(models):
            error("Tidak Ada Argumen Model yang Ditentukan Untuk Dekripsi Tipe 3 dan Tidak Mencoba Semua Kunci yang Diketahui!")
            return 1

        for model in models:
            if len(models) > 1:
                print("Mencoba Nama Model: %s" % model)
            decryptor = CBCXcryptor(model)
    if payload_type == 4:
        generated = []
        if args.try_all_known_keys:
            generated = zcu.known_keys.run_all_keygens(params)
        else:
            res = zcu.known_keys.run_keygen(params)
            if res is not None:
                generated.append(res)

        if not len(generated):
            errStr = "Tidak Ada Pembangkit Kunci Tipe 4 yang Cocok dengan Tanda Tangan dan Parameter yang Diberikan! Mungkin Menambahkan --try-all-known-keys "
            if not hasattr(params,'serial'):
                errStr += "atau --serial "
            errStr += "akan berhasil."
            error(errStr)
            return 1

        for genkey in generated:
            key, iv, source = genkey
            if len(generated) > 1:
                print("Mencoba Kunci: '%s' iv: '%s' yang Dihasilkan Dari: %s" % (key, iv, source))

            decryptor = CBCXcryptor()
            decryptor.set_key(key, iv)
    elif payload_type == 5:
        if args.key is None or args.iv_prefix is None:
            error("Kunci, Iv_Awal Tidak Boleh Kosong" % len(generated))

        print("Kunci_Awal: %s, Iv_Awal: %s" %
              (args.key_prefix, args.iv_prefix))
        decryptor = CBCXcryptor()
        decryptor.set_key(args.key_prefix, args.iv_prefix)
    elif payload_type == 6:
        if len(args.iv_prefix) == 0:
            iv_prefix = "ZTE%FN$GponNJ025"
        else:
            iv_prefix = args.iv_prefix
        if args.serial is None or args.mac is None:
            error("Serial: %s ,  Mac Tidak Boleh Kosong" % (args.serial, args.mac))

        mac = args.mac
        if not isinstance(mac, bytes):
            mac = mac.strip().replace(':', '')
            if len(mac) != 12:
                raise ValueError("String Alamat MAC Memiliki Panjang yang Salah")
            mac = bytes.fromhex(mac)
        if len(mac) != 6:
            raise ValueError("Alamat MAC Memiliki Panjang yang Salah")
        mac = "%02x%02x%02x%02x%02x%02x" % (
            mac[5], mac[4], mac[3], mac[2], mac[1], mac[0])

        print("Panjang Nomor Seri: %s" % len(args.serial))
        if len(args.serial) == 12:
            kp1 = args.serial[4:]
        elif len(args.serial) == 19:
            kp1 = args.serial[11:]
        else:
            raise ValueError("Nomor Seri Salah")
        kp = kp1 + mac
        print("MAC: %s Kunci_Awal: %s, Iv_Awal: %s" % (mac, kp, iv_prefix))
        decryptor = CBCXcryptor()
        decryptor.set_key(kp, iv_prefix)
            
    start_pos = infile.tell()
    if payload_type in (0, 1, 2, 3, 4, 5, 6):
        print("Memiliki Payload Yang Dapat Didekripsi")
        try:
            infile_dec = decryptor.decrypt(infile)
            infile_dec.seek(0)
            if zcu.zte.read_payload_type(infile_dec, raise_on_error=False) is None:
                error("Payload yang Didekripsi Tidak Tepat, Kemungkinan Anda Menggunakan Kunci yang Salah!")
                return
            infile = infile_dec
        except ValueError as ex:
            error("Gagal Mendekripsi Payload.")
            return
    else:
        print("Tidak Ada Payload Dekripsi")
        pass
    res, _ = zcu.compression.decompress(infile)
    outfile.write(res.read())
    print("Berhasil Didekode!")

def error(err):
    print(err, file=sys.stderr)

if __name__ == "__main__":
    main()
