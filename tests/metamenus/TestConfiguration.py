
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

# import the class you want to test here
from metamenus.Configuration import Configuration


class TestConfiguration(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestConfiguration.clsLogger = getLogger(__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger: Logger = TestConfiguration.clsLogger
        self._configuration: Configuration = Configuration()

    def tearDown(self):
        pass

    def testName1(self):
        pass

    def testName2(self):
        """Another test"""
        pass


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestConfiguration))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
