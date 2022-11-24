
from typing import Dict
from typing import List
from typing import NewType
from typing import Union

from json import JSONEncoder

from miniogl.Shape import Shape

from ogl.OglClass import OglClass
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutModifiers
from pyutmodel.PyutModifier import PyutModifier

EncodedGraphicClass = NewType('EncodedGraphicClass', Dict[str, int])

EncodedField  = NewType('EncodedField', Dict[str, str])
EncodedFields = NewType('EncodedFields', List[EncodedField])

EncodedMethod  = NewType('EncodedMethod', Dict[str, str])
EncodedMethods = NewType('EncodedMethods', List[EncodedMethod])

EncodedModifier  = NewType('EncodedModifier', Dict[str, str])
EncodedModifiers = NewType('EncodedModifiers', List[EncodedModifier])

ModelValueTypes = Union[int, str, float, bool, EncodedFields]
EncodedModel    = NewType('EncodedModel', Dict[str, ModelValueTypes])

Serializable  = Union[OglObject, OglLink, OglInterface2]


class OglClassEncoder(JSONEncoder):
    """
    Knows how to turn OGL Classes into json
    """

    def default(self, o: Serializable):

        if isinstance(o, OglClass):
            pyutClass: PyutClass = o.pyutObject

            graphicDictionary: EncodedGraphicClass = self._encodeGraphicClass(o)
            modelDictionary:   EncodedModel   = self._encodeModelClass(pyutClass=pyutClass)
            return {
                'graphicClass': graphicDictionary,
                'modelClass':   modelDictionary,
            }
        else:
            super().__init__()

    def _encodeGraphicClass(self, shape: Shape) -> EncodedGraphicClass:
        """

        Args:
            shape:  The basic shap class which is root of all

        Returns:  A dictionary with the graphic class attributes
        """
        w, h = shape.GetSize()
        x, y = shape.GetPosition()

        return EncodedGraphicClass({'width': w, 'height': h, 'x': x, 'y': y})

    def _encodeModelClass(self, pyutClass: PyutClass) -> EncodedModel:
        """
        Encodes the class to include its fields, methods, & source code
        Args:
            pyutClass:  The model class to encode

        Returns:  A nice model dictionary
        """
        encodedFields:  EncodedFields  = self._encodeClassFields(pyutClass.fields)
        encodedMethods: EncodedMethods = self._encodeMethods(pyutClass.methods)

        encodedModel: EncodedModel = EncodedModel (
            {
                'name':              pyutClass.name,
                'id':                pyutClass.id,
                'stereotype':        pyutClass.stereotype.name,
                'fileName':          pyutClass.fileName,

                'description':       pyutClass.description,
                'showMethods':       pyutClass.showMethods,
                'showFields':        pyutClass.showFields,
                'displayStereoType': pyutClass.displayStereoType,
                'displayParameters': pyutClass.displayParameters.value,
                'fields':            encodedFields,
                'methods':           encodedMethods,
            }
        )
        return encodedModel

    def _encodeClassFields(self, fields: List[PyutField]) -> EncodedFields:
        """
        Encodes the fields associated with a model class
        Args:
            fields:  The list of data model fields

        Returns:    A list of encoded data class model fields
        """
        encodedFields: EncodedFields = EncodedFields([])
        for field in fields:
            encodedField: EncodedField = self._encodeField(field=field)
            encodedFields.append(encodedField)
        return encodedFields

    def _encodeField(self, field: PyutField) -> EncodedField:
        """
        Encode a specific field
        Args:
            field:  The model field

        Returns:    Encoded field
        """
        return EncodedField(
            {
                'name':         field.name,
                'visibility':   field.visibility.value,
                'type':         field.type.value,
                'defaultValue': field.defaultValue
            }
        )

    def _encodeMethods(self, pyutMethods: List[PyutMethod]):

        encodedMethods: EncodedMethods = EncodedMethods([])
        for method in pyutMethods:
            encodedMethod: EncodedMethod = self._encodeMethod(method)
            encodedMethods.append(encodedMethod)

        return encodedMethods

    def _encodeMethod(self, pyutMethod: PyutMethod) -> EncodedMethod:
        encodedModifiers: EncodedModifiers = self._encodeModifiers(pyutMethod.modifiers)
        return EncodedMethod(
            {
                'name':       pyutMethod.name,
                'visibility': pyutMethod.visibility.value,
                'returnType': pyutMethod.returnType.value,
                'modifiers':  encodedModifiers
            }
        )

    def _encodeModifiers(self, pyutModifiers: PyutModifiers) -> EncodedModifiers:
        encodedModifiers: EncodedModifiers = EncodedModifiers([])

        for modifier in pyutModifiers:
            encodedModifier = self._encodeModifier(modifier)
            encodedModifiers.append(encodedModifier)

        return encodedModifiers

    def _encodeModifier(self, pyutModifier: PyutModifier) -> EncodedModifier:
        return EncodedModifier({
            'name': pyutModifier.name
        })
