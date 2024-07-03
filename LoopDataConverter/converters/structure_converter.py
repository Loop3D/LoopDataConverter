from .base_converter import BaseTypeConverter

import pandas
import numpy
import beartype


@beartype.beartype
class StructureConverter(BaseTypeConverter):
    def __init__(self, data: pandas.DataFrame):
        self.data = data
        self._type_label = "StructureConverter"

    def type(self):
        return self._type_label

    def convert(self):
        # discard any rows that has a dip value of -99 and does not have any esimated dip value
        condition = (self.data["Dip"] != -99) & (self.data["DipEstimate"] != numpy.nan)
        self.data = self.data[condition]
        # convert dip estimate to float (average of the range)
        condition = self.data["Dip"] == -99
        self.data.loc[condition, "DipEstimate"] = self.data.loc[
            condition, "DipEstimate"
        ].apply(lambda x: sum(map(float, x.split("-"))) / 2)
        self.data[condition, "Dip"] = self.data[condition, "DipEstimate"]
