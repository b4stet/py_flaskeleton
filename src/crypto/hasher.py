import scrypt
import hashlib
from Cryptodome.Random import get_random_bytes


class Hasher():
    def __init__(self, input_validator, anonymizer_salt):
        self.__input_validator = input_validator
        self.__salt_anonymizer = anonymizer_salt

    def anonymize(self, string):
        digest, _ = self.hash(string, salt=self.__salt_anonymizer)
        return digest

    def hash(self, string, salt=None, outlen_bytes=64):
        if salt is None:
            salt = get_random_bytes(16).hex()

        self.__input_validator.check_type(salt, str)
        if not (len(salt) == 32 and set(salt).issubset(set('0123456789abcdefABCDEF'))):
            raise ValueError('Invalid salt. expected a 16-byte hex string. Got {}.'.format(salt))

        digest = scrypt.hash(string.encode('utf-8'), bytes.fromhex(salt), N=16384, r=8, p=1, buflen=outlen_bytes)
        return digest.hex(), salt
