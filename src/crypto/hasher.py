import hashlib


class Hasher():
    def __init__(self):
        pass

    def hash(self, string):
        return hashlib.sha512(string.encode('utf-8')).hexdigest()
