#!/usr/bin/python
import struct
import sys
import argparse
 
import zcu
from zcu import constants
from types import SimpleNamespace
 
#DuniaMR
from zcu.xcryptors import Xcryptor, CBCXcryptor
from zcu.known_keys import serial_keygen, signature_keygen

def main():
    """The Main Function"""
    parser = argparse.ArgumentParser(description="Decode config.bin from ZTE Routers",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("infile", type=argparse.FileType("rb"),
                        help="Encoded configuration file e.g. config.bin")
    parser.add_argument("outfile", type=argparse.FileType("wb"),
                        help="Output file e.g. config.xml")
    parser.add_argument("--key", type=lambda x: x.encode(), default=b"",
                        help="Key for AES decryption")
    parser.add_argument('--file', type=str, default='',
                        help="file")
    parser.add_argument('--model', type=str, default='',
                        help="Device model for Type-3 key derivation")
    parser.add_argument("--serial", type=str, default="",
                        help="Serial number for Type-4 key generation (digimobil routers/tagparams based)")
    parser.add_argument("--mac", type=str, default="",
                        help="MAC address for TagParams-based key generation")
    parser.add_argument("--longpass", type=str, default="",
                        help="Long password from TagParams (entry 4100) for key generation")
    parser.add_argument("--signature", type=str, default="",
                        help="Supply/override signature for Type-4 key generation")
    parser.add_argument("--try-all-known-keys", action="store_true",
                        help="Try decrypting with all known keys and generators (default No)")
    parser.add_argument("--key-prefix", type=str, default='',
                        help="Override Key prefix for Serial/TagParams based key generation")
    parser.add_argument("--iv-prefix", type=str, default='',
                        help="Override IV prefix for Serial/TagParams based key generation")
    parser.add_argument("--key-suffix", type=str, default='',
                        help="Override Key suffix for Signature based key generation")
    parser.add_argument("--iv-suffix", type=str, default='',
                        help="Override IV suffix for Signature based key generation")
    args = parser.parse_args()

    infile = args.infile
    outfile = args.outfile
    #print(constants.ZTE_MAGIC)
    
    header_magic = struct.unpack('>4I', infile.read(16))
    #print(header_magic)
    if header_magic == constants.ZTE_MAGIC:
        header = struct.unpack('>28I', infile.read(112))
    else:
        infile.seek(0)

    #zcu.zte.read_header(infile)
    signature = zcu.zte.read_signature(infile).decode()
    if signature:
        print("Detected Signature: %s" % signature)
    payload_type = zcu.zte.read_payload_type(infile)
    print("Detected Payload Type: %d" % payload_type)
    
    #start_pos = infile.tell()
    
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

    if payload_type == 6:
        if len(args.iv_prefix) == 0:
            iv_prefix = "ZTE%FN$GponNJ025"
        else:
            iv_prefix = args.iv_prefix
        if args.serial is None or args.mac is None:
            error("Serial: %s ,  Mac Cannot Be Null" % (args.serial, args.mac))

        mac = args.mac
        if not isinstance(mac, bytes):
            mac = mac.strip().replace(':', '')
            if len(mac) != 12:
                raise ValueError("Mac Address String Has Wrong Length")
            mac = bytes.fromhex(mac)
        if len(mac) != 6:
            raise ValueError("Mac Address Has Wrong Length")
        mac = "%02x%02x%02x%02x%02x%02x" % (
            mac[5], mac[4], mac[3], mac[2], mac[1], mac[0])

        print("Serial Number Length %s" % len(args.serial))
        if len(args.serial) == 12:
            kp1 = args.serial[4:]
        elif len(args.serial) == 19:
            kp1 = args.serial[11:]
        else:
            raise ValueError("Wrong Serial Number")
        kp = kp1 + mac
        print(" Mac: %s Key_Prefix: %s, Iv_Prefix: %s" % (mac, kp, iv_prefix))
        decryptor = CBCXcryptor()
        decryptor.set_key(kp, iv_prefix)

    elif payload_type == 5:
        if args.key is None or args.iv_prefix is None:
            error("Key, Iv_Prefix Cannot Be Null" % len(generated))

        print("Key_Prefix: %s, Iv_Prefix: %s" %
              (args.key_prefix, args.iv_prefix))
        decryptor = CBCXcryptor()
        decryptor.set_key(args.key_prefix, args.iv_prefix)

    if payload_type == 4:
        generated = []
        if args.try_all_known_keys:
            generated = zcu.known_keys.run_all_keygens(params)
        else:
            res = zcu.known_keys.run_keygen(params)
            if res is not None:
                generated.append(res)

        if not len(generated):
            errStr = "No Type 4 Keygens Matched The Supplied/Detected Signature And Parameters! Maybe Adding --try-all-known-keys "
            if not hasattr(params,'serial'):
                errStr += "or --serial "
            errStr += "would work."
            error(errStr)
            return 1

        for genkey in generated:
            key, iv, source = genkey
            if len(generated) > 1:
                print("Trying Key: '%s' iv: '%s' Generated From %s" % (key, iv, source))

            decryptor = CBCXcryptor()
            decryptor.set_key(key, iv)

    elif payload_type == 3:
        models = []
        if hasattr(params, 'model'):
            models.append(params.model)

        if args.try_all_known_keys:
            models.extend(zcu.known_keys.get_all_models())

        if not len(models):
            error("No Model Argument Specified For Type 3 Decryption And Not Trying All Known Keys!")
            return 1

        for model in models:
            if len(models) > 1:
                print("Trying Model Name: %s" % model)
            decryptor = CBCXcryptor(model)

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
            error("No --key Specified Or Found Via Signature, And Not Trying All Known Keys!")
            return 1

        for key in keys:
            if len(keys) > 1:
                print("Trying Key: %s" % key)

            decryptor = Xcryptor(key)

    start_pos = infile.tell()
    if payload_type in (0, 1, 2, 3, 4, 5, 6):
        print("Has decrypt payload")
        try:
            infile_dec = decryptor.decrypt(infile)
            #print(infile_dec.read().hex()) 
             #try again
            infile_dec.seek(0)
            if zcu.zte.read_payload_type(infile_dec, raise_on_error=False) is None:
                error("Malformed Decrypted Payload, Likely You Used The Wrong Key!")
                return
            infile = infile_dec
        except ValueError as ex:
            error("Failed To Decrypt Payload.")
            return
    else:
        print("No Decrypt Payload")
        pass
    #print(infile.read().hex())
    #infile.seek(0)
    res, _ = zcu.compression.decompress(infile)
    outfile.write(res.read())
    print("Successfully Decoded!")
 
def error(err):
    print(err, file=sys.stderr)
 
if __name__ == "__main__":
    main()
