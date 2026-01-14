from ..datatypes import Datatype
from .base_converter import BaseConverter
from ..fields.base_config import BaseConfig
from ..utils import (
    convert_dipdir_terms,
    convert_dip_terms,
    convert_tightness_terms,
    convert_displacement_terms,
)

import pandas
import geopandas


class GenericConverter(BaseConverter):
    def __init__(self, data, config: BaseConfig):
        super().__init__()
        if not isinstance(config, BaseConfig):
            raise TypeError("config must be an instance of BaseConfig")

        self.raw_data = data.copy()
        self.update_empty_rows()
        self._type_label = "GenericConverter"
        self._config = config
        self.crs = (
            self.raw_data[Datatype.GEOLOGY].crs
            if self.raw_data[Datatype.GEOLOGY] is not None
            else None
        )
        self._data = None

    def update_empty_rows(self):
        """
        Replace empty values with NaN across the fold, fault, and structure tables.
        """
        tables_to_update = [Datatype.FOLD, Datatype.FAULT, Datatype.STRUCTURE]

        for table in tables_to_update:
            self.raw_data[table] = self.raw_data[table].map(
                lambda x: "NaN" if pandas.isna(x) or x == "" or x is None else x
            )

    def convert_fold_map(self):
        """
        Convert dip direction, dip, and tightness terms to degrees using config columns.
        """
        fold_config = self._config["fold"]
        dipdir_column = fold_config["axial_plane_dipdir_column"]
        dip_column = fold_config["axial_plane_dip_column"]
        tightness_column = fold_config["tightness_column"]

        self.raw_data[Datatype.FOLD][dipdir_column] = self.raw_data[Datatype.FOLD][
            dipdir_column
        ].apply(lambda x: convert_dipdir_terms(x))

        self.raw_data[Datatype.FOLD][dip_column] = self.raw_data[Datatype.FOLD][dip_column].apply(
            lambda x: convert_dip_terms(x, type="fold")
        )

        self.raw_data[Datatype.FOLD][tightness_column] = self.raw_data[Datatype.FOLD][
            tightness_column
        ].apply(lambda x: convert_tightness_terms(x))

    def convert_fault_map(self):
        """
        Convert dip direction, dip, and displacement terms to degrees/meters using config columns.
        """
        fault_config = self._config["fault"]
        dipdir_column = fault_config["dipdir_column"]
        dip_column = fault_config["dip_column"]
        displacement_column = fault_config["displacement_column"]

        self.raw_data[Datatype.FAULT][dipdir_column] = self.raw_data[Datatype.FAULT][
            dipdir_column
        ].apply(lambda x: convert_dipdir_terms(x))

        self.raw_data[Datatype.FAULT][dip_column] = self.raw_data[Datatype.FAULT][dip_column].apply(
            lambda x: convert_dip_terms(x, type="fault")
        )

        self.raw_data[Datatype.FAULT][displacement_column] = self.raw_data[Datatype.FAULT][
            displacement_column
        ].apply(lambda x: convert_displacement_terms(x))

        self.raw_data[Datatype.FAULT]["centroid"] = self.raw_data[Datatype.FAULT].geometry.centroid
        centroid_series = self.raw_data[Datatype.FAULT]["centroid"]
        self.raw_data[Datatype.FAULT]["centroid_x"] = centroid_series.x
        self.raw_data[Datatype.FAULT]["centroid_y"] = centroid_series.y
        self.raw_data[Datatype.FAULT]["X"] = self.raw_data[Datatype.FAULT]["centroid_x"]
        self.raw_data[Datatype.FAULT]["Y"] = self.raw_data[Datatype.FAULT]["centroid_y"]
        self.raw_data[Datatype.FAULT]["Z"] = 0.0

    def convert_structure_map(self):
        """
        Convert structure dip estimates and derive strike and coordinates using config columns.
        """
        structure_config = self._config["structure"]
        dip_column = structure_config["dip_column"]
        dipdir_column = structure_config["dipdir_column"]
        dipestimate_column = structure_config.get("dipestimate_column", "DipEst")
        dip_null_value = structure_config.get("dip_null_value", -99)

        condition = (self.raw_data[Datatype.STRUCTURE][dip_column] == dip_null_value) & (
            self.raw_data[Datatype.STRUCTURE][dipestimate_column] != "NaN"
        )

        self.raw_data[Datatype.STRUCTURE].loc[condition, dip_column] = (
            self.raw_data[Datatype.STRUCTURE]
            .loc[condition, dipestimate_column]
            .apply(lambda x: convert_dip_terms(x, type="structure"))
        )

        condition = (self.raw_data[Datatype.STRUCTURE][dip_column] == dip_null_value) & (
            self.raw_data[Datatype.STRUCTURE][dipestimate_column] == "NaN"
        )
        self.raw_data[Datatype.STRUCTURE] = self.raw_data[Datatype.STRUCTURE][~condition]

        strike_column = structure_config.get("strike_column", "Strike")
        x_column = structure_config.get("x_column", "X")
        y_column = structure_config.get("y_column", "Y")
        z_column = structure_config.get("z_column", "Z")

        self.raw_data[Datatype.STRUCTURE][strike_column] = (
            self.raw_data[Datatype.STRUCTURE][dipdir_column] + 90
        ) % 360
        self.raw_data[Datatype.STRUCTURE][x_column] = self.raw_data[Datatype.STRUCTURE].geometry.x
        self.raw_data[Datatype.STRUCTURE][y_column] = self.raw_data[Datatype.STRUCTURE].geometry.y
        self.raw_data[Datatype.STRUCTURE][z_column] = 0.0

    def fault_map_postprocessing(self):
        """
        Post-process fault data to build a fault orientation layer.
        """
        fault_config = self._config["fault"]
        dipdir_column = fault_config.get("dipdir_column", "DipDir")
        dip_column = fault_config.get("dip_column", "Dip")
        strike_column = fault_config.get("strike_column", "Strike")
        centroid_column = fault_config.get("centroid_column", "centroid")
        x_column = fault_config.get("x_column", "X")
        y_column = fault_config.get("y_column", "Y")
        z_column = fault_config.get("z_column", "Z")
        feature_id_column = fault_config.get("feature_id_column", "MSID")

        valid_faults = self.raw_data[Datatype.FAULT].dropna(
            subset=[
                feature_id_column,
                x_column,
                y_column,
                z_column,
                dipdir_column,
                strike_column,
                dip_column,
                centroid_column,
            ]
        )
        valid_faults = valid_faults.rename(columns={feature_id_column: "featureId"})
        valid_faults["geometry"] = valid_faults[centroid_column]
        self.raw_data[Datatype.FAULT_ORIENTATION] = geopandas.GeoDataFrame(
            valid_faults[
                ["featureId", x_column, y_column, z_column, dipdir_column, dip_column, "geometry"]
            ].copy(),
            crs=self.crs,
        )
        self.raw_data[Datatype.FAULT_ORIENTATION]["featureId"] = self.raw_data[
            Datatype.FAULT_ORIENTATION
        ]["featureId"].apply(lambda x: "".join(filter(str.isdigit, str(x))))
        self.raw_data[Datatype.FAULT] = self.raw_data[Datatype.FAULT].drop(columns=centroid_column)

    def convert(self):
        """
        Convert input data into Map2Loop-compatible data layers.
        """
        if self.raw_data[Datatype.FOLD] is not None:
            self.convert_fold_map()
        if self.raw_data[Datatype.FAULT] is not None:
            self.convert_fault_map()
        if self.raw_data[Datatype.STRUCTURE] is not None:
            self.convert_structure_map()
            self.fault_map_postprocessing()

        self._data = self.raw_data.copy()
