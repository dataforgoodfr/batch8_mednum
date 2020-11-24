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

    @pn.depends("localisation", "score", "score_widget.value_throttled", watch=True)
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
                "score": {"type": pn.widgets.IntRangeSlider, "bar_color": "#000000"},
            },
        )
        self.score_widget = self.score_controls[0]

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
        g_params = []
        for k, widget_opts in TREEVIEW_CHECK_BOX.items():
            # widget_opts = TREEVIEW_CHECK_BOX[k]
            # widget_opts["type"] = TreeViewCheckBox

            # select_options = [opt for opt in widget_opts.keys() if opt not in ["nom", "desc"]]

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
            g_params.append(
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

        # g_params = [
        #     pn.Param(self.param[p], widgets={p: w}) for p, w in spec_interfaces.items()
        # ]

        indicateurs = pn.Column("# Indicateurs", *g_params)

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

    # @pn.depends("localisation", "score_widget.value_throttled")
    def plot(self):

        commune_plot = self.iris_map.select(
            nom_com=self.localisation, vdims=self.map_vdims
        )

        # indices_list = list(self.ifrag_cont_df_merged)
        # indices_list.remove("geometry")
        # self.map_vdims = ["code_iris", "nom_com", "nom_iris"] + indices_list
        # self.iris_map = gv.Polygons(self.ifrag_cont_df_merged, vdims=self.map_vdims)

        vdims = self.map_vdims

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

    def view(self) -> pn.viewable.Viewable:
        self.update_params()
        # self._update_plots()
        return pn.Row(
            self.lat_widgets(),
            pn.layout.HSpacer(width=10),
            pn.Column(self.top_panel.view(), pn.Spacer(height=80), pn.Spacer()),
        )

    def panel(self):
        return pn.Row(self.lat_widgets(), self.view,)
