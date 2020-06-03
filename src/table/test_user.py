import unittest
from unittest import mock
import logging
from src.entity.user import UserEntity
from src.table.user import UserTable


class TestUserTable(unittest.TestCase):
    def setUp(self):
        self.__mock_db = mock.patch('src.service.db_connector.DbConnectorService').start()
        self.__mock_crypter = mock.patch('src.crypto.crypter.Crypter').start()
        self.__mock_hasher = mock.patch('src.crypto.hasher.Hasher').start()
        logger = logging.getLogger('TestUserTable')
        self.__user_table = UserTable(self.__mock_crypter, self.__mock_hasher, self.__mock_db, logger)

    def tearDown(self):
        del self.__user_table
        mock.patch.stopall()

    def __assert_user_equal(self, observed: UserEntity, expected: UserEntity, omit_id=False):
        if omit_id is False:
            self.assertEqual(
                observed.get_id(), expected.get_id(),
                'Expected user id {}. Got {}'.format(expected.get_id(), observed.get_id())
            )
        self.assertEqual(
            observed.get_name(), expected.get_name(),
            'Expected user name {}. Got {}'.format(expected.get_name(), observed.get_name())
        )
        self.assertEqual(
            observed.get_status(), expected.get_status(),
            'Expected user status {}. Got {}'.format(expected.get_status(), observed.get_status())
        )
        self.assertEqual(
            observed.get_password(), expected.get_password(),
            'Expected user password {}. Got {}'.format(expected.get_password(), observed.get_password())
        )
        self.assertEqual(
            observed.get_salt(), expected.get_salt(),
            'Expected user salt {}. Got {}'.format(expected.get_salt(), observed.get_salt())
        )
        self.assertEqual(
            observed.get_created_at(), expected.get_created_at(),
            'Expected user created_at {}. Got {}'.format(expected.get_created_at(), observed.get_created_at())
        )
        self.assertEqual(
            observed.get_modified_at(), expected.get_modified_at(),
            'Expected user modified_at {}. Got {}'.format(expected.get_modified_at(), observed.get_modified_at())
        )

    def test_fetch_all_no_user(self):
        # prepare data
        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        self.__mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        # execute
        users = self.__user_table.fetch_all()

        # check
        cursor_execute_calls = mock_cursor.execute.call_args_list
        expected_args = ['PREPARE select_user_all', 'EXECUTE select_user_all']
        self.assertEqual(mock_cursor.execute.call_count, 2, 'Expected 2 calls to cursor.execute(). Got {}'.format(mock_cursor.execute.call_count))
        for call, expected_arg in zip(cursor_execute_calls, expected_args):
            args, _ = call
            self.assertTrue(args[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, args[0]))

        self.assertEqual(mock_cursor.fetchall.call_count, 1, 'Expected 1 call to cursor.fetchall(). Got {}'.format(mock_cursor.fetchall.call_count))

        self.assertFalse(self.__mock_crypter.decrypt.called, 'Crypter.decrypt() was called and should not have been.')
        self.assertIsInstance(users, list, 'Expected result to be a list. Got {}'.format(type(users)))
        self.assertEqual(len(users), 0, 'Expected empty list in result. Got {}'.format(users))

        # clean
        mock_cursor.stop()

    def test_fetch_all(self):
        # prepare data
        users_expected = [
            UserEntity(user_id=1, name='user1', password='password1', salt='salt1', status='status1'),
            UserEntity(user_id=2, name='user2', password='password2', salt='salt2', status='status2'),
        ]
        records = []
        for user in users_expected:
            record = user.to_dict()
            record.pop('name', None)
            record['name_hashed'] = 'name_hashed'
            record['name_encrypted'] = 'name_encrypted'
            record['nonce'] = 'nonce'
            records.append(record)

        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        self.__mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = records
        self.__mock_crypter.decrypt.side_effect = [user.get_name() for user in users_expected]

        # execute
        users = self.__user_table.fetch_all()

        # check
        cursor_execute_calls = mock_cursor.execute.call_args_list
        expected_args = ['PREPARE select_user_all', 'EXECUTE select_user_all']
        self.assertEqual(mock_cursor.execute.call_count, 2, 'Expected 2 calls to cursor.execute(). Got {}'.format(mock_cursor.execute.call_count))
        for call, expected_arg in zip(cursor_execute_calls, expected_args):
            args, _ = call
            self.assertTrue(args[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, args[0]))

        self.assertEqual(mock_cursor.fetchall.call_count, 1, 'Expected 1 call to cursor.fetchall(). Got {}'.format(mock_cursor.fetchall.call_count))

        crypter_decrypt_calls = self.__mock_crypter.decrypt.call_args_list
        self.assertEqual(
            self.__mock_crypter.decrypt.call_count, 2,
            'Expected 2 calls to crypter.decrypt(). Got {}'.format(self.__mock_crypter.decrypt.call_count)
        )
        for call, record in zip(crypter_decrypt_calls, records):
            args, _ = call
            expected_args = (record['name_encrypted'], record['nonce'])
            self.assertSequenceEqual(args, expected_args, 'Expected crypter.decrypt() call with parameter {}. Got {}'.format(expected_args, args))

        self.assertIsInstance(users, list, 'Expected result to be a list. Got {}'.format(type(users)))
        self.assertEqual(len(users), 2, 'Expected 2 users in result. Got {}'.format(len(users)))
        self.assertListEqual([type(user) for user in users], [UserEntity, UserEntity], 'Expected 2 UserEntity in result. Got {}'.format(users))
        for observed, expected in zip(users, users_expected):
            self.__assert_user_equal(observed, expected)

        # clean
        mock_cursor.stop()

    def test_fetch_by_id_unknown(self):
        # prepare data
        user_id = 1
        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        self.__mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        # execute
        user = self.__user_table.fetch_by_id(user_id)

        # check
        cursor_execute_calls = mock_cursor.execute.call_args_list
        expected_args = ['PREPARE select_user_by_id', 'EXECUTE select_user_by_id']
        self.assertEqual(mock_cursor.execute.call_count, 2, 'Expected 2 calls to cursor.execute(). Got {}'.format(mock_cursor.execute.call_count))
        for call, expected_arg in zip(cursor_execute_calls, expected_args):
            args, _ = call
            self.assertTrue(args[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, args[0]))

        self.assertEqual(mock_cursor.fetchone.call_count, 1, 'Expected 1 call to cursor.fetchone(). Got {}'.format(mock_cursor.fetchall.call_count))

        self.assertFalse(self.__mock_crypter.decrypt.called, 'Crypter.decrypt() was called and should not have been.')
        self.assertEqual(user, None, 'Expected None as result. Got {}'.format(user))

        # clean
        mock_cursor.stop()

    def test_fetch_by_id(self):
        # prepare data
        user_expected = UserEntity(user_id=1, name='user', password='password', salt='salt', status='status')
        record = user_expected.to_dict()
        record.pop('name', None)
        record['name_hashed'] = 'name_hashed'
        record['name_encrypted'] = 'name_encrypted'
        record['nonce'] = 'nonce'

        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        self.__mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = record
        self.__mock_crypter.decrypt.return_value = user_expected.get_name()

        # execute
        user = self.__user_table.fetch_by_id(user_expected.get_id())

        # check
        cursor_execute_calls = mock_cursor.execute.call_args_list
        expected_args = ['PREPARE select_user_by_id', 'EXECUTE select_user_by_id']
        self.assertEqual(mock_cursor.execute.call_count, 2, 'Expected 2 calls to cursor.execute(). Got {}'.format(mock_cursor.execute.call_count))
        for call, expected_arg in zip(cursor_execute_calls, expected_args):
            args, _ = call
            self.assertTrue(args[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, args[0]))

        self.assertEqual(mock_cursor.fetchone.call_count, 1, 'Expected 1 call to cursor.fetchone(). Got {}'.format(mock_cursor.fetchall.call_count))

        crypter_decrypt_call = self.__mock_crypter.decrypt.call_args_list
        self.assertEqual(
            self.__mock_crypter.decrypt.call_count, 1,
            'Expected 1 calls to crypter.decrypt(). Got {}'.format(self.__mock_crypter.decrypt.call_count)
        )
        args, _ = crypter_decrypt_call[0]
        expected_args = (record['name_encrypted'], record['nonce'])
        self.assertSequenceEqual(args, expected_args, 'Expected crypter.decrypt() call with parameter {}. Got {}'.format(expected_args, args))

        self.assertIsInstance(user, UserEntity, 'Expected result to be a UserEntity. Got {}'.format(type(user)))
        self.__assert_user_equal(user, user_expected)

        # clean
        mock_cursor.stop()

    def test_fetch_by_name_unknown(self):
        # prepare data
        user_name = 'unknown_user'
        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        self.__mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        # execute
        user = self.__user_table.fetch_by_name(user_name)

        # check
        cursor_execute_calls = mock_cursor.execute.call_args_list
        expected_args = ['PREPARE select_user_by_name', 'EXECUTE select_user_by_name']
        self.assertEqual(mock_cursor.execute.call_count, 2, 'Expected 2 calls to cursor.execute(). Got {}'.format(mock_cursor.execute.call_count))
        for call, expected_arg in zip(cursor_execute_calls, expected_args):
            args, _ = call
            self.assertTrue(args[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, args[0]))

        self.assertEqual(mock_cursor.fetchone.call_count, 1, 'Expected 1 call to cursor.fetchone(). Got {}'.format(mock_cursor.fetchall.call_count))

        self.assertFalse(self.__mock_crypter.decrypt.called, 'Crypter.decrypt() was called and should not have been.')
        self.assertEqual(user, None, 'Expected None as result. Got {}'.format(user))

        # clean
        mock_cursor.stop()

    def test_fetch_by_name(self):
        # prepare data
        user_expected = UserEntity(name='user', password='password', salt='salt', status='status')
        record = user_expected.to_dict()
        record.pop('name', None)
        record['name_hashed'] = 'name_hashed'
        record['name_encrypted'] = 'name_encrypted'
        record['nonce'] = 'nonce'

        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        self.__mock_db.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = record
        self.__mock_crypter.decrypt.return_value = user_expected.get_name()

        # execute
        user = self.__user_table.fetch_by_name(user_expected.get_name())

        # check
        cursor_execute_calls = mock_cursor.execute.call_args_list
        expected_args = ['PREPARE select_user_by_name', 'EXECUTE select_user_by_name']
        self.assertEqual(mock_cursor.execute.call_count, 2, 'Expected 2 calls to cursor.execute(). Got {}'.format(mock_cursor.execute.call_count))
        for call, expected_arg in zip(cursor_execute_calls, expected_args):
            args, _ = call
            self.assertTrue(args[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, args[0]))

        self.assertEqual(mock_cursor.fetchone.call_count, 1, 'Expected 1 call to cursor.fetchone(). Got {}'.format(mock_cursor.fetchall.call_count))

        crypter_decrypt_call = self.__mock_crypter.decrypt.call_args_list
        self.assertEqual(
            self.__mock_crypter.decrypt.call_count, 1,
            'Expected 1 calls to crypter.decrypt(). Got {}'.format(self.__mock_crypter.decrypt.call_count)
        )
        args, _ = crypter_decrypt_call[0]
        expected_args = (record['name_encrypted'], record['nonce'])
        self.assertSequenceEqual(args, expected_args, 'Expected crypter.decrypt() call with parameter {}. Got {}'.format(expected_args, args))

        self.assertIsInstance(user, UserEntity, 'Expected result to be a UserEntity. Got {}'.format(type(user)))
        self.__assert_user_equal(user, user_expected)

        # clean
        mock_cursor.stop()

    def test_dict2entity_none(self):
        # prepare data
        record = None

        # execute
        user = self.__user_table._dict2entity(record)

        # check
        self.assertFalse(self.__mock_crypter.decrypt.called, 'Crypter.decrypt() was called and should not have been.')
        self.assertEqual(user, None, 'Expected None as result. Got {}'.format(user))

    def test_dict2entity(self):
        # prepare data
        user_expected = UserEntity(name='user', password='password', salt='salt', status='status')
        record = user_expected.to_dict()
        record.pop('name', None)
        record['name_hashed'] = 'name_hashed'
        record['name_encrypted'] = 'name_encrypted'
        record['nonce'] = 'nonce'

        self.__mock_crypter.decrypt.return_value = user_expected.get_name()

        # execute
        user = self.__user_table._dict2entity(record)

        # check
        crypter_decrypt_call = self.__mock_crypter.decrypt.call_args_list
        self.assertEqual(
            self.__mock_crypter.decrypt.call_count, 1,
            'Expected 1 call to crypter.decrypt(). Got {}.'.format(self.__mock_crypter.decrypt.call_count)
        )
        args, _ = crypter_decrypt_call[0]
        expected_args = (record['name_encrypted'], record['nonce'])
        self.assertSequenceEqual(args, expected_args, 'Expected crypter.decrypt() call with parameter {}. Got {}'.format(expected_args, args))

        self.assertIsInstance(user, UserEntity, 'Expected result to be a UserEntity. Got {}'.format(type(user)))
        self.__assert_user_equal(user, user_expected)

    def test_save_no_id(self):
        # prepare data
        user_expected = UserEntity(name='user', password='password', salt='salt', status='status')
        record_after = user_expected.to_dict()
        record_after.pop('name', None)
        record_after['name_hashed'] = 'name_hashed'
        record_after['name_encrypted'] = 'name_encrypted'
        record_after['nonce'] = 'nonce'
        record_after['id'] = 1

        self.__mock_crypter.encrypt.return_value = ('name_encrypted', 'nonce')
        self.__mock_crypter.decrypt.return_value = user_expected.get_name()
        self.__mock_hasher.anonymize.return_value = 'name_hashed'

        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        mock_connection = mock.patch('psycopg2.extensions.connection').start()
        self.__mock_db.cursor.return_value = mock_cursor
        self.__mock_db.connection.return_value = mock_connection
        mock_cursor.fetchone.return_value = record_after

        # execute
        user = self.__user_table.save(user_expected)

        # check
        crypter_encrypt_call = self.__mock_crypter.encrypt.call_args_list
        arg, _ = crypter_encrypt_call[0]
        expected_arg = (user_expected.get_name(),)
        self.assertEqual(
            self.__mock_crypter.encrypt.call_count, 1,
            'Expected 1 call to crypter.encrypt(). Got {}'.format(self.__mock_crypter.encrypt.call_count)
        )
        self.assertEqual(arg, expected_arg, 'Expected crypter.encrypt() call with parameter {}. Got {}'.format(expected_arg, arg))

        hasher_anonymize_call = self.__mock_hasher.anonymize.call_args_list
        self.assertEqual(
            self.__mock_hasher.anonymize.call_count, 2,
            'Expected 2 call to hasher.anonymize(). Got {}'.format(self.__mock_hasher.anonymize.call_count)
        )
        for call in hasher_anonymize_call:
            arg, _ = call
            expected_arg = (user_expected.get_name(),)
            self.assertEqual(arg, expected_arg, 'Expected hasher.anonymize() call with parameter {}. Got {}'.format(expected_arg, arg))

        cursor_execute_calls = mock_cursor.execute.call_args_list
        expected_args = ['PREPARE insert_user', 'EXECUTE insert_user', 'PREPARE select_user_by_name', 'EXECUTE select_user_by_name']
        self.assertEqual(mock_cursor.execute.call_count, 4, 'Expected 4 calls to cursor.execute(). Got {}'.format(mock_cursor.execute.call_count))
        for call, expected_arg in zip(cursor_execute_calls, expected_args):
            args, _ = call
            self.assertTrue(args[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, args[0]))

        self.assertEqual(mock_connection.commit.call_count, 1, 'Expected 1 call to connection.commit(). Got {}'.format(mock_connection.commit.call_count))
        self.assertEqual(mock_cursor.fetchone.call_count, 1, 'Expected 1 call to cursor.fetchone(). Got {}'.format(mock_cursor.fetchall.call_count))

        crypter_decrypt_call = self.__mock_crypter.decrypt.call_args_list
        self.assertEqual(
            self.__mock_crypter.decrypt.call_count, 1,
            'Expected 1 calls to crypter.decrypt(). Got {}'.format(self.__mock_crypter.decrypt.call_count)
        )
        args, _ = crypter_decrypt_call[0]
        expected_args = (record_after['name_encrypted'], record_after['nonce'])
        self.assertSequenceEqual(args, expected_args, 'Expected crypter.decrypt() call with parameter {}. Got {}'.format(expected_args, args))

        self.assertIsInstance(user, UserEntity, 'Expected result to be a UserEntity. Got {}'.format(type(user)))
        self.__assert_user_equal(user, user_expected, omit_id=True)
        self.assertEqual(user.get_id(), record_after['id'], 'Expected user id {}. got {}'.format(record_after['id'], user.get_id()))

    def test_save_with_id(self):
        # prepare data
        user_expected = UserEntity(user_id=1, name='user', password='password', salt='salt', status='status')
        record_after = user_expected.to_dict()
        record_after.pop('name', None)
        record_after['name_hashed'] = 'name_hashed'
        record_after['name_encrypted'] = 'name_encrypted'
        record_after['nonce'] = 'nonce'

        self.__mock_crypter.decrypt.return_value = user_expected.get_name()
        self.__mock_hasher.anonymize.return_value = 'name_hashed'

        mock_cursor = mock.patch('psycopg2.extras.DictCursor').start()
        mock_connection = mock.patch('psycopg2.extensions.connection').start()
        self.__mock_db.cursor.return_value = mock_cursor
        self.__mock_db.connection.return_value = mock_connection
        mock_cursor.fetchone.return_value = record_after

        # execute
        user = self.__user_table.save(user_expected)

        # check
        self.assertFalse(self.__mock_crypter.encrypt.called, 'Crypter.encrypt() was called and should not have been.')

        hasher_anonymize_call = self.__mock_hasher.anonymize.call_args_list
        self.assertEqual(
            self.__mock_hasher.anonymize.call_count, 1,
            'Expected 1 call to hasher.anonymize(). Got {}'.format(self.__mock_hasher.anonymize.call_count)
        )
        arg, _ = hasher_anonymize_call[0]
        expected_arg = (user_expected.get_name(),)
        self.assertEqual(arg, expected_arg, 'Expected hasher.anonymize() call with parameter {}. Got {}'.format(expected_arg, arg))

        cursor_execute_calls = mock_cursor.execute.call_args_list
        expected_args = ['PREPARE update_user', 'EXECUTE update_user', 'PREPARE select_user_by_name', 'EXECUTE select_user_by_name']
        self.assertEqual(mock_cursor.execute.call_count, 4, 'Expected 4 calls to cursor.execute(). Got {}'.format(mock_cursor.execute.call_count))
        for call, expected_arg in zip(cursor_execute_calls, expected_args):
            args, _ = call
            self.assertTrue(args[0].startswith(expected_arg), 'Expected call to cursor.execute() with {}. Got {}'.format(expected_arg, args[0]))

        self.assertEqual(mock_connection.commit.call_count, 1, 'Expected 1 call to connection.commit(). Got {}'.format(mock_connection.commit.call_count))
        self.assertEqual(mock_cursor.fetchone.call_count, 1, 'Expected 1 call to cursor.fetchone(). Got {}'.format(mock_cursor.fetchall.call_count))

        crypter_decrypt_call = self.__mock_crypter.decrypt.call_args_list
        self.assertEqual(
            self.__mock_crypter.decrypt.call_count, 1,
            'Expected 1 calls to crypter.decrypt(). Got {}'.format(self.__mock_crypter.decrypt.call_count)
        )
        args, _ = crypter_decrypt_call[0]
        expected_args = (record_after['name_encrypted'], record_after['nonce'])
        self.assertSequenceEqual(args, expected_args, 'Expected crypter.decrypt() call with parameter {}. Got {}'.format(expected_args, args))

        self.assertIsInstance(user, UserEntity, 'Expected result to be a UserEntity. Got {}'.format(type(user)))
        self.__assert_user_equal(user, user_expected)
