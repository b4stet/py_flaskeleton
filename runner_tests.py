import unittest

from src.converter import test_time
from src.validator import test_input, test_user
from src.crypto import test_crypter, test_hasher

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_time))
suite.addTests(loader.loadTestsFromModule(test_input))
suite.addTests(loader.loadTestsFromModule(test_user))
suite.addTests(loader.loadTestsFromModule(test_crypter))
suite.addTests(loader.loadTestsFromModule(test_hasher))

runner = unittest.TextTestRunner(verbosity=3)
runner.run(suite)
