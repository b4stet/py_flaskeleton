from flask import request
from werkzeug.exceptions import Forbidden

from src.entity.user import UserEntity


class UserAuthorizationMiddleware():
    def __init__(self, hasher, user_bo, logger):
        self.__logger = logger
        self.__user_bo = user_bo
        self.__hasher = hasher

    def check(self):
        creds = request.authorization

        if creds is None:
            raise Forbidden('No authorization header found.')

        user = self.__user_bo.get_by_name(creds.username, full=True)
        if user is None:
            raise Forbidden('Unknown user {}.'.format(creds.username))

        # user authentication
        if user.get_status() == UserEntity.STATUS_DISABLED:
            raise Forbidden('User {} is disabled.'.format(creds.username))

        password, _ = self.__hasher.hash(creds.password, salt=user.get_salt())
        if password != user.get_password():
            raise Forbidden('Invalid password for user {}.'.format(creds.username))
