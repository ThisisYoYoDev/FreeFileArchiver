from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from .constants import KEY, IV


def encrypt(message: bytes):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    ct_bytes = cipher.encrypt(pad(message, AES.block_size))
    return ct_bytes


def decrypt(ct_bytes: bytes):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
    return pt
