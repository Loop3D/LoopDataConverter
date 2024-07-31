from .ntgs_converter import NTGSConverter
from ..datatypes import SurveyName
from ..file_readers import LoopGisReader
from ..input import InputData


class LoopConverter:
    """
    LoopConverter class use the LoopGisReader to look up the correct file
    reader for the input file type and then converting the data to
    Map2Loop format using the adequate converter
    """

    def __init__(self, survey_name: SurveyName, data: InputData, layer: str = None):
        '''
        This function initializes an object with survey name, input data, and optional layer
        information, along with converters for different survey names.

        Parameters
        ----------
        survey_name : SurveyName
            `survey_name` is a parameter that represents the name of a survey. It is expected to be of type
        `SurveyName`.
        data : InputData
            The `data` parameter in the `__init__` method is of type `InputData`. It seems to represent the
        data that will be used in the survey.
        layer : str
            The `layer` parameter in the `__init__` method is a string that represents a specific layer
        within the data. It is an optional parameter with a default value of `None`, which means it can
        be omitted when creating an instance of the class. If provided, it specifies the layer to

        '''
        self._fileData = data
        self._layer = layer
        self._survey_name = survey_name
        self._converters = {
            SurveyName.NTGS: NTGSConverter,
            SurveyName.GA: "",
            SurveyName.GSQ: "",
            SurveyName.GSWA: "",
            SurveyName.GSSA: "",
            SurveyName.GSV: "",
            SurveyName.GSNSW: "",
            SurveyName.MRT: "",
        }

    def read_file(self):
        """
        read the file using the correct file reader
        """
        file_reader = LoopGisReader(self._fileData)
        file_reader.read(self._fileData, self._layer)
        return file_reader.data

    def get_converter(self):
        '''
        This function returns a converter based on the survey name.

        Returns
        -------
            The `get_converter` method is returning the converter associated with the survey name stored in
        the `_survey_name` attribute.

        '''
        return self._converters[self._survey_name]

    def convert(self):
        '''
        This function reads data from a file, uses a converter to process the data, and stores the
        converted data in the object's data attribute.

        '''
        data = self.read_file()
        converter = self.get_converter()
        converter(data)
        self.data = converter._data
