from dataclasses import dataclass
from ..datatypes import Datatype



@dataclass
class InputData:
    geology: Datatype.GEOLOGY = None
    structure: Datatype.STRUCTURE = None
    fault: Datatype.FAULT = None
    fold: Datatype.FOLD = None


    def __getitem__(self, datatype: Datatype):

        return self.__dict__[datatype]

@dataclass 
class OutputData(InputData):
    
    def __getitem__(self, datatype: Datatype):
        return super().__getitem__(datatype)