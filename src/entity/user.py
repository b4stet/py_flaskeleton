import string


class UserEntity():
    STATUS_ENABLED = 'enabled'
    STATUS_DISABLED = 'disabled'
    STATUSES = [STATUS_ENABLED, STATUS_DISABLED]
    NAME_CHARSET = ''.join(sorted(set(string.digits) | set(string.ascii_letters) | set('-_')))
    PASSWORD_CHARSET = ''.join(sorted(set(string.digits) | set(string.ascii_letters) | set('.+-*/?!_')))

    def __init__(self, name, password, salt, status, created_at=None, modified_at=None, user_id=None):
        self.__id = user_id
        self.__name = name
        self.__password = password
        self.__salt = salt
        self.__status = status
        self.__created_at = created_at
        self.__modified_at = modified_at

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_password(self):
        return self.__password

    def get_salt(self):
        return self.__salt

    def get_status(self):
        return self.__status

    def get_created_at(self):
        return self.__created_at

    def get_modified_at(self):
        return self.__modified_at

    def set_password(self, password):
        self.__password = password
        return self

    def set_salt(self, salt):
        self.__salt = salt
        return self

    def set_status(self, status):
        self.__status = status
        return self

    def set_created_at(self, created_at):
        self.__created_at = created_at
        return self

    def set_modified_at(self, modified_at):
        self.__modified_at = modified_at
        return self
