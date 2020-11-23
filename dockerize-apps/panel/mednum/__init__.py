# from .widgets import *
# from .tools import *
# from .loaders import *
# from .indicators import *
# from .controlers import *
# from . import controlers # noqa
# from . import indicators # noqa
# # from . import tools # noqa
# from . import loaders
# from . import config # noqa

import panel as pn
import geoviews as gv
from mednum.config import *
from mednum.controlers.overallparameters import OverallParameters
from mednum.indicators.panels import TopIndicators
from mednum.widgets import TreeViewCheckBox


class MedNumApp(OverallParameters):
    score_widget = pn.widgets.IntRangeSlider
    _layout = pn.Column()

    def __init__(self, **params):
        super().__init__(**params)
        self.load_data()

        self.param.interfaces_num.objects = OPTIONS_INT_NUM
        self.param.infos_num.objects = OPTIONS_X_INFOS

        self.param.comp_admin.objects = OPTIONS_X_COMP_ADMIN
        self.param.comp_usage_num.objects = OPTIONS_X_COMP_USAGE

        # indic_w_g_value_1 = {
        #     "name": "indic1_1",
        #     "indicators": [
        #         dict(name="accès", main=True, value=85, max_value=100),
        #         dict(name="information", value=118),
        #         dict(name="Interfaces", value=53),
        #     ],
        # }

        # indic_w_g_value_2 = {
        #     "indicators": [
        #         dict(name="Compétences", main=True, value=135, max_value=180),
        #         dict(name="indic3_2", value=115),
        #         dict(name="indic4", value=155),
        #     ]
        # }

        self.top_panel = TopIndicators()
        # self._layout = pn.Row(
        #     self.lat_widgets(),
        #     pn.layout.HSpacer(width=10),
        #     pn.Column(
        #         self.top_panel.view(),
        #         pn.Spacer(height=80),
        #         pn.Spacer()
        #     ),
        # )

    def update_params(self):
        d = dict(self.get_param_values())
        d.pop("name")
        for k, v in d.items():
            try:
                self.top_panel.set_param(**{k: v})
            except Exception as e:
                pass

    def lat_widgets(self):
        self.score_controls = pn.Param(
            self.param.score,
            widgets={
                "score": {"type": pn.widgets.IntRangeSlider, "bar_color": "#000000"},
            },
        )
        self.score_widget = self.score_controls[0]

        score_panel = pn.Column("# Score", self.score_controls)
        point_ref_panel = pn.Column(
            "# Point de reference",
            pn.Param(
                self.param.point_ref,
                widgets={
                    "point_ref": pn.widgets.RadioBoxGroup,
                },
            ),
        )
        export_panel = pn.Column(
            "# Aller plus loin", self.param.export_data, self.param.edit_report
        )

        localisation_panel = pn.Column("# Localisation", self.param.localisation)
        spec_interfaces = {k: TreeViewCheckBox for k,v in TREEVIEW_CHECK_BOX.items()
            # "interfaces_num": TreeViewCheckBox(tree_categories=),
            # "infos_num": TreeViewCheckBox,
            # "comp_admin": TreeViewCheckBox,
            # "comp_usage_num": TreeViewCheckBox,
        }
        
        g_params = [
            pn.Param(self.param[p], widgets={p: w}) for p, w in spec_interfaces.items()
        ]

        indicateurs = pn.Column("# Indicateurs", *g_params)

        ordered_panel = pn.Column(
            localisation_panel,
            score_panel,
            indicateurs,
            point_ref_panel,
            export_panel,
            width=400,
        )

        return ordered_panel

    # @pn.depends("localisation", "score_widget.value_throttled")
    def plot(self):

        commune_plot = self.iris_map.select(
            nom_com=self.localisation, vdims=self.map_vdims
        )


        # indices_list = list(self.ifrag_cont_df_merged)
        # indices_list.remove("geometry")
        # self.map_vdims = ["code_iris", "nom_com", "nom_iris"] + indices_list
        # self.iris_map = gv.Polygons(self.ifrag_cont_df_merged, vdims=self.map_vdims)

        vdims=self.map_vdims

        # commune_plot = self.iris_map.select(
        #     nom_com=self.localisation, vdims=self.map_vdims
        # )

        # minx, miny, maxx, maxy = commune_plot.geom().bounds
        # df_filtered = self.ifrag_cont_df_merged
        # df_filtered = df_filtered[df_filtered.nom_com == self.localisation]

        # # minx, miny, maxx, maxy = df_filtered.dissolve(by='nom_com').geometry.bounds.values[0]


        # commune_plot = gv.Polygons(df_filtered, vdims=vdims)
        # .redim.range(
        #     Latitude=(miny, maxy),
        #     Longitude=(minx, maxx),
        # )
        
        # self.iris_map.select(
        #     nom_com=self.localisation, vdims=self.map_vdims
        # )
        # Cartes
        return commune_plot.opts(color=INDICE, fill_alpha=0.5)

    def _update_plots(self):
        import datetime
        self._layout[-1][0] = self.top_panel.view()
        # self._layout[-1][-1] = self.plot()

    #@pn.depends("localisation", "score_widget.value_throttled")
    def view(self) -> pn.viewable.Viewable:
        self.update_params()
        # self._update_plots()
        return pn.Row(
            self.lat_widgets(),
            pn.layout.HSpacer(width=10),
            pn.Column(
                self.top_panel.view(),
                pn.Spacer(height=80),
                pn.Spacer()
            ),
        )

    def panel(self):
        return pn.Row(
            self.lat_widgets(),
            self.view,
        )
