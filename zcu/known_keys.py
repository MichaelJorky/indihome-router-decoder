"""Kunci enkripsi yang diketahui untuk file config.bin router ZTE"""

# Elemen pertama adalah kunci, yang lain adalah awal dari tanda tangan
KNOWN_KEYS = {
    "MIK@0STzKpB%qJZe": ["zxhn h118n e"],
    "MIK@0STzKpB%qJZf": ["zxhn h118n v"],
    "402c38de39bed665": ["zxhn h267a"],
    "Q#Zxn*x3kVLc":     ["zxhn h168n v2"],
    # karena bug, aslinya "Wj%2$CjM"
    "Wj":               ["zxhn h298n"],
    "m8@96&ZG3Nm7N&Iz": ["zxhn h298a"],
    "GrWM2Hz&LTvz&f^5": ["zxhn h108n"],
    "GrWM3Hz&LTvz&f^9": ["zxhn h168n v3", "zxhn h168n h"],
    "Renjx%2$CjM":      ["zxhn h208n", "zxv10 h201l"],
    "tHG@Ti&GVh@ql3XN": ["zxhn h267n"],
    # tidak yakin, mungkin terkait dengan H108N
    "SDEwOE5WMi41Uk9T": ["TODO"]
}


def find_key(signature):
    signature = signature.lower()
    for key, sigs in KNOWN_KEYS.items():
        for sig in sigs:
            if signature.startswith(sig):
                return key
    return None


def get_all_keys():
    return KNOWN_KEYS.keys()

KNOWN_MODELS = ["H268Q", "H298Q", "H188A", "H288A"]

def get_all_models():
    return KNOWN_MODELS

def mac_to_str(mac):
    if not len(mac):
        return ''
    if not isinstance(mac, bytes):
        mac = mac.strip().replace(':','')
        if len(mac) != 12:
            raise ValueError("String alamat MAC memiliki panjang yang salah")
        mac = bytes.fromhex(mac)
    if len(mac) != 6:
        raise ValueError("Alamat MAC memiliki panjang yang salah")

    return "%02x:%02x:%02x:%02x:%02x:%02x" % (mac[0], mac[1], mac[2], mac[3], mac[4], mac[5])

def tagparams_keygen(params, key_prefix='Mcd5c46e', iv_prefix='G21b667b'):
    if hasattr(params, 'key_prefix'):
        key_prefix = params.key_prefix
    if hasattr(params, 'iv_prefix'):
        iv_prefix = params.iv_prefix

    try:
        macStr = mac_to_str(params.mac)
        key = params.longPass + params.serial + key_prefix
        iv = iv_prefix + macStr + params.longPass
        return (key, iv, "tagparams: mac='%s', serial='%s', longPass='%s'" % (macStr, params.serial, params.longPass))
    except AttributeError:
        return ()

def serial_keygen(params, key_prefix='8cc72b05705d5c46', iv_prefix='667b02a85c61c786'):
    if hasattr(params, 'key_prefix'):
        key_prefix = params.key_prefix
    if hasattr(params, 'iv_prefix'):
        iv_prefix = params.iv_prefix

    try:
        key = key_prefix + params.serial
        iv = iv_prefix + params.serial
        return (key, iv, "serial: '%s'" % params.serial)
    except AttributeError:
        return ()

def signature_keygen(params, key_suffix='Key02721401', iv_suffix='Iv02721401'):
    if hasattr(params, 'key_suffix'):
        key_suffix = params.key_suffix
    if hasattr(params, 'iv_suffix'):
        iv_suffix = params.iv_suffix

    try:
        nospaces = params.signature.replace(' ', '')
        key = nospaces + key_suffix
        iv = nospaces + iv_suffix
        return (key, iv, "signature: '%s'" % params.signature)
    except AttributeError:
        return ()

# Elemen pertama adalah fungsi yang menghasilkan kunci, yang kedua adalah array awalan tanda tangan yang cocok
KNOWN_KEYGENS = {
    (lambda p : tagparams_keygen(p)): ["H288A"],
    (lambda p : serial_keygen(p)): ["ZXHN H298A"],
    (lambda p : signature_keygen(p)): ["ZXHN H168N V3.5"],
    (lambda p : signature_keygen(p, key_suffix='Key02710010', iv_suffix='Iv02710010')): ["ZXHN H298Q", "ZXHN H268Q"],
    (lambda p : signature_keygen(p, key_suffix='Key02710001', iv_suffix='Iv02710001')): ["H188A", "H288A"],
    (lambda p : signature_keygen(p, key_suffix='Key02660004', iv_suffix='Iv02660004')): ["H196Q"],
    (lambda p : signature_keygen(p, key_suffix='8cc72b05705d5c46f412af8cbed55aa', iv_suffix='667b02a85c61c786def4521b060265e')): ["ZXHN F450(EPON ONU)"],

}

def run_keygen(params):
    for gen, sigs in KNOWN_KEYGENS.items():
        matching = False
        for sig in sigs:
            if params.signature.lower().startswith(sig.lower()):
                matching = True
                break
        if matching:
            genResult = gen(params)
            if len(genResult):
                return genResult
    return None

def run_all_keygens(params):
    outArr = []
    for gen in KNOWN_KEYGENS.keys():
        genResult = gen(params)
        if len(genResult):
            outArr.append(genResult)

    return outArr

def run_any_keygen(params, wanted):
    keygened = run_keygen(params)
    if keygened is not None:
        return keygened

    # tidak ada kecocokan tanda tangan yang ditemukan dalam keygen, temukan keygen generik dari jenis yang diinginkan dan gunakan itu
    allgens = run_all_keygens(params)
    for gen in allgens:
        if gen[2].startswith(wanted):
            return gen

    # seharusnya tidak sampai ke sini selama wanted adalah tipe yang ada
    return None
