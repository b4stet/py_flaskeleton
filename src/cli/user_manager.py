from flask.cli import with_appcontext
import click
import json

from src.template.response_cli import Response
from src.entity.user import UserEntity


class UserManagerCli():
    def __init__(self, input_validator, user_validator, time_converter, user_bo, logger):
        self.__logger = logger
        self.__input_validator = input_validator
        self.__user_validator = user_validator
        self.__user_bo = user_bo
        self.__time_converter = time_converter

    def init_app(self, app):
        group = click.Group(name='user', help='Scripts to administrate user accounts.')

        options = self.__get_options()
        group.add_command(click.Command(
            name='create', callback=with_appcontext(self.create_user), params=[options['name'], options['password']],
            help='Create a new user. Name and password required.',
        ))
        group.add_command(click.Command(
            name='list', callback=with_appcontext(self.list_users),
            help='List info of users',
        ))
        group.add_command(click.Command(
            name='update', callback=with_appcontext(self.update_user), params=[options['name'], options['password'], options['status']],
            help='Update status and/or password of a user.'
        ))
        app.cli.add_command(group)

    def __get_options(self):
        return {
            'name': click.Option(
                ['--name'],
                help='User name, allowed charset {}'.format(UserEntity.NAME_CHARSET)
            ),
            'password': click.Option(
                ['--password'],
                is_flag=True,
                default=False,
                help='Prompt for user password',
                callback=self.__prompt_password
            ),
            'status': click.Option(
                ['--status'],
                help='User status',
                type=click.Choice(UserEntity.STATUSES)
            )
        }

    def __prompt_password(self, ctx, param, password):
        if password is True:
            pwd = click.prompt(
                text='Enter password, allowed charset {}'.format(UserEntity.PASSWORD_CHARSET),
                hide_input=True,
                confirmation_prompt=True
            )

            return pwd

    def create_user(self, name, password):
        # validate data
        self.__input_validator.check_mandatory(name, 'name')
        self.__user_validator.check_name(name)

        self.__input_validator.check_mandatory(password, 'password')
        self.__user_validator.check_password(password)

        # add account
        self.__user_bo.add_user(name=name, password=password)

        Response('create_user', 'user {} created'.format(name), self.__logger).send()

    def list_users(self):
        users = self.__user_bo.get_all()

        Response('list_users', 'there are {} user(s) in db'.format(len(users))).send()
        for user in users:
            Response('list_users', '{} [id {}, created at {}]: status {}, last modified at {}'.format(
                user.get_name(),
                user.get_id(),
                self.__time_converter.to_str(user.get_created_at()),
                user.get_status(),
                self.__time_converter.to_str(user.get_modified_at())
            )).send()

    def update_user(self, name, password, status):
        # validate data
        self.__input_validator.check_mandatory(name, 'name')
        self.__user_validator.check_name(name)

        message = ''
        if password is not None:
            self.__user_validator.check_password(password)
            message += 'password changed'

        if status is not None:
            self.__user_validator.check_status(status)
            message += 'status set to {}'.format(status)

        # update account
        user = self.__user_bo.update_user(name=name, password=password, status=status)
        Response('update_user', '{} updated: {}'.format(user.get_name(), message), self.__logger).send()
