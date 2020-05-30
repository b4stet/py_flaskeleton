from flask import g, current_app

from src.crypto.crypter import Crypter
from src.crypto.hasher import Hasher


class CryptoService():
    def __init__(self):
        self.__secret = current_app.config['app']['encryption_secret']

    def init_app(self, app):
        self.register()

    def register(self):
        if "crypto" not in g:
            g.crypto = {
                'crypter': Crypter(self.__secret),
                'hasher': Hasher()
            }

        return g.crypto