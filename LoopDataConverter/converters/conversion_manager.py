from .ntgs_converter import NTGSConverter
from ..datatypes import SurveyName


class ConversionManager:
    def __init__(self, file):
        self._converters = {
            SurveyName.NTGS: NTGSConverter,
            SurveyName.GA: "",
            SurveyName.GSQ: "",
            SurveyName.GSWA: "",
            SurveyName.GSSA: "",
            SurveyName.GSV: "",
            SurveyName.MRT: "",
            SurveyName.GSNSW: "",
        }

    # the conversion manager is responsible for looking up the correct file reader for the given file type
    # and then converting the data to the correct format using the correct converter

