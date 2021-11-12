
from logging import Logger
from logging import getLogger

from metamenus.Singleton import Singleton


class Configuration(Singleton):

    def init(self):

        self.logger: Logger = getLogger(__name__)

        self.indentation: str = 2 * " "
        """
        Indentation level for menus
        """