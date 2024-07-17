
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import ITEM_CHECK
from wx import ITEM_RADIO

from metamenus.BaseMenuEx import BaseMenuEx
from metamenus.SItem import SItem
from metamenus.SItem import SItems

from metamenus.internal.ITypes import MenuBarDescriptor

from tests.TestBase import TestBase


class TestBaseMenuEx(TestBase):
    """
    """
    # noinspection SpellCheckingInspection
    testFileMenuBarDescriptor: MenuBarDescriptor = MenuBarDescriptor([
        [
            ['&File'],
            ['  &New\tCtrl+N'],
            ['  &Open...\tCtrl+O'],
            ['  &Save\tCtrl+S'],
            ['  Save &As...\tCtrl+Shift+S'],
            ['  -'],
            ['  Publis&h\tCtrl+Shift+P']
        ]
    ])

    testOptionsMenuBarDescriptor: MenuBarDescriptor = MenuBarDescriptor([
        [
            ['&Options'],
            ['  &Foo',         ("Foo status bar text", ITEM_RADIO)],
            ['  &Bar',         ("Bar status bar text", ITEM_RADIO)],
            ['  -'],
            ['  &Spam',        "check"],
            ['  &Eggs',        ITEM_CHECK],
        ]
    ])

    DEEPEST_ITEM_NAME: str = 'Item.2'

    testDeepMenuBarDescriptor: MenuBarDescriptor = MenuBarDescriptor([
        [
            ['Top'],
            ['  Item.1'],
            ['    Item.1.1'],
            ['    Item.1.2'],
            ['  Item.2'],           # Builds the deepest number of items
            ['    Item.2.1'],
            ['    Item.2.2'],
            ['      Item.2.2.1'],
            ['      Item.2.2.2'],
            ['        Item.2.2.2.1'],
            ['        Item.2.2.2.2'],
            ['  Item.3'],
            ['    Item.3.1'],
            ['    Item.3 2'],
            ['  Item.4'],
        ]
    ])
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

    def testEvolveFileMenuBar(self):
        try:
            for mb in TestBaseMenuEx.testFileMenuBarDescriptor:
                top: SItem = BaseMenuEx.evolve(menuBarDescriptor=mb)

                self.assertIsNotNone(top, 'We should get something')

                expectedLabel: str = TestBaseMenuEx.testFileMenuBarDescriptor[0][0][0]  # Yuck
                actualLabel:   str = top.GetLabelText()
                self.assertEqual(expectedLabel, actualLabel, 'File Menu bar item mismatch')

                expectedChildCount: int = len(TestBaseMenuEx.testFileMenuBarDescriptor[0]) - 1
                actualChildCount:   int = len(top.GetChildren())
                self.assertEqual(expectedChildCount, actualChildCount, 'Menu bar child count mismatch')

        except AttributeError as ae:
            self.logger.warning(f'{ae}')

    def testEvolveFileMenuBarChildren(self):
        for mb in TestBaseMenuEx.testFileMenuBarDescriptor:
            top: SItem = BaseMenuEx.evolve(menuBarDescriptor=mb)

            self.assertIsNotNone(top, 'We should get something')

            children: List[SItem] = top.GetChildren()
            self.logger.debug(f'{children}')
            labels: List[str] = self._getLabels()
            self.logger.debug(f'{labels=}')
            for child in children:
                actualLabel: str = child.GetLabelText()
                self.assertTrue(actualLabel in labels, 'This menu entry did not get an SItem')

    def testEvolveOptionsMenuBar(self):

        for mb in TestBaseMenuEx.testOptionsMenuBarDescriptor:
            top: SItem = BaseMenuEx.evolve(menuBarDescriptor=mb)

            self.assertIsNotNone(top, 'We should get something')

            expectedLabel: str = TestBaseMenuEx.testOptionsMenuBarDescriptor[0][0][0]  # Yuck
            actualLabel:   str = top.GetLabelText()
            self.assertEqual(expectedLabel, actualLabel, 'Options Menu bar item mismatch')

    def testEvolveDeepMenuBar(self):

        mb: MenuBarDescriptor = TestBaseMenuEx.testDeepMenuBarDescriptor[0]
        top: SItem            = BaseMenuEx.evolve(menuBarDescriptor=mb)

        self.assertIsNotNone(top, 'We should get something for our deep menu')

        deepSItem: SItem = self._findTopDeepSItems(top=top)
        self.assertIsNotNone(deepSItem, 'Oops did the names change!')

        expectedName: str = TestBaseMenuEx.DEEPEST_ITEM_NAME
        actualName:   str = deepSItem.GetLabel()
        self.assertEqual(expectedName, actualName, 'I could not find that SItem')

        sItems: SItems = deepSItem.GetChildWithChildren()

        self.assertTrue(len(sItems) == 2, 'Incorrect number of child items that also have children')
        childLabels: List[str] = ['Item.2.2', 'Item.2.2.2']
        for foundSItem in sItems:
            actualLabel: str = foundSItem.GetLabel()
            self.assertIn(actualLabel, childLabels, 'This is not one of our nested items')

    def _getLabels(self) -> List[str]:

        labels: List[str] = []
        for topMenuDescriptor in TestBaseMenuEx.testFileMenuBarDescriptor:
            for menuDescriptor in topMenuDescriptor:
                label: str = self._getLabel(menuDescriptor[0])
                labels.append(label)

        return labels

    def _getLabel(self, menuDescriptor: str) -> str:

        label:     str = menuDescriptor.strip()
        labelText: str = label.split("\t")[0].strip()

        return labelText

    def _findTopDeepSItems(self, top: SItem) -> SItem:
        """
        I hard code the name for now;
        Did I mention that I hate recursion !!!

        Returns:  The SItem
        """
        deepSItem:       SItem  = cast(SItem, None)
        children:        SItems = top.GetChildren()

        for childItem in children:
            childLabel: str = childItem.GetLabel()
            self.logger.debug(f'{childLabel=}')
            if childLabel == TestBaseMenuEx.DEEPEST_ITEM_NAME:
                return childItem
            else:
                deepSItem = self._findTopDeepSItems(childItem)
                if deepSItem is not None:
                    break

        return deepSItem


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestBaseMenuEx))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
