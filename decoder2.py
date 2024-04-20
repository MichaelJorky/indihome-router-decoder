""" Decoder oleh "Dunia MR" Tutorial Lengkap cek Di Channel Youtube https://www.youtube.com/@DuniaMR/videos """
import sys
import argparse
import zcu
import struct
import os
import io
import linecache
from types import SimpleNamespace
from zcu import constants
from zcu.xcryptors import Xcryptor, CBCXcryptor
from zcu.known_keys import serial_keygen, signature_keygen, run_any_keygen, run_all_keygens, run_keygen, tagparams_keygen, mac_to_str, get_all_models, get_all_keys, find_key

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
    
    infile.seek(145)
    remaining_data = infile.read()
    infile = io.BytesIO(remaining_data)

    zcu.zte.read_header(infile)
    signature = zcu.zte.read_signature(infile).decode()
    if signature:
        print(f"Tanda tangan yang terdeteksi: {signature}")
    payload_type = zcu.zte.read_payload_type(infile)
    print(f"Tipe payload yang terdeteksi: {payload_type}")
    start_pos = infile.tell()
    
    params = SimpleNamespace()
    if args.signature: params.signature = args.signature
    else: params.signature = signature
    if args.key: params.key = args.key
    if args.model: params.model = args.model
    if args.serial: params.serial = args.serial if (args.serial != 'NONE') else ''
    if args.mac: params.mac = args.mac if (args.mac != 'NONE') else ''
    if args.longpass: params.longPass = args.longpass if (args.longpass != 'NONE') else ''
    if args.key_prefix: params.key_prefix = args.key_prefix if (args.key_prefix != 'NONE') else ''
    if args.key_suffix: params.key_suffix = args.key_suffix if (args.key_suffix != 'NONE') else ''
    if args.iv_prefix: params.iv_prefix = args.iv_prefix if (args.iv_prefix != 'NONE') else ''
    if args.iv_suffix: params.iv_suffix = args.iv_suffix if (args.iv_suffix != 'NONE') else ''

    matched = None
    if payload_type == 0:
        pass
    elif payload_type == 1:
        pass
    elif payload_type == 2:
        keys = [args.key] if args.key else []
        if not keys and hasattr(params, 'signature'):
            found_key = zcu.known_keys.find_key(params.signature)
            if found_key is not None and found_key not in keys:
                keys.append(found_key)
        if args.try_all_known_keys:
            keys.extend(zcu.known_keys.get_all_keys())

        if not keys:
            error("Tidak ada --key yang ditentukan atau ditemukan melalui tanda tangan, dan tidak mencoba semua kunci yang diketahui!")
            return 1

        for key in keys:
            if len(keys) > 1:
                print(f"Mencoba kunci: {key}")

            decryptor = Xcryptor(key)
            infile.seek(start_pos)
            decrypted = decryptor.decrypt(infile)
            if zcu.zte.read_payload_type(decrypted, raise_on_error=False) is not None:
                matched = f"kunci: '{key}'"
                infile = decrypted
                break

        if matched is None:
            error(f"Gagal mendekripsi payload tipe 2, mencoba {len(keys)} kunci!")
            return 1
    elif payload_type == 3:
        models = [args.model] if args.model else []
        if args.try_all_known_keys:
            models.extend(zcu.known_keys.get_all_models())

        if not models:
            error("Argumen model tidak ditentukan untuk dekripsi tipe 3 dan tidak mencoba semua kunci yang diketahui!")
            return 1

        for model in models:
            if len(models) > 1:
                print(f"Mencoba nama model: {model}")
            decryptor = CBCXcryptor(model)
            infile.seek(start_pos)
            decrypted = decryptor.decrypt(infile)
            if zcu.zte.read_payload_type(decrypted, raise_on_error=False) is not None:
                matched = f"model: '{model}'"
                infile = decrypted
                break

        if matched is None:
            error(f"Gagal mendekripsi payload tipe 3, mencoba {len(models)} nama model!")
            return 1
    elif payload_type == 4:
        generated = []
        if args.try_all_known_keys:
            generated = zcu.known_keys.run_all_keygens(params)
        else:
            res = zcu.known_keys.run_keygen(params)
            if res is not None:
                generated.append(res)

        if not generated:
            errStr = "Tidak ada pembangkit kunci tipe 4 yang cocok dengan tanda tangan dan parameter yang disediakan/deteksi! Mungkin menambahkan --try-all-known-keys "
            if not hasattr(params, 'serial'):
                errStr += "atau --serial "
            errStr += "akan berhasil."
            error(errStr)
            return 1

        for genkey in generated:
            key, iv, source = genkey
            if len(generated) > 1:
                print(f"Mencoba kunci: '{key}' iv: '{iv}' dihasilkan dari {source}")

            decryptor = CBCXcryptor()
            decryptor.set_key(key, iv)
            infile.seek(start_pos)
            decrypted = decryptor.decrypt(infile)
            if zcu.zte.read_payload_type(decrypted, raise_on_error=False) is not None:
                matched = source
                infile = decrypted
                break

        if matched is None:
            error(f"Gagal mendekripsi payload tipe 4, mencoba {len(generated)} kunci yang dihasilkan!")
            return 1
    elif payload_type == 5:
        if args.key is None or args.iv_prefix is None:
            error("Kunci, Awalan Iv Tidak Boleh Kosong" % len(generated))

        print("Awalan Kunci: %s, Awalan Iv: %s" %
              (args.key_prefix, args.iv_prefix))
        decryptor = CBCXcryptor()
        decryptor.set_key(args.key_prefix, args.iv_prefix)
        
        infile.seek(start_pos)
        decrypted = decryptor.decrypt(infile)

        if zcu.zte.read_payload_type(decrypted, raise_on_error=False) is not None:
            matched = True
            infile = decrypted

        if matched is None:
            error("Gagal mendekripsi payload tipe 5, mencoba %d Iv_Prefix Key(s)!" % len(
                args.iv_prefix))
            return 1
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
                raise ValueError("String Alamat Mac Memiliki Panjang Yang Salah")
            mac = bytes.fromhex(mac)
        if len(mac) != 6:
            raise ValueError("Alamat Mac Memiliki Panjang Yang Salah")
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
        print("Mac: %s Awalan Kunci: %s, Awalan Iv: %s" % (mac, kp, iv_prefix))
        decryptor = CBCXcryptor()
        decryptor.set_key(kp, iv_prefix)
        
        infile.seek(start_pos)
        decrypted = decryptor.decrypt(infile)
        if zcu.zte.read_payload_type(decrypted, raise_on_error=False) is not None:
            matched = f"Serial: '{args.serial}'"
            infile = decrypted

        if matched is None:
            error("Gagal mendekripsi payload tipe 6, mencoba %D Iv_Prefix Key(s)!" % len(
                args.iv_prefix))
            return 1
    else:
        error(f"Tipe payload tidak dikenal {payload_type}!")
        return 1

    res, _ = zcu.compression.decompress(infile)
    outfile.write(res.read())

    if matched is not None:
        print(f"Berhasil didekode menggunakan {matched}!")
    else:
        print("Berhasil didekode!")

    return 0

def error(err):
    print(err, file=sys.stderr)

if __name__ == "__main__":
    main()
