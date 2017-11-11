import unittest
from .test_api import TestAPI

suite = unittest.TestLoader().loadTestsFromTestCase(TestAPI)
