#!/usr/bin/env python
# coding: utf-8
import os
from pathlib import Path

import geoviews as gv
import panel as pn
import param
from holoviews import opts
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
    score = param.Range(
        default=(0, 250),
        bounds=(0, 250),
    )
    interfaces_num = param.ListSelector(label="")
    infos_num = param.ListSelector(label="")

    comp_admin = param.ListSelector(label="")
    comp_usage_num = param.ListSelector(label="")

    point_ref = param.Selector(
        objects=["Pays", "Région", "Département", "Intercommune", "Commune"],
        label="Point de référence",
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

    def load_data(self):

        # cwd = Path(os.getcwd())
        data_path = Path("../data")

        if not data_path.exists():
            data_path = Path("./data")
        
        raw_data = data_path / "raw/"
        
        external_data = data_path / "external/"

        interim_data = data_path / "interim/"

        cont_iris = external_data / "france-geojson" / "contours-iris.geojson"

        cont_iris = external_data / "france-geojson" / "contours-iris.geojson"

        indice_frag = raw_data / "Tableau_data.csv"

        # Merged
        output_data_path = interim_data / "get_merged_iris_data.trc.pqt"
        if output_data_path.exists():
            import geopandas as gpd

            self.ifrag_cont_df_merged = gpd.read_parquet(output_data_path)
        else:
            self.ifrag_cont_df_merged = get_merged_iris_data(
                iris_df(cont_iris),
                get_indice_frag_pivot(get_indice_frag(indice_frag)),
            )

        indices_list = list(self.ifrag_cont_df_merged)
        indices_list.remove("geometry")
        self.map_vdims = ["code_iris", "nom_com", "nom_iris"] + indices_list

        # Cartes
        self.iris_map = gv.Polygons(self.ifrag_cont_df_merged, vdims=self.map_vdims)




#if __name__ == "__main__":
