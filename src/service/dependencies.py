from flask import g, current_app
import os

from src.validator.user import UserValidator
from src.validator.input import InputValidator
from src.converter.time import TimeConverter

from src.table.user import UserTable
from src.table.db_migrator import DbMigratorTable

from src.bo.user import UserBo
from src.bo.db_migrator import DbMigratorBo

from src.service.db_connector import DbConnectorService
from src.middleware.user_authorization import UserAuthorizationMiddleware
from src.action.get_index import GetIndexAction
from src.action.list_users import ListUsersAction
from src.cli.db_manager import DbManagerCli
from src.cli.user_manager import UserManagerCli


class DependenciesService():
    def __init__(self):
        self.__logger = current_app.logger
        self.__crypter = g.crypto['crypter']
        self.__hasher = g.crypto['hasher']
        self.__db_config = current_app.config['db']
        self.__mode = current_app.config['mode']

    def init_app(self, app):
        self.register()

    def register(self):
        input_validator = InputValidator()
        user_validator = UserValidator()
        time_converter = TimeConverter()
        migration_dir = os.path.join(current_app.instance_path, 'migration')

        db_connector = DbConnectorService(self.__db_config, self.__mode)
        user_table = UserTable(self.__crypter, self.__hasher, db_connector, self.__logger)
        migrator_table = DbMigratorTable(db_connector, self.__logger)

        user_bo = UserBo(time_converter, self.__hasher, user_table, self.__logger)
        migrator_bo = DbMigratorBo(migrator_table, self.__logger)

        if 'di_container' not in g:
            g.di_container = {
                UserAuthorizationMiddleware: UserAuthorizationMiddleware(self.__hasher, user_bo, self.__logger).check,
                GetIndexAction: GetIndexAction.as_view('get_index', self.__logger),
                ListUsersAction: ListUsersAction.as_view('list_users', time_converter, user_bo, self.__logger),
                DbManagerCli: DbManagerCli(migration_dir, migrator_bo, self.__logger),
                UserManagerCli: UserManagerCli(input_validator, user_validator, time_converter, user_bo, self.__logger),
            }

        return g.di_container
