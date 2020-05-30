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

        if user is not None and full is False:
            user = self.__account2safe(user)

        return user

    def get_all(self, full=False):
        users = self.__user_table.fetch_all()
        if full is False:
            users = [self.__account2safe(user) for user in users]

        return users

    def entity2dict(self, user: UserEntity):
        if user is None:
            return {}

        result = {
            'name': user.get_name(),
            'status': user.get_status(),
            'created_at': self.__time_converter.to_str(user.get_created_at()),
            'modified_at': self.__time_converter.to_str(user.get_modified_at()),
        }

        if user.get_password() is not None:
            result['password'] = user.get_password()

        return result

    def __account2safe(self, user: UserEntity):
        user_safe = user
        return user_safe.set_password(None)

    def add_user(self, name, password):
        # verify account is new
        user = self.__user_table.fetch_by_name(name)
        if user is not None:
            raise ValueError('Cannot create {}, user already exists.'.format(name))

        # create
        user = UserEntity(
            name=name,
            password=self.__hasher.hash(password),
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
            user = user.set_password(self.__hasher.hash(password))

        if status is not None:
            user = user.set_status(status)

        user = user.set_modified_at(datetime.now(timezone.utc))

        return self.__user_table.save(user)
