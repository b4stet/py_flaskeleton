import unittest
from src.validator.user import UserValidator
from src.entity.user import UserEntity


class TestUserValidator(unittest.TestCase):
    def setUp(self):
        self.__user_validator = UserValidator()

    def tearDown(self):
        del self.__user_validator

    def test_check_name(self):
        name = UserEntity.NAME_CHARSET
        try:
            self.__user_validator.check_name(name)
        except ValueError:
            self.fail('ValueError raised despite valid name {}.'.format(name))

    def test_check_name_wrong_charset(self):
        wrong_names = [
            'n4m3!',
            'n4?m3',
            '"n4m3',
            "n4'm3",
            'nâm3!',
        ]

        for name in wrong_names:
            with self.assertRaises(ValueError):
                self.__user_validator.check_name(name)
                self.fail('ValueError not raised for name {}.'.format(name))

    def test_check_password(self):
        password = UserEntity.PASSWORD_CHARSET
        try:
            self.__user_validator.check_password(password)
        except ValueError:
            self.fail('ValueError raised despite valid password {}.'.format(password))

    def test_check_password_wrong_charset(self):
        wrong_passwords = [
            'p4ssw0rd"',
            "p4ss'w0rd",
            '@p4ssw0rd',
            'pâssw0rd',
            'p4ss#w0rd',
        ]

        for password in wrong_passwords:
            with self.assertRaises(ValueError):
                self.__user_validator.check_password(password)
                self.fail('ValueError not raised for password {}.'.format(password))

    def test_check_status(self):
        for status in UserEntity.STATUSES:
            try:
                self.__user_validator.check_status(status)
            except ValueError:
                self.fail('ValueError raised despite valid status {}.'.format(status))

    def test_check_status_unkown(self):
        wrong_statuses = [
            True,
            False,
            'Enabled',
            'Disabled',
            0,
            1,
        ]

        for status in wrong_statuses:
            with self.assertRaises(ValueError):
                self.__user_validator.check_status(status)
                self.fail('ValueError not raised for status {}.'.format(status))


if __name__ == '__main__':
    unittest.main()
