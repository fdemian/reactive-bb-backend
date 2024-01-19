from hashlib import scrypt


def hash_password(password, salt):
    # TODO: make this configurable? (with sane defaults)
    """
    hashlib.scrypt(password, *, salt, n, r, p, maxmem=0, dklen=64)
    The function provides scrypt password-based key derivation function as defined in RFC 7914.
    - n is the CPU/Memory cost factor,
    - r the block size,
    - p parallelization factor
    -  and maxmem limits memory (OpenSSL 1.1.0 defaults to 32 MiB).
    - dklen is the length of the derived key.
    """
    scrypt_key = scrypt(password.encode(), salt=salt, n=16384, r=8, p=1)
    return scrypt_key


def check_password(pass_to_check, current_pass, salt):
    encoded_pass = hash_password(pass_to_check, salt)
    return encoded_pass == current_pass
