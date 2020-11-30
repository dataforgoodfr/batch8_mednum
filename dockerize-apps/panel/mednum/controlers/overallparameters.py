#!/usr/bin/env python
# coding: utf-8
import os
from pathlib import Path

import geoviews as gv
import panel as pn
import param
from holoviews import opts
from panel.widgets import Checkbox
from mednum.widgets import TreeViewCheckBox
from holoviews.element.tiles import StamenTerrain
from mednum.loaders import *
from pygal.style import Style
from mednum import tools
from mednum.config import *

import mednum as mind


gv.extension("bokeh")

opts.defaults(
    opts.Polygons(
        width=800,
        height=600,
        toolbar="above",
        colorbar=True,
        tools=["hover", "tap"],
        aspect="equal",
    )
)


class OverallParameters(param.Parameterized):
    localisation = param.String(default="Toulouse", label="")
    score = param.Range(default=(0, 250), bounds=(0, 250),)

    tout_axes = param.Boolean(False, label="")
    interfaces_num = param.ListSelector(label="")
    infos_num = param.ListSelector(label="")
    comp_admin = param.ListSelector(label="")
    comp_usage_num = param.ListSelector(label="")

    point_ref = param.Selector(
        objects=list(MAP_COL_WIDGETS["level_1"].keys()), label="Point de référence",
    )

    donnees_infra = param.Action(
        lambda x: x, doc="""Données Infra-Communales""", precedence=0.7
    )
    export_data = param.Action(
        lambda x: x.timestamps.append(dt.datetime.utcnow()),
        doc="""Exporter les résultats""",
        precedence=0.7,
    )
    edit_report = param.Action(
        lambda x: x.timestamps.append(dt.datetime.utcnow()),
        doc="""Editer un rapport""",
        precedence=0.7,
    )
    tiles = gv.tile_sources.StamenTerrain

    df_merged = param.DataFrame()
    # indices_list = param.ListSelector(label="")
    # filtered_list = param.ListSelector(label="")
    # df_filtered = param.DataFrame()

    def __init__(self, **params):
        super(OverallParameters, self).__init__(**params)
        interim_data, cont_iris, indice_frag = self.define_paths()

        # Merged
        output_data_path = interim_data / "add_geom_data_to_merged_data.trc.pqt"
        if output_data_path.exists():
            import geopandas as gpd

            self.df_merged = gpd.read_parquet(output_data_path)
        else:
            # self.df_merged = get_merged_iris_data(
            #     iris_df(cont_iris), get_indice_frag_pivot(get_indice_frag(indice_frag)),
            # )
            self.df_merged = add_geom_data_to_merged_data(
                iris_df(cont_iris), read_merged_data(indice_frag)
            )

        # Create multindex
        self.set_dataframes_indexes()
        self.set_dataframes_level()

        # Create widgets for indicators
        self.define_indices_params()

        # Define what is level 0 and level 1 to consider
        self.set_entity_levels()

        # What is selected in each level
        self.get_selected_indice_by_level()

        # self.indices_list = list(self.df_merged)
        # self.indices_list.remove("geometry")
        # self.map_vdims = ["code_iris", "nom_com", "nom_iris"] + self.indices_list

        # Cartes
        # self.iris_map = gv.Polygons(self.df_merged) #, vdims=self.map_vdims)

    def define_paths(self):
        data_path = Path("../data")

        if not data_path.exists():
            data_path = Path("./data")

        raw_data = data_path / "raw/"

        external_data = data_path / "external/"

        interim_data = data_path / "interim/"

        cont_iris = external_data / "france-geojson" / "contours-iris.geojson"

        indice_frag = processed_data / "MERGE_data_clean.csv"
        return interim_data, cont_iris, indice_frag

    def define_indices_params(self):
        """ 
        Create all indices parameters -> Will become a TreeCheckBox
        """
        self.g_params = []
        for k, widget_opts in TREEVIEW_CHECK_BOX.items():
            # Voir si description ne peut être passée
            widgets_params = self.create_checkbox_type_widget_params(widget_opts)

            self.g_params.append(pn.Param(self.param[k], widgets={k: widgets_params}))

    def get_params(self):
        paramater_names = [par[0] for par in self.get_param_values()]
        return pn.Param(
            self.param,
            parameters=[par for par in paramater_names if par != "df_merged"],
        )

    def set_dataframes_level(self):
        real_name_level = []
        for col in self.df_merged.columns:
            if col in CATEGORIES_INDICES.keys():
                real_name_level.append((col, CATEGORIES_INDICES[col]))
            else:
                real_name_level.append((col, col))

        self.df_merged.columns = pd.MultiIndex.from_tuples(
            real_name_level, names=["variable", "nom"]
        )

    def set_dataframes_indexes(self):
        indexes = [MAP_COL_WIDGETS["level_0"]] + list(
            MAP_COL_WIDGETS["level_1"].values()
        )
        self.df_merged.set_index(indexes, inplace=True)

    @pn.depends("localisation", "point_ref", watch=True)
    def set_entity_levels(self):
        """Set the entity levels and point values for this entity .
        """
        self.level_0_column, self.level_1_column = (
            MAP_COL_WIDGETS["level_0"],
            MAP_COL_WIDGETS["level_1"][self.point_ref],
        )
        self.level_0_value = self.localisation
        # self.level_1_value = self.point_ref

        # if self.level_1_column != "":
        # self.level_1_values = self.df_merged.loc[
        #     self.df_merged[self.level_0_column] == self.level_0_value,
        #     self.level_1_column,
        # ]
        # print('ok')
        # else:
        #     self.level_1_values = None

    @pn.depends(
        "tout_axes",
        "interfaces_num",
        "infos_num",
        "comp_admin",
        "comp_usage_num",
        watch=True,
    )
    def get_selected_indice_by_level(self):
        """get the indices of the selected column

        Args:
            self ([type]): [description]

        Returns:
            [type]: [description]
        """
        param_values = {k: v for k, v in self.param.get_param_values()}
        selected_col = []
        for axe, indices in param_values.items():
            if axe in TREEVIEW_CHECK_BOX.keys() and indices:
                for indice in indices:
                    try:
                        selected_col += [CATEGORIES_INDICES_REV[indice]]
                    except:
                        pass

        self.selected_indices_level_0 = list(
            set(selected_col)
        )  #  + [self.level_0_column]))
        self.selected_indices_level_1 = list(
            set(selected_col)
        )  # + [self.level_1_column]))

        # if with_geom:
        #     return self.filtered_list + [
        #         "geometry"
        #     ]  # elf.df_merged[self.indices_list + ["geometry"]]
        # else:
        return self.selected_indices_level_0, self.selected_indices_level_1

    def create_checkbox_type_widget_params(self, widget_opts):
        """Create dict of widget type and checkbox params .

        Args:
            widget_opts ([type]): [description]

        Returns:
            [type]: [description]
        """
        if len(widget_opts.items()) > 3:
            select_options = [
                val["nom"]
                for opt, val in widget_opts.items()
                if opt not in ["nom", "desc"]
            ]
            descriptions = [
                val["desc"]
                for opt, val in widget_opts.items()
                if opt not in ["nom", "desc"]
            ]
            widget_type = TreeViewCheckBox
            widgets_params = {
                "type": widget_type,
                "select_options": select_options,
                "select_all": widget_opts["nom"],
                "desc": descriptions,
            }
        else:
            descriptions = widget_opts["desc"]
            widget_type = Checkbox
            widgets_params = {
                "name": widget_opts["nom"],
                "type": widget_type,
                "value": True,
                "desc": descriptions,
            }
        return widgets_params

    def set_real_name(df):
        real_name_level = []
        for col in df.columns:
            if col in CATEGORIES_INDICES.keys():
                real_name_level.append((col, CATEGORIES_INDICES[col]))
            else:
                real_name_level.append((col, col))

        return real_name_level

    @pn.depends("localisation", "point_ref", watch=True)
    def score_calculation(self):
        df = self.df_merged.copy().droplevel("nom", axis=1)

        selected = []
        real_name_level = []
        for kAxe, vAxe in TREEVIEW_CHECK_BOX.items():
            n = 0
            for kIndic, vIndic in vAxe.items():
                # Exclusion du cas complet
                if kIndic not in ["nom", "desc"]:
                    # exclusion de nom et desc donne le nombre d'indice
                    real_name_level.append((kAxe, kIndic))
                    selected.append(kIndic)

        mean_by_level_1 = df[selected].groupby(level=self.level_1_column).mean()
        self.df_score = (
            df[selected].sub(mean_by_level_1).div(mean_by_level_1) * 100 + 100
        )

        self.df_score.columns = pd.MultiIndex.from_tuples(
            real_name_level, names=["axe", "indicateur"]
        )

