import unittest
from unittest import mock
from Cryptodome.Random import get_random_bytes
from src.crypto.hasher import Hasher


class TestHasher(unittest.TestCase):
    def setUp(self):
        input_validator_patcher = mock.patch('src.validator.input.InputValidator')
        salt = get_random_bytes(16).hex()
        self.__mock_input_validator = input_validator_patcher.start()
        self.__hasher = Hasher(self.__mock_input_validator, salt)

    def tearDown(self):
        del self.__hasher
        mock.patch.stopall()

    def test_hash_with_salt(self):
        salt = get_random_bytes(16).hex()
        string = 'a_string_to_hash'
        self.__mock_input_validator.check_type.return_value = None

        try:
            result_hash, result_salt = self.__hasher.hash(string, salt)
        except ValueError:
            self.fail('ValueError raised despite valid salt {}.'.format(salt))
        self.__mock_input_validator.check_type.assert_called_once_with(salt, str)
        self.assertEqual(result_salt, salt, 'Expected salt {}. Got {}'.format(salt, result_salt))

    def test_hash_no_salt(self):
        string = 'a_string_to_hash'
        self.__mock_input_validator.check_type.return_value = None

        try:
            result_hash, result_salt = self.__hasher.hash(string)
        except ValueError:
            self.fail('ValueError raised despite salt generated on the fly.')
        self.__mock_input_validator.check_type.assert_called_once()

    def test_hash_wrong_salt_type(self):
        string = 'string'
        wrong_salt = 'wrong_salt'
        self.__mock_input_validator.check_type.side_effect = TypeError

        with self.assertRaises(TypeError):
            self.__hasher.hash(string, wrong_salt)
            self.fail('TypeError not raised for salt {}'.format(wrong_salt))
        self.__mock_input_validator.check_type.assert_called_once_with(wrong_salt, str)

    def test_hash_wrong_salt_value(self):
        string = 'string'
        wrong_salts = [
            get_random_bytes(10).hex(),
            get_random_bytes(20).hex(),
            'abc',
        ]
        self.__mock_input_validator.check_type.return_value = None

        for salt in wrong_salts:
            with self.assertRaises(ValueError):
                self.__hasher.hash(string, salt)
                self.fail('ValueError not raised for salt {}'.format(salt))
            self.__mock_input_validator.check_type.assert_called_once_with(salt, str)
            self.__mock_input_validator.reset_mock()

    def test_anonymize(self):
        string = 'a_string_to_anonymize'
        self.__mock_input_validator.check_type.return_value = None

        try:
            result_hash = self.__hasher.anonymize(string)
        except ValueError:
            self.fail('ValueError raised despite valid salt configured.')
        self.__mock_input_validator.check_type.assert_called_once()
