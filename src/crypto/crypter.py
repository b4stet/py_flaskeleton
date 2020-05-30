from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util import Padding
import hashlib


class Crypter():
    def __init__(self, secret):
        self.__key = hashlib.sha256(secret.encode('utf-8')).hexdigest()

    def encrypt(self, plain):
        plain_padded = Padding.pad(plain.encode('utf-8'), block_size=16)
        nonce = get_random_bytes(16).hex()

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
