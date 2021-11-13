
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

    def testDefaultIndentation(self):

        expectedIndentation: str = Configuration.DEFAULT_INDENTATION
        actualIndentation:   str = self._configuration.indentation
        self.assertEqual(expectedIndentation, actualIndentation, 'Default indentation has changed')

    def testDefaultMenuBarPrefix(self):

        expectedPrefix: str = Configuration.DEFAULT_MENU_BAR_PREFIX
        actualPrefix:   str = self._configuration.menuBarPrefix
        self.assertEqual(expectedPrefix, actualPrefix, 'Default menu bar method prefix has changed')

    def testDefaultMenuPrefix(self):

        expectedPrefix: str = Configuration.DEFAULT_MENU_PREFIX
        actualPrefix:   str = self._configuration.menuPrefix
        self.assertEqual(expectedPrefix, actualPrefix, 'Default menu method prefix has changed')

    def testDefaultVerboseWarnings(self):

        expectedValue: bool = Configuration.DEFAULT_VERBOSE_WARNINGS
        actualValue:   bool = self._configuration.verboseWarnings
        self.assertEqual(expectedValue, actualValue, 'Verbosity default has changed')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestConfiguration))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
