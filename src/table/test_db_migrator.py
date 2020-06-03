import unittest
from unittest import mock
from unittest.mock import mock_open
import logging
from src.entity.db_migrator import DbMigratorEntity
from src.table.db_migrator import DbMigratorTable


class TestDbMigratorTable(unittest.TestCase):
    def setUp(self):
        self.__mock_db = mock.patch('src.service.db_connector.DbConnectorService').start()
        logger = logging.getLogger('TestDbMigratorTable')
        self.__migrator_table = DbMigratorTable(self.__mock_db, logger)

    def tearDown(self):
        del self.__migrator_table
        mock.patch.stopall()

    def test_has_table_yes(self):
        # prepare data
        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        self.__mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]

        # execute
        has_table = self.__migrator_table.has_table()

        # check
        cursor_execute_calls = mock_cursor.execute.call_args_list
        expected_args = ['PREPARE has_migration', 'EXECUTE has_migration']
        self.assertEqual(mock_cursor.execute.call_count, 2, 'Expected 2 calls to cursor.execute(). Got {}'.format(len(cursor_execute_calls)))
        for call, expected_arg in zip(cursor_execute_calls, expected_args):
            args, _ = call
            self.assertTrue(args[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, args[0]))

        self.assertEqual(mock_cursor.fetchone.call_count, 1, 'Expected 1 call to cursor.fetchone(). Got {}'.format(mock_cursor.fetchone.call_count))

        self.assertTrue(has_table, 'Expected True result. Got {}'.format(has_table))

        # clean
        mock_cursor.stop()

    def test_has_table_no(self):
        # prepare data
        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        self.__mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = []

        # execute
        has_table = self.__migrator_table.has_table()

        # check
        cursor_execute_calls = mock_cursor.execute.call_args_list
        expected_args = ['PREPARE has_migration', 'EXECUTE has_migration']
        self.assertEqual(mock_cursor.execute.call_count, 2, 'Expected 2 calls to cursor.execute(). Got {}'.format(len(cursor_execute_calls)))
        for call, expected_arg in zip(cursor_execute_calls, expected_args):
            args, _ = call
            self.assertTrue(args[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, args[0]))

        self.assertEqual(mock_cursor.fetchone.call_count, 1, 'Expected 1 call to cursor.fetchone(). Got {}'.format(mock_cursor.fetchone.call_count))

        self.assertFalse(has_table, 'Expected False result. Got {}'.format(has_table))

        # clean
        mock_cursor.stop()

    def test_create_table(self):
        # prepare data
        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        mock_connection = mock.patch('psycopg2.extensions.connection').start()
        self.__mock_db.cursor.return_value = mock_cursor
        self.__mock_db.connection.return_value = mock_connection

        # execute
        self.__migrator_table.create_table()

        # check
        cursor_execute_call = mock_cursor.execute.call_args_list
        expected_arg = 'CREATE TABLE migration'
        self.assertEqual(mock_cursor.execute.call_count, 1, 'Expected 1 call to cursor.execute(). Got {}'.format(mock_cursor.execute.call_count))
        arg, _ = cursor_execute_call[0]
        self.assertTrue(arg[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, arg))

        self.assertEqual(mock_connection.commit.call_count, 1, 'Expected 1 call to connection.commit(). Got {}'.format(mock_connection.commit.call_count))

    def test_fetch_all_no_migration(self):
        # prepare data
        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        self.__mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        # execute
        migrations = self.__migrator_table.fetch_all()

        # check
        cursor_execute_calls = mock_cursor.execute.call_args_list
        expected_args = ['PREPARE select_migration_all', 'EXECUTE select_migration_all']
        self.assertEqual(mock_cursor.execute.call_count, 2, 'Expected 2 calls to cursor.execute(). Got {}'.format(mock_cursor.execute.call_count))
        for call, expected_arg in zip(cursor_execute_calls, expected_args):
            args, _ = call
            self.assertTrue(args[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, args[0]))

        self.assertEqual(mock_cursor.fetchall.call_count, 1, 'Expected 1 call to cursor.fetchall(). Got {}'.format(mock_cursor.fetchall.call_count))

        self.assertIsInstance(migrations, list, 'Expected result to be a list. Got {}'.format(type(migrations)))
        self.assertEqual(len(migrations), 0, 'Expected empty list in result. Got {}'.format(migrations))

        # clean
        mock_cursor.stop()

    def test_fetch_all(self):
        # prepare data
        migrations_expected = [
            DbMigratorEntity(migration_id=1, filename='001_schema.sql', applied_at='time1'),
            DbMigratorEntity(migration_id=2, filename='002_schema.sql', applied_at='time2'),
        ]
        records = [migration.to_dict() for migration in migrations_expected]

        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        self.__mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = records

        # execute
        migrations = self.__migrator_table.fetch_all()

        # check
        cursor_execute_calls = mock_cursor.execute.call_args_list
        expected_args = ['PREPARE select_migration_all', 'EXECUTE select_migration_all']
        self.assertEqual(mock_cursor.execute.call_count, 2, 'Expected 2 calls to cursor.execute(). Got {}'.format(mock_cursor.execute.call_count))
        for call, expected_arg in zip(cursor_execute_calls, expected_args):
            args, _ = call
            self.assertTrue(args[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, args[0]))

        self.assertEqual(mock_cursor.fetchall.call_count, 1, 'Expected 1 call to cursor.fetchall(). Got {}'.format(mock_cursor.fetchall.call_count))

        self.assertIsInstance(migrations, list, 'Expected result to be a list. Got {}'.format(type(migrations)))
        self.assertEqual(len(migrations), 2, 'Expected empty list in result. Got {}'.format(migrations))
        self.assertListEqual(
            [type(migration) for migration in migrations], [DbMigratorEntity, DbMigratorEntity],
            'Expected 2 DbMigratorEntity in result. Got {}'.format(migrations)
        )
        for observed, expected in zip(migrations, migrations_expected):
            self.assertEqual(
                observed.get_id(), expected.get_id(),
                'Expected migration id {}. Got {}'.format(expected.get_id(), observed.get_id())
            )
            self.assertEqual(
                observed.get_filename(), expected.get_filename(),
                'Expected migration filename {}. Got {}'.format(expected.get_filename(), observed.get_filename())
            )
            self.assertEqual(
                observed.get_applied_at(), expected.get_applied_at(),
                'Expected migration applied_at {}. Got {}'.format(expected.get_applied_at(), observed.get_applied_at())
            )

        # clean
        mock_cursor.stop()

    def test_record_migration(self):
        # prepare data
        migration = DbMigratorEntity(filename='001_schema.sql', applied_at='time1')

        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        self.__mock_db.cursor.return_value = mock_cursor

        # execute
        self.__migrator_table.record_migration(migration)

        # check
        cursor_execute_calls = mock_cursor.execute.call_args_list
        expected_args = ['PREPARE insert_migration', 'EXECUTE insert_migration']
        self.assertEqual(mock_cursor.execute.call_count, 2, 'Expected 2 calls to cursor.execute(). Got {}'.format(mock_cursor.execute.call_count))
        for call, expected_arg in zip(cursor_execute_calls, expected_args):
            args, _ = call
            self.assertTrue(args[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, args[0]))

    def test_apply_migration(self):
        # prepare data
        migration_file = 'migration_file.sql'
        mock_open_file = mock.patch('src.table.db_migrator.open', mock_open()).start()
        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        self.__mock_db.cursor.return_value = mock_cursor

        # execute
        self.__migrator_table.apply_migration(migration_file)

        # check
        mock_open_file.assert_called_once_with('migration_file.sql', mode='r')
        handle = mock_open_file()
        handle.read.assert_called_once()
        mock_cursor.execute.assert_called_once()

        # clean
        mock_cursor.stop()

    def test_finish_transaction_no_error(self):
        mock_connection = mock.patch('psycopg2.extensions.connection').start()
        self.__mock_db.connection.return_value = mock_connection

        self.__migrator_table.finish_transaction(False)

        mock_connection.commit.assert_called_once()
        mock_connection.rollback.assert_not_called()

    def test_finish_transaction_with_error(self):
        mock_connection = mock.patch('psycopg2.extensions.connection').start()
        self.__mock_db.connection.return_value = mock_connection

        self.__migrator_table.finish_transaction(True)

        mock_connection.rollback.assert_called_once()
        mock_connection.commit.assert_not_called()

    def test_dict2entity_none(self):
        # prepare data
        record = None

        # execute
        migration = self.__migrator_table._dict2entity(record)

        # check
        self.assertEqual(migration, None, 'Expected None as result. Got {}'.format(migration))

    def test_dict2entity(self):
        # prepare data
        migration_expected = DbMigratorEntity(filename='001_schema.sql', applied_at='time1')
        record = migration_expected.to_dict()

        # execute
        migration = self.__migrator_table._dict2entity(record)

        # check
        self.assertIsInstance(migration, DbMigratorEntity, 'Expected result to be a DbMigratorEntity. Got {}'.format(type(migration)))
        self.assertEqual(
            migration.get_id(), migration_expected.get_id(),
            'Expected migration id {}. Got {}'.format(migration_expected.get_id(), migration.get_id())
        )
        self.assertEqual(
            migration.get_filename(), migration_expected.get_filename(),
            'Expected migration filename {}. Got {}'.format(migration_expected.get_filename(), migration.get_filename())
        )
        self.assertEqual(
            migration.get_applied_at(), migration_expected.get_applied_at(),
            'Expected migration applied_at {}. Got {}'.format(migration_expected.get_applied_at(), migration.get_applied_at())
        )
