from typing import List
from typing import cast
from collections import namedtuple

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import ITEM_RADIO

from metamenus.SItem import MethodNames
from metamenus.types import CustomMethods
from metamenus.types import MenuName
from metamenus.types import MethodName
from tests.TestBase import TestBase

from metamenus.SItem import SItem

TestSItems = namedtuple('TestSItems', 'parentSItem, childSItem')

TEST_METHOD_NAME_PREFIX: str = 'onPrefix'


class TestSItem(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestSItem.clsLogger = getLogger(__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger: Logger = TestSItem.clsLogger

    def tearDown(self):
        pass

    def testGetPath(self):

        testSItems: TestSItems = self._makeTestSItems()

        childSItem:  SItem = testSItems.childSItem

        childPath: str = childSItem.GetPath()

        self.assertIsNotNone(childPath, 'Get something')
        self.assertNotEqual('', childPath, 'Can not be empty')

        expectedPath: str = '&Options  @@@  &Foo'

        self.assertEqual(expectedPath, childPath, 'Path logic seems to have changed')

    def testSetMethodNameStandard(self):

        customMethods: CustomMethods = CustomMethods({})
        testSItems: TestSItems = self._makeTestSItems()

        childSItem:  SItem = testSItems.childSItem

        childSItem.SetMethod(prefix=TEST_METHOD_NAME_PREFIX, customMethods=customMethods)

        expectedMethodName: str = f'{TEST_METHOD_NAME_PREFIX}OptionsFoo'
        actualMethodName:   str = childSItem.GetMethod()

        self.assertEqual(expectedMethodName, actualMethodName, 'Should be use standard method name')

    def testSetMethodNameCustom(self):

        expectedMethodName: str = 'onFoo'

        customMethods: CustomMethods = CustomMethods({
            MenuName('OptionsFoo'): MethodName(expectedMethodName),
            MenuName("OptionsBar"):       MethodName("onBar")
        })

        testSItems: TestSItems = self._makeTestSItems()

        childSItem:  SItem = testSItems.childSItem

        childSItem.SetMethod(prefix=TEST_METHOD_NAME_PREFIX, customMethods=customMethods)

        actualMethodName: str = childSItem.GetMethod()
        self.assertEqual(expectedMethodName, actualMethodName, 'Incorrect method name')

    def testAllMethods(self):

        customMethods: CustomMethods = CustomMethods({})
        testSItems: TestSItems = self._makeTestSItems()

        childSItem:  SItem = testSItems.childSItem

        childSItem.SetMethod(prefix=TEST_METHOD_NAME_PREFIX, customMethods=customMethods)

        methodNames: MethodNames = childSItem.GetAllMethods()
        self.logger.debug(f'{methodNames=}')

        expectedMethodNames: List[str] = [f'{TEST_METHOD_NAME_PREFIX}OptionsFoo', 'OptionsFoo', None]
        for methodName in methodNames.keys():
            self.assertIn(methodName, expectedMethodNames, 'Missing method name')

    def _makeTestSItems(self) -> TestSItems:

        parentParams = ['&Options']
        childParams  = ['  &Foo',         ("Foo status bar text", ITEM_RADIO)]

        parentSItem: SItem = SItem(params=parentParams)
        childSItem:  SItem = SItem(params=childParams)

        childSItem = parentSItem.AddChild(childSItem)

        return TestSItems(parentSItem=parentSItem, childSItem=childSItem)


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestSItem))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
