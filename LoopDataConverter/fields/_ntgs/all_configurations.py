from .structure_config import structure_config
from .geology_config import geology_config
from .fault_config import fault_config
from .fold_config import fold_config
from ..datatypes.enums import Datatype


config_map = {
    Datatype.GEOLOGY: geology_config,
    Datatype.STRUCTURE: structure_config,
    Datatype.FAULT: fault_config,
    Datatype.FOLD: fold_config,
    Datatype.DTM: {},
    Datatype.FAULT_ORIENTATION: {},
}