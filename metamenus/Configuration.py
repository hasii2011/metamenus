
from logging import Logger
from logging import getLogger

from metamenus.Singleton import Singleton


class Configuration(Singleton):

    DEFAULT_INDENTATION:     str = 2 * ' '
    DEFAULT_MENU_BAR_PREFIX: str = 'OnMB_'

    def init(self):

        self.logger: Logger = getLogger(__name__)

        self._indentation:   str = Configuration.DEFAULT_INDENTATION
        self._menuBarPrefix: str = Configuration.DEFAULT_MENU_BAR_PREFIX

    @property
    def indentation(self) -> str:
        """
        Indentation level for menus

        Returns:  The number of spaces that menus are indented
        """
        return self._indentation

    @indentation.setter
    def indentation(self, newValue: str):
        self._indentation = newValue

    @property
    def menuBarPrefix(self) -> str:
        """
        The prefix for the method names called on for a menu bar event

        Returns:  The prefix
        """
        return self._menuBarPrefix

    @menuBarPrefix.setter
    def menuBarPrefix(self, newValue: str):
        self._menuBarPrefix = newValue

