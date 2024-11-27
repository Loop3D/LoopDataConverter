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


class NTGSConverter(BaseConverter):
    # TODO: modify class to take fold, fault, and structure layers as arguments
    def __init__(self, data: pandas.DataFrame):
        self.raw_data = data.copy()
        self.update_empty_rows()
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

    def update_empty_rows(self):
        '''
        The function `update_empty_rows` updates empty rows in the DataFrame with NaN values.

        Parameters
        ----------
            None

        This method operates on the DataFrames stored in the class and replaces all empty values
        (e.g., empty strings, None, NaN) with NaN across the specified tables.
        '''

        # List of tables (DataFrames) to update
        tables_to_update = [Datatype.FOLD, Datatype.FAULT, Datatype.STRUCTURE]

        for table in tables_to_update:
            # Replace empty strings, None, or NaN with np.nan in the entire table
            self.raw_data[table] = self.raw_data[table].map(
                lambda x: "NaN" if pandas.isna(x) or x == "" or x is None else x
            )

    def convert_fold_map(self):
        '''
        The function `convert_fold_map` converts dip direction, dip, and tightness terms in the raw data
        to degrees.

        '''
        # # rename columns
        # if "AxialPlaneDipDir" in self.raw_data[Datatype.FOLD].columns:
        #     self.raw_data[Datatype.FOLD] = self.raw_data[Datatype.FOLD].rename(columns={'AxialPlaneDipDir': 'AxPlDipDir'})
        # if "AxialPlaneDip" in self.raw_data[Datatype.FOLD].columns:
        #     self.raw_data[Datatype.FOLD] = self.raw_data[Datatype.FOLD].rename(columns={'AxialPlaneDip': 'AxPlaneDip'})
        # if "AxialPlane" in self.raw_data[Datatype.FOLD].columns:
        #     self.raw_data[Datatype.FOLD] = self.raw_data[Datatype.FOLD].rename(columns={'AxialPlane': 'AxPlDipDir'})
        # if "AxialPla_1" in self.raw_data[Datatype.FOLD].columns:
        #     self.raw_data[Datatype.FOLD] = self.raw_data[Datatype.FOLD].rename(columns={'AxialPla_1': 'AxPlaneDip'})
        # if "InterlimbA" in self.raw_data[Datatype.FOLD].columns:
        #     self.raw_data[Datatype.FOLD] = self.raw_data[Datatype.FOLD].rename(columns={'InterlimbA': 'Interlimb'})
            
        # convert dip direction terms to degrees
        self.raw_data[Datatype.FOLD]["AxPlDipDir"] = self.raw_data[Datatype.FOLD]["AxPlDipDir"].apply(
            lambda x: convert_dipdir_terms(x)
        )
        
        # convert dip terms to degrees
        self.raw_data[Datatype.FOLD]["AxPlDip"] = self.raw_data[Datatype.FOLD][
            "AxPlDip"
        ].apply(lambda x: convert_dip_terms(x, type="fold"))
        # convert tightness terms to degrees
        self.raw_data[Datatype.FOLD]["IntlimbAng"] = self.raw_data[Datatype.FOLD]["IntlimbAng"].apply(
            lambda x: convert_tightness_terms(x)
        )

    def convert_fault_map(self):
        '''
        The function `convert_fault_map` converts dip direction, dip, and displacement terms to degrees
        in a DataFrame.

        '''

        # convert dip direction terms to degrees

        self.raw_data[Datatype.FAULT]["DipDir"] = self.raw_data[Datatype.FAULT][
            "DipDir"
        ].apply(lambda x: convert_dipdir_terms(x))
        # convert dip terms to degrees
        self.raw_data[Datatype.FAULT]["Dip"] = self.raw_data[Datatype.FAULT]["Dip"].apply(
            lambda x: convert_dip_terms(x, type="fault")
        )
        # convert displacement terms to meters
        self.raw_data[Datatype.FAULT]["Displace"] = self.raw_data[Datatype.FAULT]["Displace"].apply(
            lambda x: convert_displacement_terms(x)
        )

    def convert_structure_map(self):
        '''
        This function filters out rows with a dip value of -99 and no estimated dip value, then converts
        dip estimates to floats by averaging the range.

        '''
        # select any rows that has a dip value of -99 and have any estimated dip value
        condition = (self.raw_data[Datatype.STRUCTURE]["Dip"] == -99) & (
            self.raw_data[Datatype.STRUCTURE]["DipEst"] != "NaN"
        )

        # convert dip estimate to float (average of the range)
        self.raw_data[Datatype.STRUCTURE].loc[condition, "Dip"] = (
            self.raw_data[Datatype.STRUCTURE]
            .loc[condition, "DipEst"]
            .apply(lambda x: convert_dip_terms(x, type="structure"))
        )

        # discard any rows that has a dip value of -99 and does not have any estimated dip value
        condition = (self.raw_data[Datatype.STRUCTURE]["Dip"] == -99) & (
            self.raw_data[Datatype.STRUCTURE]["DipEst"] == "NaN"
        )
        self.raw_data[Datatype.STRUCTURE] = self.raw_data[Datatype.STRUCTURE][~condition]

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
