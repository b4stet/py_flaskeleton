from flask import g, current_app

from src.crypto.crypter import Crypter
from src.crypto.hasher import Hasher
from src.validator.input import InputValidator


class CryptoService():
    def __init__(self):
        self.__encryption_secret = current_app.config['app']['encryption_secret']
        self.__encryption_salt = current_app.config['app']['encryption_salt']
        self.__anonymizer_salt = current_app.config['app']['anonymizer_salt']

    def init_app(self, app):
        self.register()

    def register(self):
        input_validator = InputValidator()
        hasher = Hasher(input_validator, self.__anonymizer_salt)
        key, _ = hasher.hash(self.__encryption_secret, salt=self.__encryption_salt, outlen_bytes=32)

        if "crypto" not in g:
            g.crypto = {
                'crypter': Crypter(input_validator, key),
                'hasher': hasher,
            }

        return g.crypto
