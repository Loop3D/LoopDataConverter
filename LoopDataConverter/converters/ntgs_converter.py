from .base_converter import BaseConverter
import pandas
import numpy


class NTGSConverter(BaseConverter):
    def __init__(self, data: pandas.DataFrame):
        self.data = data
        self._type_label = "NTGSConverter"

    def type(self):
        return self._type_label

    def convert_fold_map(self):
        pass

    def convert_fault_map(self):
        pass

    def convert_geology_map(self):
        pass

    def convert_structure_map(self):
        # discard any rows that has a dip value of -99 and does not have any esimated dip value
        condition = (self.data["Dip"] != -99) & (self.data["DipEstimate"] != numpy.nan)
        self.data = self.data[condition]
        # convert dip estimate to float (average of the range)
        condition = self.data["Dip"] == -99
        self.data.loc[condition, "DipEstimate"] = self.data.loc[
            condition, "DipEstimate"
        ].apply(lambda x: sum(map(float, x.split("-"))) / 2)
        self.data[condition, "Dip"] = self.data[condition, "DipEstimate"]

    def convert(self):
        pass
