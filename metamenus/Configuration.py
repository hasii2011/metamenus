
from logging import Logger
from logging import getLogger

from metamenus.Singleton import Singleton


class Configuration(Singleton):

    DEFAULT_INDENTATION: str = 2 * ' '

    def init(self):

        self.logger: Logger = getLogger(__name__)

        self._indentation: str = Configuration.DEFAULT_INDENTATION

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
