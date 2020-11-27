
import panel as pn
import geoviews as gv
from mednum.config import *
from mednum.controlers.overallparameters import OverallParameters
from mednum.indicators.panels import TopIndicators
from mednum.widgets import TreeViewCheckBox
import param


class MedNumApp(OverallParameters):
    score_widget = pn.widgets.IntRangeSlider
    _layout = pn.Column()
    top_params = param.Dict(default={})

    def __init__(self, **params):
        super().__init__(**params)
        self.load_data()

        # self.param.interfaces_num.objects = OPTIONS_INT_NUM
        # self.param.infos_num.objects = OPTIONS_X_INFOS

        # self.param.comp_admin.objects = OPTIONS_X_COMP_ADMIN
        # self.param.comp_usage_num.objects = OPTIONS_X_COMP_USAGE

        self.top_panel = TopIndicators()

    @pn.depends("localisation", "score", watch=True) # .value_throttled"
    def update_params(self):
        d = dict(self.get_param_values())
        d.pop("name")
        for k, v in d.items():
            try:
                self.top_panel.set_param(**{k: v})
            except Exception as e:
                pass

    def set_params(self):
        self.top_params = {
            "score": self.score,
            "localisation": self.localisation,
        }

    def lat_widgets(self):
        self.score_controls = pn.Param(
            self.param.score,
            widgets={
                "score": {
                    "type": pn.widgets.IntRangeSlider,
                     "bar_color": "#000000",
                     "throttled": True
                },
            },
        )
        # self.score_widget = self.score_controls[0]

        score_panel = pn.Column("# Score", self.score_controls)
        point_ref_panel = pn.Column(
            "# Point de reference",
            pn.Param(
                self.param.point_ref, widgets={"point_ref": pn.widgets.RadioBoxGroup,},
            ),
        )
        export_panel = pn.Column(
            "# Aller plus loin", self.param.export_data, self.param.edit_report
        )

        localisation_panel = pn.Column("# Localisation", self.param.localisation)
        spec_interfaces = {k: TreeViewCheckBox for k, v in TREEVIEW_CHECK_BOX.items()}
        self.g_params = []
        for k, widget_opts in TREEVIEW_CHECK_BOX.items():
            # Voir si description ne peut être passée
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
            self.g_params.append(
                pn.Param(
                    self.param[k],
                    widgets={
                        k: {
                            "type": TreeViewCheckBox,
                            "select_options": select_options,
                            "select_all": widget_opts["nom"],
                            "desc": descriptions,
                        }
                    },
                )
            )

        indicateurs = pn.Column("# Indicateurs", *self.g_params)

        ordered_panel = pn.Column(
            localisation_panel,
            score_panel,
            indicateurs,
            point_ref_panel,
            export_panel,
            width=400,
        )
        self.set_params()
        return ordered_panel

    @pn.depends("score", watch=True)
    def update_map_values(self):
        vdims = self.map_vdims[:2]

        maps = self.iris_map.select(nom_com=self.localisation, vdims=vdims)

        minx, miny, maxx, maxy = maps.geom().bounds
        df_filtered = self.ifrag_cont_df_merged
        df_filtered = df_filtered[df_filtered.nom_com == self.localisation]

        self.maps = maps.select(name=self.localisation)


        return self.maps.opts(
            tools=["hover"],
            color=vdims[0],
            colorbar=True,
            toolbar="above",
            xaxis=None,
            yaxis=None,
            fill_alpha=0.5,
        )

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
        return gv.DynamicMap(self.update_map_coords) * gv.DynamicMap(
            self.update_map_values
        )
