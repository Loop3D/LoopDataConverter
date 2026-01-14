_UNSET = object()


class BaseConfig:
    def __init__(self):
        self.fold_config = {
            "structtype_column": "FoldType",
            "fold_text": "'Anticline','Syncline','Antiform','Synform','Monocline','Monoform','Neutral','Fold axis','Overturned syncline'",
            "description_column": "Desc",
            "synform_text": "FoldType",
            "foldname_column": "FoldName",
            "objectid_column": "OBJECTID",
            "tightness_column": "IntlimbAng",
            "axial_plane_dipdir_column": "AxPlDipDir",
            "axial_plane_dip_column": "AxPlDip",
        }

        self.fault_config = {
            "orientation_type": "dip direction",
            "structtype_column": "FaultType",
            "fault_text": "'Thrust','Reverse','Normal','Shear zone','Strike-slip','Thrust','Unknown'",
            "dip_null_value": "-999",
            "dipdir_flag": "num",
            "dipdir_column": "DipDir",
            "dip_column": "Dip",
            "dipestimate_column": "DipEstimate",
            "dipestimate_text": "'NORTH_EAST','NORTH',<rest of cardinals>,'NOT ACCESSED'",
            "displacement_column": "Displace",
            "displacement_text": "'1m-100m', '100m-1km', '1km-5km', '>5km'",
            "fault_length_column": "FaultLen",
            "fault_length_text": "Small (0-5km),Medium (5-30km),Large (30-100km),Regional (>100km),Unclassified",
            "name_column": "FaultName",
            "objectid_column": "OBJECTID",
        }

        self.geology_config = {
            "unitname_column": "Formation",
            "alt_unitname_column": "Formation",
            "group_column": "Group",
            "supergroup_column": "Supergroup",
            "description_column": "LithDescn1",
            "minage_column": "AgeMin",
            "maxage_column": "AgeMax",
            "rocktype_column": "LithClass",
            "alt_rocktype_column": "RockCat",
            "sill_text": "RockCat",
            "intrusive_text": "RockCat",
            "volcanic_text": "RockCat",
            "objectid_column": "OBJECTID",
            "ignore_lithology_codes": ["cover", "Unknown"],
        }

        self.structure_config = {
            "orientation_type": "dip direction",
            "dipdir_column": "DipDir",
            "dip_column": "Dip",
            "description_column": "FeatDesc",
            "bedding_text": "ObsType",
            "overturned_column": "Desc",
            "overturned_text": "overturned",
            "objectid_column": "OBJECTID",
        }

        self.config_map = {
            "geology": self.geology_config,
            "structure": self.structure_config,
            "fault": self.fault_config,
            "fold": self.fold_config,
        }

    def _apply_updates(self, target, updates, extra):
        for key, value in updates.items():
            if value is not _UNSET:
                target[key] = value
        if extra:
            target.update(extra)

    def update_fold_config(
        self,
        *,
        structtype_column=_UNSET,
        fold_text=_UNSET,
        description_column=_UNSET,
        synform_text=_UNSET,
        foldname_column=_UNSET,
        objectid_column=_UNSET,
        tightness_column=_UNSET,
        axial_plane_dipdir_column=_UNSET,
        axial_plane_dip_column=_UNSET,
        **extra,
    ):
        updates = {
            "structtype_column": structtype_column,
            "fold_text": fold_text,
            "description_column": description_column,
            "synform_text": synform_text,
            "foldname_column": foldname_column,
            "objectid_column": objectid_column,
            "tightness_column": tightness_column,
            "axial_plane_dipdir_column": axial_plane_dipdir_column,
            "axial_plane_dip_column": axial_plane_dip_column,
        }
        self._apply_updates(self.fold_config, updates, extra)

    def update_fault_config(
        self,
        *,
        orientation_type=_UNSET,
        structtype_column=_UNSET,
        fault_text=_UNSET,
        dip_null_value=_UNSET,
        dipdir_flag=_UNSET,
        dipdir_column=_UNSET,
        dip_column=_UNSET,
        dipestimate_column=_UNSET,
        dipestimate_text=_UNSET,
        displacement_column=_UNSET,
        displacement_text=_UNSET,
        fault_length_column=_UNSET,
        fault_length_text=_UNSET,
        name_column=_UNSET,
        objectid_column=_UNSET,
        **extra,
    ):
        updates = {
            "orientation_type": orientation_type,
            "structtype_column": structtype_column,
            "fault_text": fault_text,
            "dip_null_value": dip_null_value,
            "dipdir_flag": dipdir_flag,
            "dipdir_column": dipdir_column,
            "dip_column": dip_column,
            "dipestimate_column": dipestimate_column,
            "dipestimate_text": dipestimate_text,
            "displacement_column": displacement_column,
            "displacement_text": displacement_text,
            "fault_length_column": fault_length_column,
            "fault_length_text": fault_length_text,
            "name_column": name_column,
            "objectid_column": objectid_column,
        }
        self._apply_updates(self.fault_config, updates, extra)

    def update_geology_config(
        self,
        *,
        unitname_column=_UNSET,
        alt_unitname_column=_UNSET,
        group_column=_UNSET,
        supergroup_column=_UNSET,
        description_column=_UNSET,
        minage_column=_UNSET,
        maxage_column=_UNSET,
        rocktype_column=_UNSET,
        alt_rocktype_column=_UNSET,
        sill_text=_UNSET,
        intrusive_text=_UNSET,
        volcanic_text=_UNSET,
        objectid_column=_UNSET,
        ignore_lithology_codes=_UNSET,
        **extra,
    ):
        updates = {
            "unitname_column": unitname_column,
            "alt_unitname_column": alt_unitname_column,
            "group_column": group_column,
            "supergroup_column": supergroup_column,
            "description_column": description_column,
            "minage_column": minage_column,
            "maxage_column": maxage_column,
            "rocktype_column": rocktype_column,
            "alt_rocktype_column": alt_rocktype_column,
            "sill_text": sill_text,
            "intrusive_text": intrusive_text,
            "volcanic_text": volcanic_text,
            "objectid_column": objectid_column,
            "ignore_lithology_codes": ignore_lithology_codes,
        }
        self._apply_updates(self.geology_config, updates, extra)

    def update_structure_config(
        self,
        *,
        orientation_type=_UNSET,
        dipdir_column=_UNSET,
        dip_column=_UNSET,
        description_column=_UNSET,
        bedding_text=_UNSET,
        overturned_column=_UNSET,
        overturned_text=_UNSET,
        objectid_column=_UNSET,
        **extra,
    ):
        updates = {
            "orientation_type": orientation_type,
            "dipdir_column": dipdir_column,
            "dip_column": dip_column,
            "description_column": description_column,
            "bedding_text": bedding_text,
            "overturned_column": overturned_column,
            "overturned_text": overturned_text,
            "objectid_column": objectid_column,
        }
        self._apply_updates(self.structure_config, updates, extra)

    def __getitem__(self, datatype):
        return self.config_map[datatype]

    def update(self, geology_dict, structure_dict, fault_dict, fold_dict):
        self.update_geology_config(**geology_dict)
        self.update_structure_config(**structure_dict)
        self.update_fault_config(**fault_dict)
        self.update_fold_config(**fold_dict)
