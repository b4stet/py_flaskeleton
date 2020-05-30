import unittest
from datetime import datetime, timezone
from src.converter.time import TimeConverter


class TestTimeConverter(unittest.TestCase):
    def setUp(self):
        self.__time_converter = TimeConverter()

    def tearDown(self):
        del self.__time_converter

    def test_to_str(self):
        dt = datetime.now(timezone.utc)
        expected = dt.strftime(self.__time_converter.FORMAT)

        result = self.__time_converter.to_str(dt)
        self.assertEqual(result, expected, 'Expected {}. Got {}.'.format(expected, result))

    def test_to_datetime(self):
        dt_str = '2020-05-30 13:37:00 UTC'
        expected = datetime.strptime(dt_str, self.__time_converter.FORMAT)
        expected = expected.astimezone(timezone.utc)

        result = self.__time_converter.to_datetime(dt_str)
        self.assertEqual(result, expected, 'Expected {}. Got {}.'.format(expected, result))

    def test_to_datetime_wrong_format(self):
        dt_wrong_format = [
            '2020-05-30 13:37 UTC',
            '2020-05-30 13:37:00',
            '20200530 13:37',
            '20200530 13:37:00',
            '20200530 13:37:00 UTC',
        ]

        for dt in dt_wrong_format:
            with self.assertRaises(ValueError):
                self.__time_converter.to_datetime(dt)
                self.fail('ValueError not raised for input {}'.format(dt))


if __name__ == '__main__':
    unittest.main()
