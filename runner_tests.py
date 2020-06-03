import unittest

from src.converter import test_time
from src.validator import test_input
from src.validator import test_user as test_user_validator
from src.crypto import test_crypter, test_hasher
from src.table import test_user as test_user_table
from src.table import test_db_migrator

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_time))
suite.addTests(loader.loadTestsFromModule(test_input))
suite.addTests(loader.loadTestsFromModule(test_user_validator))
suite.addTests(loader.loadTestsFromModule(test_crypter))
suite.addTests(loader.loadTestsFromModule(test_hasher))
suite.addTests(loader.loadTestsFromModule(test_user_table))
suite.addTests(loader.loadTestsFromModule(test_db_migrator))

runner = unittest.TextTestRunner(verbosity=3)
runner.run(suite)
