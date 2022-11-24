
import logging
import logging.config

from os import system as osSystem

import json

from unittest import TestCase

from pkg_resources import resource_filename

from wx import App
from wx import Frame
from wx import ID_ANY

from miniogl.DiagramFrame import DiagramFrame

JSON_LOGGING_CONFIG_FILENAME: str = "testLoggingConfig.json"
TEST_DIRECTORY:               str = 'tests'


class DummyApp(App):
    def OnInit(self):
        return True


class TestBase(TestCase):

    RESOURCES_PACKAGE_NAME:                   str = 'tests.resources'
    RESOURCES_TEST_FILES_PACKAGE_NAME:        str = f'{RESOURCES_PACKAGE_NAME}.testfiles'

    EXTERNAL_DIFF_PROGRAM:    str = 'diff'

    def setUp(self):
        self._app:   DummyApp = DummyApp()

        #  Create frame
        baseFrame: Frame = Frame(None, ID_ANY, "", size=(10, 10))
        # noinspection PyTypeChecker
        umlFrame = DiagramFrame(baseFrame)
        umlFrame.Show(True)

    def tearDown(self):
        self._app.OnExit()

    """
    A base unit test class to initialize some logging stuff we need
    """
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

        fqFileName = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

        return fqFileName

    def _getFullyQualifiedTestFilePath(self, testFileName: str) -> str:

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_FILES_PACKAGE_NAME, testFileName)
        return fqFileName

    def _runDiff(self, expectedContentsFileName: str, actualContentsFileName) -> int:

        status: int = osSystem(f'{TestBase.EXTERNAL_DIFF_PROGRAM} {expectedContentsFileName} {actualContentsFileName}')

        return status
