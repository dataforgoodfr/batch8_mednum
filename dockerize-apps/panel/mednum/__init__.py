import panel as pn
import geoviews as gv
from mednum.config import *
from mednum.controlers.overallparameters import OverallParameters
from mednum.indicators.panels import TopIndicators
import param
from cartopy import crs
from bokeh.models import HoverTool
import re
from holoviews import opts
import cProfile

opts.defaults(
    opts.Polygons(
        width=900,
        height=900,
        toolbar="above",
        colorbar=True,
        tools=["hover", "tap"],
        aspect="equal",
    )
)


class MedNumApp(TopIndicators):
    score_widget = pn.widgets.IntRangeSlider
    _layout = pn.Column()
    top_params = param.Dict(default={})

    def __init__(self, **params):
        super(MedNumApp, self).__init__(**params)
        self.catch_request()

    def catch_request(self):
        try:
            self.localisation = str(
                pn.state.session_args.get("localisation")[0].decode()
            )
        except Exception as e:
            self.localisation = "Auch"

        try:
            self.level_1_column = str(
                pn.state.session_args.get("level_1_column")[0].decode()
            )
        except Exception:
            self.level_1_column = "EPCI"

        try:
            self.level_0_column = str(
                pn.state.session_args.get("level_0_column")[0].decode()
            )
        except Exception:
            self.level_0_column = "insee_com"
            pass

        try:
            self.level_0_column_names = str(
                pn.state.session_args.get("level_0_column_names")[0].decode()
            )
        except Exception:
            self.level_0_column_names = "nom_com"
            pass

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
        # niveau_details_panel = pn.Column(
        #     "## " + self.param.niveau_details.label,
        #     pn.Param(
        #         self.param.niveau_details,
        #         widgets={"niveau_details": pn.widgets.RadioBoxGroup},
        #     ),
        # )

        export_panel = pn.Column(
            """## Aller plus loin""",
            pn.pane.HTML(
                """
         <a href="https://lamednum.coop/actions/indice-de-fragilite-numerique/" title="En savoir plus sur la méthode" class="link2"> &gt; En savoir plus sur la méthode</a>
         """
            )
            # self.param.export_data,  # self.param.edit_report
        )

        localisation_panel = pn.Column(
            "## Localisation",
            pn.Param(
                self.param.localisation,
                widgets={
                    "localisation": {
                        "type": pn.widgets.AutocompleteInput,
                        "options": self.seachable_localisation,
                        "value": self.localisation,
                        "case_sensitive": False,
                    }
                },
            ), css_classes=['blc-search']
        )

        indicateurs = pn.Column("## Indicateurs", *self.g_params)

        ordered_panel = pn.Column(
            localisation_panel,
            score_panel,
            indicateurs,
            point_ref_panel,
            niveau_observation_panel,
            # niveau_details_panel,
            export_panel,
        )
        return ordered_panel

    @pn.depends("score", "localisation", "point_ref", "df_score")  # ,watch=True)
    def update_map_values(self):
        try:
            # Selection par localisation
            #  http://holoviews.org/user_guide/Plotting_with_Bokeh.html
            # https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#custom-tooltip
            map_info = ["tout_axes", "nom_com"]

            vdims = (
                map_info
                + [k + "_SCORE" for k in self.selected_indices_level_0]
                + list(AXES_INDICES.keys())
            )

            TOOLTIPS_HTML = """<span style="font-size: 22px; font-weight: bold;"> @nom_com : @tout_axes</span>
            <div>
            """
            for k, indicators in AXES_INDICES.items():
                display_name = indicators["nom"]
                vdim_name = k
                if vdim_name in vdims:
                    TOOLTIPS_HTML += """<div class="mednum-hover">
                    <span style="font-size: 18px; font-weight: bold;">  {display_name} :</span> <span style=""> @{vdim_name}</span>
                </div>""".format(
                        display_name=display_name, vdim_name=vdim_name
                    )

                else:
                    TOOLTIPS_HTML += """<div class="mednum-hover">
                    <span style="font-size: 18px; font-weight: bold;">  {display_name} :</span> <span style="color:orange"> N/A </span>
                </div>""".format(
                        display_name=display_name, vdim_name=vdim_name
                    )

                for indic in indicators:
                    if indic not in ["desc", "nom"]:
                        display_name = CATEGORIES_INDICES[indic]
                        vdim_name = indic + "_SCORE"
                        if vdim_name in vdims:

                            TOOLTIPS_HTML += """<div class="mednum-hover">
                            <span style="font-size: 12px; ">  {display_name} :</span> <span style="">@{vdim_name}</span>
                            </div>""".format(
                                display_name=display_name, vdim_name=vdim_name
                            )
                        else:
                            TOOLTIPS_HTML += """<div class="mednum-hover">
                            <span style="font-size: 12px;">  {display_name} :</span> <span style="color:orange">N/A</span>
                            </div>""".format(
                                display_name=display_name
                            )

                TOOLTIPS_HTML += """
                </div>
                """

            hover_custom = HoverTool(tooltips=TOOLTIPS_HTML)

            self.maps = gv.Polygons(self.df_score, vdims=vdims)
            return self.maps.opts(
                tools=[hover_custom],
                color="tout_axes",
                colorbar=True,
                toolbar="above",
                xaxis=None,
                yaxis=None,
                fill_alpha=0.5,
            )

        except Exception as e:
            print(e)
            pass

    @pn.depends("localisation")  # , watch=True)
    def map_view(self):
        return self.tiles * gv.DynamicMap(self.update_map_values)

    @pn.depends("tout_axes", watch=True)
    def selection_indicateurs(self):
        for par in self.g_params:
            indic_name = next(iter(par.widgets))
            if "tout_axes" != indic_name:
                widg = par.widgets[indic_name].get("type", None)
                widg.param.select_all = self.tout_axes

    def table_view(self):
        script = """
        <script>
        if (document.readyState === "complete") {
        $('.mednum-df').DataTable();
        } else {
        $(document).ready(function () {
            $('.mednum-df').DataTable();
        })
        }
        </script>
        """
        df = self.df_score[self.selected_indices_level_0]
        df.index.names = [
            MAP_COL_WIDGETS_REV[name] if name in MAP_COL_WIDGETS_REV else name
            for name in df.index.names
        ]
        df.columns = [
            CATEGORIES_INDICES[name] if name in CATEGORIES_INDICES else name
            for name in df.columns
        ]

        html = df.to_html(classes=["mednum-df", "panel-df"])
        return pn.Column(
            self.download,
            pn.pane.HTML(html + script, sizing_mode="stretch_width"),
            sizing_mode="stretch_width"
        )

    @pn.depends("localisation")
    def tabs_view(self):
        return pn.Tabs(
            ("Carte", self.map_view),
            ("Tableau", self.table_view),
            css_classes=[
                re.sub(r"(?<!^)(?=[A-Z])", "-", self.get_name() + "Tabs").lower()
            ],
        )

