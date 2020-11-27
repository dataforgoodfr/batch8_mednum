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
        objects=list(MAP_COL_WIDGETS["point_ref"].keys()), label="Point de référence",
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

    df_merge = param.DataFrame()
    # indices_list = param.ListSelector(label="")
    filtered_list = param.ListSelector(label="")
    df_filtered = param.DataFrame()

    def __init__(self, **params):
        super(OverallParameters, self).__init__(**params)
        interim_data, cont_iris, indice_frag = self.define_paths()

        self.define_indices_params()

        # Merged
        output_data_path = interim_data / "get_merged_iris_data.trc.pqt"
        if output_data_path.exists():
            import geopandas as gpd

            self.df_merge = gpd.read_parquet(output_data_path)
        else:
            self.df_merge = get_merged_iris_data(
                iris_df(cont_iris), get_indice_frag_pivot(get_indice_frag(indice_frag)),
            )

        self.indices_list = list(self.df_merge)
        self.indices_list.remove("geometry")
        self.map_vdims = ["code_iris", "nom_com", "nom_iris"] + self.indices_list

        # Cartes
        self.iris_map = gv.Polygons(self.df_merge, vdims=self.map_vdims)

    def define_paths(self):
        data_path = Path("../data")

        if not data_path.exists():
            data_path = Path("./data")

        raw_data = data_path / "raw/"

        external_data = data_path / "external/"

        interim_data = data_path / "interim/"

        cont_iris = external_data / "france-geojson" / "contours-iris.geojson"

        indice_frag = raw_data / "Tableau_data.csv"
        return interim_data, cont_iris, indice_frag

    def define_indices_params(self):
        self.g_params = []
        for k, widget_opts in TREEVIEW_CHECK_BOX.items():
            # Voir si description ne peut être passée
            widgets_params = self.create_checkbox_type_widget_params(widget_opts)

            self.g_params.append(pn.Param(self.param[k], widgets={k: widgets_params}))

    def get_params(self):
        paramater_names = [par[0] for par in self.get_param_values()]
        return pn.Param(
            self.param, parameters=[par for par in paramater_names if par != "df_merge"]
        )

    def filtered_parameters(self, with_geom=False):
        # self.filtered_list = self.indices_list.copy()
        # self.filtered_view_list = self.indices_list.copy()
        param_values = {k: v for k, v in self.param.get_param_values()}

        ref_column = MAP_COL_WIDGETS["point_ref"][param_values["point_ref"]]
        selected_col = [ref_column]
        for axe, indices in param_values.items():
            # try:
            if (
                axe in TREEVIEW_CHECK_BOX.keys() and indices
            ):  # isinstance(indices, list):
                for indice in indices:
                    try:
                        selected_col += [CATEGORIES_INDICES_REV[indice]]
                    except:
                        pass
            # except:
            #     pass

        self.filtered_list = list(set(selected_col))

        if with_geom:
            return self.filtered_list + [
                "geometry"
            ]  # elf.df_merge[self.indices_list + ["geometry"]]
        else:
            return self.filtered_list  # self.df_merge[self.indices_list]

    def filter_data(self):
        # return pn.pane.DataFrame(
        return self.filtered_parameters()
        #     max_rows=20,
        #     max_cols=5,
        #     col_space="100px",
        #     show_dimensions=True,
        # )  # .select(age=self.age)

    def create_checkbox_type_widget_params(self, widget_opts):
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
