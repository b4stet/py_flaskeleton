from src.entity.user import UserEntity


class UserValidator():
    def __init__(self):
        pass

    def check_name(self, name):
        if set(name).issubset(set(UserEntity.NAME_CHARSET)) is False:
            raise ValueError('Invalid name, allowed charset is: {}'.format(UserEntity.NAME_CHARSET))

    def check_password(self, password):
        if set(password).issubset(set(UserEntity.PASSWORD_CHARSET)) is False:
            raise ValueError('Invalid password, allowed charset is: {}'.format(UserEntity.PASSWORD_CHARSET))

    def check_status(self, status):
        if status not in UserEntity.STATUSES:
            raise ValueError('Unknown status {}'.format(status))
