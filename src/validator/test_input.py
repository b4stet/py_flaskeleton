import unittest
from src.validator.input import InputValidator


class TestInputValidator(unittest.TestCase):
    def setUp(self):
        self.__input_validator = InputValidator()

    def tearDown(self):
        del self.__input_validator

    def test_check_mandatory_not_none(self):
        field_name = 'a_field'
        value = 'not_empty'

        try:
            self.__input_validator.check_mandatory(value, field_name)
        except KeyError:
            self.fail('KeyError raised despite not empty.')

    def test_check_mandatory_none(self):
        field_name = 'a_field'

        with self.assertRaises(KeyError):
            self.__input_validator.check_mandatory(None, field_name)
            self.fail('KeyError not raised for value None.')

    def test_check_type_right(self):
        good_types = {
            str: '',
            int: 0,
            bytes: b'',
            list: [],
            dict: {},
            tuple: (),
        }
        for expected_type, value in good_types.items():
            try:
                self.__input_validator.check_type(value, expected_type)
            except TypeError:
                self.fail('TypeError raised despite valid input {} as type {}.'.format(value, expected_type.__name__))

    def test_check_type_wrong(self):
        wrong_types = {
            str: 0,
            int: '0',
            bytes: 0x00,
            list: {},
            dict: (),
            tuple: [],
        }

        for expected_type, value in wrong_types.items():
            with self.assertRaises(TypeError):
                self.__input_validator.check_type(value, expected_type)
                self.fail('TypeError not raised for value {} as type {}.'.format(value, expected_type.__name__))


if __name__ == '__main__':
    unittest.main()
