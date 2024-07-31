# internal imports
from ..datatypes import Datatype
from .base_converter import BaseConverter
from ..utils import (
    convert_dipdir_terms,
    convert_dip_terms,
    convert_tightness_terms,
    convert_displacement_terms,
)

# external imports
import pandas
import numpy


class NTGSConverter(BaseConverter):
    # TODO: modify class to take fold, fault, and structure layers as arguments
    def __init__(self, data: pandas.DataFrame):
        self.raw_data = data.copy()
        self._type_label = "NTGSConverter"
        self._data = None

    def type(self):
        '''
        The function `type` returns the `_type_label` attribute of the object.
        
        Returns
        -------
            The `type` method is returning the value of the `_type_label` attribute of the object.
        
        '''
        return self._type_label

    def convert_fold_map(self):
        '''
        The function `convert_fold_map` converts dip direction, dip, and tightness terms in the raw data
        to degrees.
        
        '''
        # convert dip direction terms to degrees
        self.raw_data[Datatype.FOLD]["AxialPlaneDipDir"] = self.raw_data[Datatype.FOLD]["AxialPlaneDipDir"].apply(
            lambda x: convert_dipdir_terms(x)
        )
        # convert dip terms to degrees
        self.raw_data[Datatype.FOLD]["AxialPlaneDip"] = self.raw_data[Datatype.FOLD]["AxialPlaneDip"].apply(
            lambda x: convert_dip_terms(x, type="fold")
        )
        # convert tightness terms to degrees
        self.raw_data[Datatype.FOLD]["InterlimbAngle"] = self.raw_data[Datatype.FOLD]["InterlimbAngle"].apply(
            lambda x: convert_tightness_terms(x)
        )

    def convert_fault_map(self):
        '''
        The function `convert_fault_map` converts dip direction, dip, and displacement terms to degrees
        in a DataFrame.
        
        '''
        
        # convert dip direction terms to degrees
        self.raw_data[Datatype.FAULT]["DipDirection"] = self.raw_data[Datatype.FAULT]["DipDirection"].apply(
            lambda x: convert_dipdir_terms(x)
        )
        # convert dip terms to degrees
        self.raw_data[Datatype.FAULT]["Dip"] = self.raw_data[Datatype.FAULT]["Dip"].apply(
            lambda x: convert_dip_terms(x, type="fault")
        )
        self.raw_data[Datatype.FAULT]["Displacement"] = self.raw_data[Datatype.FAULT]["Displacement"].apply(
            lambda x: convert_displacement_terms(x)
        )

    def convert_structure_map(self):
        '''
        This function filters out rows with a dip value of -99 and no estimated dip value, then converts
        dip estimates to floats by averaging the range.
        
        '''
        # discard any rows that has a dip value of -99 and does not have any estimated dip value
        condition = (self.raw_data[Datatype.STRUCTURE]["Dip"] != -99) & (self.raw_data[Datatype.STRUCTURE]["DipEstimate"] != numpy.nan)
        self.raw_data = self.raw_data[Datatype.STRUCTURE][condition]
        # convert dip estimate to float (average of the range)
        condition = self.raw_data[Datatype.STRUCTURE]["Dip"] == -99
        self.raw_data[Datatype.STRUCTURE].loc[condition, "DipEstimate"] = self.raw_data[Datatype.STRUCTURE].loc[
            condition, "DipEstimate"
        ].apply(lambda x: sum(map(float, x.split("-"))) / 2)
        self.raw_data[Datatype.STRUCTURE][condition, "Dip"] = self.raw_data[Datatype.STRUCTURE][condition, "DipEstimate"]

    def convert(self):
        '''
        The function `convert` performs various conversions and copies the raw data in a Python class.
        
        '''
        if self.raw_data[Datatype.FOLD] is not None:
            self.convert_fold_map()
        if self.raw_data[Datatype.FAULT] is not None:
            self.convert_fault_map()
        if self.raw_data[Datatype.STRUCTURE] is not None:
            self.convert_structure_map()

        self._data = self.raw_data.copy()
