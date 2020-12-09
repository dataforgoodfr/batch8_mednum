import geoviews as gv
import panel as pn
from geoviews import opts
from cartopy import crs as ccrs
import param
from holoviews import opts
import holoviews as hv
import geopandas as gpd
import geoviews as gv
import numpy as np
import cartopy.crs as ccrs
from mednum import tools
from mednum.config import *
from mednum.loaders import *
from pathlib import Path
from bokeh.models import HoverTool

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


def define_paths():
    data_path = Path("../data")

    if not data_path.exists():
        data_path = Path("./data")

    raw_data = data_path / "raw/"

    external_data = data_path / "external/"

    interim_data = data_path / "interim/"

    cont_iris = external_data / "france-geojson" / "contours-iris.geojson"

    indice_frag = processed_data / "MERGE_data_clean.csv"
    return interim_data, cont_iris, indice_frag


interim_data, cont_iris, indice_frag = define_paths()
polygons = iris_df(cont_iris)
polygons = polygons[polygons.nom_com.isin(["Toulouse", "Lille"])]


# vdims = ['nom_com']
# maps = gv.Polygons(df_merged, vdims=vdims)


class Example(param.Parameterized):
    localisation = param.ObjectSelector(
        default="Toulouse", objects=["Toulouse", "Lille"]
    )
    some_value = param.Integer(bounds=(0, 100))
    tiles = gv.tile_sources.StamenTerrain()

    @pn.depends("some_value", "localisation")
    def update_poly(self):
        poly = polygons.copy()
        poly = poly[poly.nom_com == self.localisation]

        poly.loc[:, "value"] = np.random.rand(len(poly)) * self.some_value
        vdims = ["value", "value2"]

        poly.loc[:, "value2"] = np.random.rand(len(poly)) * self.some_value

        # Hovertool
        # https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#hovertool

        # gv.Polygons(d1, vdims=[('pop_est','Population'), ('name', 'Country')]).options(
        #     tools=['hover'], width=800, height=500, projection=crs.Robinson()
        # )

        tooltips = [("value", "@value"), ("value2", "-")]

        if self.some_value > 50:
            tooltips = [("value", "@value"), ("value2", "@value2")]

        TOOLTIPS_HTML = """
        <div>
        """
        for val in ["value", "value2"]:
            TOOLTIPS_HTML += """<div>
                <span style="font-size: 17px; font-weight: bold;">{parameter} :</span> <span style="red"> @{parameter}</span>
            </div>""".format(
                parameter=val
            )

        TOOLTIPS_HTML += """
        </div>
        """

        hover_custom = HoverTool(tooltips=TOOLTIPS_HTML)

        maps = gv.Polygons(poly, vdims=vdims).opts(
            # tools=[hover_custom],
            tools=[hover_custom],
            color="value",
            colorbar=True,
            toolbar="above",
            fill_alpha=0.5,
            width=800,
            height=800,
        )
        return maps

    @pn.depends("localisation")
    def update_tiles(self):
        return self.tiles * gv.DynamicMap(self.update_poly)


example = Example()
print(type(example.update_tiles()))
pn.Row(example, example.update_tiles).servable()

