
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

    testOptionsMenuBarDescriptor: MenuBarDescriptor = MenuBarDescriptor(
        [
            ['&Options'],
            ['  &Foo',         ("Foo status bar text", ITEM_RADIO)],
            ['  &Bar',         ("Bar status bar text", ITEM_RADIO)],
            ['  -'],
            ['  &Spam',        "check"],
            ['  &Eggs',        ITEM_CHECK],
        ]
    )
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
                top: SItem = BaseMenuEx.evolve(menuDescriptorList=mb)

                self.assertIsNotNone(top, 'We should get something')

                expectedLabel: str = TestBaseMenuEx.testFileMenuBarDescriptor[0][0][0]  # Yuck
                actualLabel:   str = top.GetLabelText()
                self.assertEqual(expectedLabel, actualLabel, 'Menu bar item mismatch')

                expectedChildCount: int = len(TestBaseMenuEx.testFileMenuBarDescriptor[0]) - 1
                actualChildCount:   int = len(top.GetChildren())
                self.assertEqual(expectedChildCount, actualChildCount, 'Menu bar child count mismatch')

        except AttributeError as ae:
            self.logger.warning(f'{ae}')

    def testEvolveFileMenuBarChildren(self):
        for mb in TestBaseMenuEx.testFileMenuBarDescriptor:
            top: SItem = BaseMenuEx.evolve(menuDescriptorList=mb)

            self.assertIsNotNone(top, 'We should get something')

            children: List[SItem] = top.GetChildren()
            self.logger.debug(f'{children}')
            labels: List[str] = self._getLabels()
            self.logger.warning(f'{labels=}')
            for child in children:
                actualLabel: str = child.GetLabelText()
                self.assertTrue(actualLabel in labels, 'This menu entry did not get an SItem')

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


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestBaseMenuEx))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
