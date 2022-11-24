from typing import cast

from logging import Logger
from logging import getLogger

import json
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutDisplayParameters import PyutDisplayParameters
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutModifiers
from pyutmodel.PyutModifier import PyutModifier
from pyutmodel.PyutStereotype import PyutStereotype
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from wx import App

from ogl.OglClass import OglClass

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutv3.encoders.OglEncoder import OglClassEncoder
from tests.TestBase import TestBase


class TestOglClassEncoder(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglClassEncoder.clsLogger = getLogger(__name__)

    def setUp(self):
        self.app: App = App()

        self.logger: Logger = TestOglClassEncoder.clsLogger

    def tearDown(self):
        pass

    def testBasicOglJson(self):

        pyutClass: PyutClass = self._generateBasicPyutClass()
        pyutClass = self._addFields(pyutClass=pyutClass)
        pyutClass = self._addMethods(pyutClass=pyutClass)

        oglClass:  OglClass = OglClass(pyutClass=pyutClass, w=120, h=60)
        oglClass.SetPosition(x=120, y=240)

        # Sort keys so we can verify them
        oglClassStr = json.dumps(oglClass, cls=OglClassEncoder, indent=4, sort_keys=True)
        self.logger.info(f'{oglClassStr=}')

        with open('OglClass.json', 'w') as f:
            f.write(oglClassStr)

    def _generateBasicPyutClass(self) -> PyutClass:

        pyutClass: PyutClass = PyutClass(name='Ozzee')
        pyutClass.id          = 23
        pyutClass.description = 'Soy Gato'
        pyutClass.fileName    = '/tmp/TheBox.txt'
        pyutClass.stereotype  = PyutStereotype(name='model')
        pyutClass.showFields  = False
        pyutClass.displayParameters = PyutDisplayParameters.DISPLAY

        return pyutClass

    def _addFields(self, pyutClass: PyutClass) -> PyutClass:

        protectedField: PyutField = PyutField(name='protectedField',
                                              fieldType=PyutType(value='str'),
                                              visibility=PyutVisibilityEnum.PROTECTED,
                                              defaultValue='gato')
        privateField: PyutField = PyutField(name='privateField',
                                            fieldType=PyutType(value='int'),
                                            visibility=PyutVisibilityEnum.PRIVATE,
                                            defaultValue='6666')
        publicField: PyutField = PyutField(name='publicField',
                                           fieldType=PyutType(value='float'),
                                           visibility=PyutVisibilityEnum.PUBLIC,
                                           defaultValue='23.0')

        pyutClass.addField(field=protectedField)
        pyutClass.addField(field=privateField)
        pyutClass.addField(field=publicField)

        return pyutClass

    def _addMethods(self, pyutClass: PyutClass) -> PyutClass:

        publicMethod: PyutMethod = PyutMethod(name='publicMethod',
                                              visibility=PyutVisibilityEnum.PUBLIC,
                                              returnType=PyutType(value='int'))
        publicMethod.setModifiers(
            PyutModifiers(
                [
                    PyutModifier('abstract'),
                    PyutModifier('reentrant')
                ]
            )
        )
        pyutClass.addMethod(publicMethod)
        return pyutClass


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglClassEncoder))

    return testSuite


if __name__ == '__main__':
    unitTestMain()

"""
                <Method name="privateMethod" visibility="PRIVATE">
                    <Modifier name="static"/>
                    <Return type="str"/>
                    <Param name="noDefaultValueParam" type="str" defaultValue=""/>
                    <SourceCode/>
                </Method>

"""