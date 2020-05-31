import unittest
from unittest import mock
from Cryptodome.Random import get_random_bytes
from src.crypto.crypter import Crypter


class TestCrypter(unittest.TestCase):
    def setUp(self):
        input_validator_patcher = mock.patch('src.validator.input.InputValidator')
        key = get_random_bytes(32).hex()
        self.__mock_input_validator = input_validator_patcher.start()
        self.__crypter = Crypter(self.__mock_input_validator, key)

    def tearDown(self):
        del self.__crypter
        mock.patch.stopall()

    def test_encrypt_with_nonce(self):
        nonce = get_random_bytes(16).hex()
        plains = [
            'plain_short',
            'plain_____________________1block',
            'plain_________________________long',
        ]
        self.__mock_input_validator.check_type.return_value = None

        for plain in plains:
            try:
                result_cipher, result_nonce = self.__crypter.encrypt(plain, nonce)
            except ValueError:
                self.fail('ValueError raised despite valid nonce {}.'.format(nonce))
            self.__mock_input_validator.check_type.assert_called_once_with(nonce, str)
            self.assertEqual(result_nonce, nonce, 'Expected nonce {}. Got {}'.format(nonce, result_nonce))
            self.__mock_input_validator.reset_mock()

    def test_encrypt_no_nonce(self):
        plains = [
            'plain_short',
            'plain_____________________1block',
            'plain_________________________long',
        ]
        self.__mock_input_validator.check_type.return_value = None

        for plain in plains:
            try:
                result_cipher, result_nonce = self.__crypter.encrypt(plain)
            except ValueError:
                self.fail('ValueError raised despite nonce generated on the fly.')
            self.__mock_input_validator.check_type.assert_called_once()
            self.__mock_input_validator.reset_mock()

    def test_encrypt_wrong_nonce_type(self):
        plain = 'plain'
        wrong_nonce = 'wrong_nonce'
        self.__mock_input_validator.check_type.side_effect = TypeError

        with self.assertRaises(TypeError):
            self.__crypter.encrypt(plain, wrong_nonce)
            self.fail('TypeError not raised for nonce {}'.format(wrong_nonce))
        self.__mock_input_validator.check_type.assert_called_once_with(wrong_nonce, str)

    def test_encrypt_wrong_nonce_value(self):
        plain = 'plain'
        wrong_nonces = [
            get_random_bytes(10).hex(),
            get_random_bytes(20).hex(),
            'abc',
        ]
        self.__mock_input_validator.check_type.return_value = None

        for nonce in wrong_nonces:
            with self.assertRaises(ValueError):
                self.__crypter.encrypt(plain, nonce)
                self.fail('ValueError not raised for nonce {}'.format(nonce))
            self.__mock_input_validator.check_type.assert_called_once_with(nonce, str)
            self.__mock_input_validator.reset_mock()

    def test_decrypt(self):
        plains = [
            'plain_short',
            'plain_____________________1block',
            'plain_________________________long',
        ]
        self.__mock_input_validator.check_type.return_value = None

        for plain in plains:
            cipher, nonce = self.__crypter.encrypt(plain)
            result = self.__crypter.decrypt(cipher, nonce)
            self.assertEqual(result, plain, 'Expected plaintext {}. Got {}'.format(plain, result))
