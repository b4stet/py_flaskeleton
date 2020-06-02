from datetime import datetime, timezone

from src.entity.user import UserEntity


class UserBo():
    def __init__(self, time_converter, hasher, user_table, logger):
        self.__logger = logger
        self.__user_table = user_table
        self.__time_converter = time_converter
        self.__hasher = hasher

    def get_by_name(self, name, full=False):
        user = self.__user_table.fetch_by_name(name)
        if user is None:
            return user

        if full is False:
            user = user.to_safe()

        return user

    def get_all(self, full=False):
        users = self.__user_table.fetch_all()
        if full is False:
            users = [user.to_safe() for user in users]

        return users

    def add_user(self, name, password):
        # verify account is new
        user = self.__user_table.fetch_by_name(name)
        if user is not None:
            raise ValueError('Cannot create {}, user already exists.'.format(name))

        # create
        digest, salt = self.__hasher.hash(password)
        user = UserEntity(
            name=name,
            password=digest,
            salt=salt,
            status=UserEntity.STATUS_ENABLED,
            created_at=datetime.now(timezone.utc),
            modified_at=datetime.now(timezone.utc)
        )

        return self.__user_table.save(user)

    def update_user(self, name, password=None, status=None):
        # verify provider exists
        user = self.__user_table.fetch_by_name(name)
        if user is None:
            raise ValueError('Cannot update {}, user does not exist.'.format(name))

        # update fields
        if password is not None:
            new_digest, _ = self.__hasher.hash(password, user.get_salt())
            user = user.set_password(new_digest)

        if status is not None:
            user = user.set_status(status)

        user = user.set_modified_at(datetime.now(timezone.utc))

        return self.__user_table.save(user)
