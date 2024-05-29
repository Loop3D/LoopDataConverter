from abc import ABC, abstractmethod

class BaseTypeConverter(ABC):

    def __init__(self):
        self._type_label = "BaseTypeConverter"

    def type(self):
        return self._type_label
    
    @abstractmethod
    def set(self):
        pass
    
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def map(self):
        pass

    @abstractmethod
    def convert(self):
        pass
    
