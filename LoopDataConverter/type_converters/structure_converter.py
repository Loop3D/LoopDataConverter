from ..fields._ntgs import structure_config
from .base_converter import BaseTypeConverter
from map2loop.config import Config


class StructureConverter(BaseTypeConverter):
    def __init__(self, data):
        self.data = data
        self._type_label = "StructureConverter"

    def type(self):

        return self._type_label

    def set(self):
        pass

    def get(self):
        pass

    def map(self):
        pass

    def convert(self):
        pass
     