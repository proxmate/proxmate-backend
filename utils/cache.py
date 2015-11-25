import hashlib


def _smart_key(key):
    m = hashlib.sha256()
    m.update(str(key))
    return m.hexdigest()


def make_key(key, key_prefix, version):
    "Truncate all keys to 250 or less and remove control characters"
    return ':'.join([key_prefix, str(version), _smart_key(key)])[:250]
