
import logging
import logging.config

import json

from pkg_resources import resource_filename

from wx import App
from wx import Locale
from wx import Platform

from demo.DemoFrame import DemoFrame


class DemoApp(App):
    RESOURCES_PACKAGE_NAME: str = 'demo.resources'
    JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"

    def OnInit(self):

        import wx

        self._setUpLogging()
        # Find languages available on this system:
        self.available_languages = {}
        for i in [i for i in dir(wx) if i.startswith("LANGUAGE_")]:
            if i not in ["LANGUAGE_DEFAULT",
                         "LANGUAGE_UNKNOWN",
                         "LANGUAGE_USER_DEFINED"]:
                at = getattr(wx, i)
                if Locale().IsAvailable(at):
                    self.available_languages[i] = at

        DemoFrame().Show(True)

        print(f'Demonstration running on platform - {Platform}')
        return True

    def _setUpLogging(self):
        """
        """
        loggingConfigFilename: str = self._findLoggingConfig()

        with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    def _findLoggingConfig(self) -> str:

        fqFileName = resource_filename(DemoApp.RESOURCES_PACKAGE_NAME, DemoApp.JSON_LOGGING_CONFIG_FILENAME)

        return fqFileName
