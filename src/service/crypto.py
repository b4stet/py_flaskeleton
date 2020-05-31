from flask import g, current_app

from src.crypto.crypter import Crypter
from src.crypto.hasher import Hasher
from src.validator.input import InputValidator


class CryptoService():
    def __init__(self):
        self.__secret = current_app.config['app']['encryption_secret']
        self.__salt = current_app.config['app']['anonymizer_salt']

    def init_app(self, app):
        self.register()

    def register(self):
        input_validator = InputValidator()

        if "crypto" not in g:
            g.crypto = {
                'crypter': Crypter(input_validator, self.__secret),
                'hasher': Hasher(input_validator, self.__salt),
            }

        return g.crypto
