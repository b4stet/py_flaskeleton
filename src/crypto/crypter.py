from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util import Padding
import hashlib


class Crypter():
    def __init__(self, input_validator, key):
        self.__key = key
        self.__input_validator = input_validator

    def encrypt(self, plain, nonce=None):
        plain_padded = Padding.pad(plain.encode('utf-8'), block_size=16)

        if nonce is None:
            nonce = get_random_bytes(16).hex()

        self.__input_validator.check_type(nonce, str)
        if not (len(nonce) == 32 and set(nonce).issubset(set('0123456789abcdefABCDEF'))):
            raise ValueError('Invalid nonce. expected a 16-byte hex string. Got {}.'.format(nonce))

        cipher = AES.new(bytes.fromhex(self.__key), mode=AES.MODE_EAX, nonce=bytes.fromhex(nonce))
        ciphertext = cipher.encrypt(plain_padded)
        ciphertext = ciphertext.hex()
        nonce = cipher.nonce.hex()

        return ciphertext, nonce

    def decrypt(self, ciphertext, nonce):
        plain = AES.new(bytes.fromhex(self.__key), mode=AES.MODE_EAX, nonce=bytes.fromhex(nonce))
        plaintext_padded = plain.decrypt(bytes.fromhex(ciphertext))
        plaintext = Padding.unpad(plaintext_padded, block_size=16)

        return plaintext.decode('utf-8')
