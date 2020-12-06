import panel as pn
import geoviews as gv
from mednum.config import *
from mednum.controlers.overallparameters import OverallParameters
from mednum.indicators.panels import TopIndicators
import param


class MedNumApp(TopIndicators):
    score_widget = pn.widgets.IntRangeSlider
    _layout = pn.Column()
    top_params = param.Dict(default={})

    def __init__(self, **params):
        super(MedNumApp, self).__init__(**params)

    def lat_widgets(self):
        self.score_controls = pn.Param(
            self.param.score,
            widgets={
                "score": {
                    "type": pn.widgets.IntRangeSlider,
                    "bar_color": "#000000",
                    "throttled": True,
                },
            },
        )

        score_panel = pn.Column("## Score", self.score_controls)
        point_ref_panel = pn.Column(
            "## Point de reference",
            pn.Param(
                self.param.point_ref, widgets={"point_ref": pn.widgets.RadioBoxGroup},
            ),
        )
        niveau_observation_panel = pn.Column(
            "## " + self.param.niveau_observation.label,
            pn.Param(
                self.param.niveau_observation,
                widgets={"niveau_observation": pn.widgets.RadioBoxGroup},
            ),
        )
        niveau_details_panel = pn.Column(
            "## " + self.param.niveau_details.label,
            pn.Param(
                self.param.niveau_details,
                widgets={"niveau_details": pn.widgets.RadioBoxGroup},
            ),
        )

        export_panel = pn.Column(
            "## Aller plus loin", self.param.export_data, self.param.edit_report
        )

        localisation_panel = pn.Column("## Localisation", self.param.localisation)

        indicateurs = pn.Column("## Indicateurs", *self.g_params)

        ordered_panel = pn.Column(
            localisation_panel,
            score_panel,
            indicateurs,
            point_ref_panel,
            niveau_observation_panel,
            niveau_details_panel,
            export_panel,
        )
        return ordered_panel

    # @pn.depends(
    #     "score",
    #     "df_score",
    #     watch=True,
    # )
    def update_map_values(self):
        try:
            # Selection par localisation
            # http://holoviews.org/user_guide/Plotting_with_Bokeh.html
            # https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#custom-tooltip
            map_info = ["tout_axes", "nom_com"]
            vdims = (
                map_info
                + [k + "_SCORE" for k in self.selected_indices_level_0]
                + list(AXES_INDICES.keys())
            )
            self.maps = gv.Polygons(self.df_score, vdims=vdims)
            return self.maps.opts(
                tools=["hover"],
                color="score",
                colorbar=True,
                toolbar="above",
                xaxis=None,
                yaxis=None,
                fill_alpha=0.5,
            )

        except Exception as e:
            print(e)
            pass

    # @pn.depends("localisation", watch=True)
    # def update_map_coords(self):
    #     if not hasattr(self, "maps"):
    #         self.update_map_values()
    #     minx, miny, maxx, maxy = self.maps.geom().bounds
    #     self.tiles.redim.range(
    #         Latitude=(miny, maxy), Longitude=(minx, maxx),
    #     )
    #     return self.tiles

    def map_view(self):
        # return gv.DynamicMap(self.update_map_coords) * gv.DynamicMap(self.update_map_values)
        return self.tiles * gv.DynamicMap(self.update_map_values)

    @pn.depends("tout_axes", watch=True)
    def selection_indicateurs(self):
        for par in self.g_params:
            indic_name = next(iter(par.widgets))
            if "tout_axes" != indic_name:
                widg = par.widgets[indic_name].get("type", None)
                widg.param.select_all = self.tout_axes

    def table_view(self):
        return pn.Row(
            pn.pane.DataFrame(
                self.df_merged[self.selected_indices_level_0].droplevel(
                    "variable", axis=1
                ),
                max_rows=20,
            )
        ) 

