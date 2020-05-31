from flask.cli import with_appcontext
import click
import os
from datetime import datetime, timezone

from src.template.response_cli import Response


class DbManagerCli():
    def __init__(self, migration_dir, migrator_bo, logger):
        self.__logger = logger
        self.__migrator_bo = migrator_bo
        self.__migration_dir = migration_dir

    def init_app(self, app):
        group = click.Group(name='db_migration', help='Scripts to alter DB schema.')

        group.add_command(click.Command(
            name='init', callback=with_appcontext(self.init_migrations),
            help='Creates a table to follow migrations.'
        ))

        group.add_command(click.Command(
            name='check', callback=with_appcontext(self.check_migrations),
            help='Verifies if DB schema is sync with migration files.'
        ))

        group.add_command(click.Command(
            name='apply', callback=with_appcontext(self.apply_migrations),
            help='Updates DB schema.'
        ))

        app.cli.add_command(group)

    def init_migrations(self):
        result = self.__migrator_bo.init()
        if result is True:
            Response('init_migrations', 'table created', self.__logger).send()
        else:
            Response('init_migrations', 'table already exists').send()

    def check_migrations(self):
        to_apply = self.__migrator_bo.compare(self.__migration_dir)
        Response('check_migrations', 'comparing db state with migration folder').send()

        if len(to_apply) == 0:
            Response('check_migrations', 'db schema is up to date').send()
        else:
            Response('check_migrations', 'db schema is behind by {} file(s). Change to apply:'.format(len(to_apply))).send()
            for migration in to_apply:
                Response('check_migrations', '* {}'.format(migration)).send()

    def apply_migrations(self):
        to_apply = self.__migrator_bo.compare(self.__migration_dir)
        Response('apply_migrations', 'collecting migrations to apply').send()

        result, first_failure = self.__migrator_bo.apply(self.__migration_dir, to_apply)
        if result is True:
            Response('apply_migrations', 'migration(s) successful', self.__logger).send()
        else:
            Response('apply_migrations', 'migration(s) failed on {}. Rolled back to previous DB shema'.format(first_failure), self.__logger).send()
