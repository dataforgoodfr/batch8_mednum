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
        super(MedNumApp, self).__init__(**params)  # self.load_data()

        # self.param.interfaces_num.objects = OPTIONS_INT_NUM
        # self.param.infos_num.objects = OPTIONS_X_INFOS

        # self.param.comp_admin.objects = OPTIONS_X_COMP_ADMIN
        # self.param.comp_usage_num.objects = OPTIONS_X_COMP_USAGE

    #     self.top_panel = TopIndicators()

    # @pn.depends("localisation", "score", watch=True)  # .value_throttled"
    # def update_params(self):
    #     d = dict(self.get_param_values())
    #     d.pop("name")
    #     for k, v in d.items():
    #         try:
    #             self.top_panel.set_param(**{k: v})
    #         except Exception as e:
    #             pass

    # def set_params(self):
    #     self.top_params = {
    #         "score": self.score,
    #         "localisation": self.localisation,
    #     }

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
        # spec_interfaces = {k: TreeViewCheckBox for k, v in TREEVIEW_CHECK_BOX.items()}

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
        # self.set_params()
        return ordered_panel

    @pn.depends("score", watch=True)
    def update_map_values(self):

        try:
            # Selection par localisation

            association = {}
            indexes = self.df_merged.loc[self.level_0_value].index
            for k, v in zip(
                indexes.names,
                indexes.unique()[0],
            ):
                association[k] = v

            df_merged_by = self.df_merged.droplevel("variable", axis=1)
            df_merged_by = df_merged_by.xs(
                association[self.level_1_column], level=self.level_1_column,  drop_level=False
            )

            df_merged_by = df_merged_by.dissolve(
                by=[
                    MAP_COL_WIDGETS["level_1"][self.niveau_details],
                    self.level_0_column,
                ],
                aggfunc="mean",
            )

            vdims_by = [
                c[0] if isinstance(c, tuple) else c for c in df_merged_by.columns
            ]
            df_merged_by.columns = vdims_by
            vdims_by = [c for c in vdims_by if c != "geometry"]
            import random

            random.shuffle(vdims_by)
            self.maps = gv.Polygons(df_merged_by, vdims=vdims_by + ["nom_com"])
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

    @pn.depends("localisation", watch=True)
    def update_map_coords(self):
        if not hasattr(self, "maps"):
            self.update_map_values()
        minx, miny, maxx, maxy = self.maps.geom().bounds
        self.tiles.redim.range(
            Latitude=(miny, maxy), Longitude=(minx, maxx),
        )
        return self.tiles

    def map_view(self):
        # return gv.DynamicMap(self.update_map_coords) * gv.DynamicMap(
        return self.tiles * gv.DynamicMap(self.update_map_values)

    @pn.depends("tout_axes", watch=True)
    def selection_indicateurs(self):
        for par in self.g_params:
            indic_name = next(iter(par.widgets))
            if "tout_axes" != indic_name:
                widg = par.widgets[indic_name].get("type", None)
                widg.param.select_all = self.tout_axes

    def table_view(self):
        return pn.pane.DataFrame(
            self.df_merged[self.selected_indices_level_0].droplevel("variable", axis=1),
            max_rows=20,
        )  # self.score_calculation

