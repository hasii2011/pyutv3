
import logging
import logging.config

import json

from click import command
from click import option
from click import version_option
from pkg_resources import resource_filename

from wx import App

from pyutv3.PyutV3Frame import PyutV3Frame

__version__ = "3.0.0"


JSON_LOGGING_CONFIG_FILENAME: str = 'loggingConfiguration.json'
RESOURCES_PACKAGE_NAME:       str = 'pyutv3.resources'


class PyutV3(App):

    WINDOW_WIDTH:  int = 900
    WINDOW_HEIGHT: int = 500

    def __init__(self, redirect: bool = False):

        super(PyutV3, self).__init__(redirect=redirect)

    def OnInit(self) -> bool:

        PyutV3.setUpLogging()

        self._frameTop: PyutV3Frame = PyutV3Frame()

        self._frameTop.Show(True)

        return True

    @classmethod
    def setUpLogging(cls):
        """"""
        loggingConfigFilename: str = cls.findLoggingConfig()

        with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    @classmethod
    def findLoggingConfig(cls) -> str:

        fqFileName = resource_filename(RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

        return fqFileName

    def loadXmlFile(self, fqFileName: str):
        """

        Args:
            fqFileName: full qualified file name
        """
        self._frameTop.loadXmlFile(fqFileName=fqFileName)


@command()
@version_option(version=f'{__version__}', message='%(version)s')
@option('-i', '--input-file', required=False, help='The input .xml file to preload on startup.')
def commandHandler(input_file: str):

    if input_file is not None:
        testApp: PyutV3 = PyutV3(redirect=False)
        testApp.loadXmlFile(input_file)
    else:
        testApp = PyutV3(redirect=False)

    testApp.MainLoop()


if __name__ == "__main__":

    commandHandler()
