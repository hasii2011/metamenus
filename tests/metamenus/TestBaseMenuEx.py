
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from metamenus.BaseMenuEx import BaseMenuEx
from tests.TestBase import TestBase

# import the class you want to test here
# from pytrek.tests.TestTemplate import TestTemplate


class TestBaseMenuEx(TestBase):
    """
    """
    testMenuBarDescriptor = [
        [
            ['&File'],
            ['  &New\tCtrl+N'],
            ['  &Open...\tCtrl+O'],
            ['  &Save\tCtrl+S'],
            ['  Save &As...\tCtrl+Shift+S'],
            ['  -'],
            ['  Publis&h\tCtrl+Shift+P']
        ]
    ]

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestBaseMenuEx.clsLogger = getLogger(__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger: Logger = TestBaseMenuEx.clsLogger

    def tearDown(self):
        pass

    def testEvolve(self):
        try:
            for mb in TestBaseMenuEx.testMenuBarDescriptor:
                top = BaseMenuEx.evolve(a=mb)
                self.assertIsNotNone(top, 'We should get something')
        except AttributeError as ae:
            self.logger.warning(f'{ae}')


    def testName2(self):
        """Another test"""
        pass


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestBaseMenuEx))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
