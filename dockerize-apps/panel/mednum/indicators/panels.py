import re
from pathlib import Path

import panel as pn
import param
import pygal
from pygal.style import Style

from mednum.controlers.overallparameters import OverallParameters
from mednum.tools import css2dict
from mednum.config import *

css_file_gauge = Path(__file__).parent.parent / "css" / "pygauge.css"


class PyGauge(param.Parameterized):
    value = param.Integer(85, bounds=(0, 1000))
    max_value = param.Integer(150)
    pygal_config = pygal.Config()

    custom_style = param.Dict(
        default=dict(
            background="transparent",
            plot_background="transparent",
            foreground="#0000ff",  # 53E89B",
            foreground_strong="#53A0E8",
            foreground_subtle="transparent",
            opacity=".2",
            opacity_hover=".9",
            transition="400ms ease-in",
            colors=("#0000ff", "#ff0000"),
        )
    )
    custom_style_css_path = param.Filename(css_file_gauge)

    css_info_h2 = """
        margin: auto;
    """
    size_w = param.Integer(100)
    value_font_size = param.Integer()
    w_name = ""

    def __init__(self, **params):
        super(PyGauge, self).__init__(**params)
        self.set_max()
        self.value_font_size = len(str(self.value)) * self.size_w
        self.w_name = self.name

    @pn.depends("value_font_size", "custom_style", watch=True)
    def set_style(self):
        if self.custom_style_css_path:
            self.pygal_config.css.append(self.custom_style_css_path)
            # with open(self.custom_style_css_path, 'r') as f: css = f.read()
            # self.custom_style = css2dict(css)

        self.custom_style["value_font_size"] = self.value_font_size
        self.param["custom_style"].default = self.custom_style

    @pn.depends("max_value", watch=True)
    def set_max(self):
        self.param.value.bounds = (0, self.max_value)
        if self.max_value == 0:
            self.max_value = int(1e5)
        self.value = self.max_value if self.value > self.max_value else self.value

    @pn.depends("value", "custom_style", watch=True)
    def create_gauge(self):
        gauge = pygal.SolidGauge(
            inner_radius=0.70, show_legend=False, style=Style(**self.custom_style),
        )
        percent_formatter = lambda x: "{:.10g}".format(x)
        gauge.value_formatter = percent_formatter
        vals = {"value": self.value, "max_value": self.max_value}
        gauge.add("", [vals])
        self.file_name = gauge.render_data_uri()
        self.HTML_GAUGE_HEADER = """
        <h2 style="{css_info_h2}">{name}</h2>
        """.format(
            name=self.w_name, css_info_h2=self.css_info_h2,
        )

        self.HTML_GAUGE_IMG = """
        <img src="{filepath}" width="{width}px" />
        
        """.format(
            filepath=self.file_name, width=self.size_w,
        )

    def view(self):
        self.create_gauge()
        return pn.pane.HTML(
            self.HTML_GAUGE_HEADER + self.HTML_GAUGE_IMG,
            css_classes=[re.sub(r"(?<!^)(?=[A-Z])", "-", type(self).__name__).lower()],
        )


class Indicators(PyGauge):  # param.Parameterized):
    indicators = param.List(
        [
            dict(name="indic2", main=True, value=50, max_value=100, img_path=''),
            dict(name="indic2", value=150),
        ]
    )
    other_indic = []
    css_info_td = """
        align-items: center;
        text-transform: capitalize;
        border-left: #E65924 solid 8px;
        padding: 8px;
        line-height: 14px;
    """
    css_info_h3 = """
        margin: auto;
        font-size: 1rem;
    """
    main_indicators_name = ""
    with_gauge_true = param.Boolean(False)

    def __init__(self, **params) -> None:
        super(Indicators, self).__init__(**params)
        self.set_indicators()

    @pn.depends("indicators", watch=True)
    def set_indicators(self):

        for ind in self.indicators:
            if "main" in ind:
                self.with_gauge_true = True
                self.max_value = ind["max_value"]
                self.value = ind["value"]
                self.main_indicators_name = ind["name"]
        self.other_indic = []
        for ind in self.indicators:
            if ind["name"] != self.main_indicators_name:
                self.other_indic.append(ind)
        try:
            c2d = css2dict(self.css_info_td)
            font_h = int(c2d["font-size"].replace("px", ""))
            pad = int(c2d["padding"].replace("px", ""))
        except:
            font_h = 18
            pad = 10
        self.size_w = (((font_h * 2) + (pad * 2)) * len(self.indicators)) * 7 // 10

    def view(self):
        self.w_name = self.main_indicators_name
        self.create_gauge()
        rowspan = len(self.indicators) - 1

        HTML_MAIN_INDIC = """<table class="gauge-cls" style="border-spacing: 1em">"""

        if self.with_gauge_true:
            HTML_MAIN_INDIC += """
            <tr class="gauge-tr">
                <td class="gauge-td" style="{style}">{gauge_header}
                </td>
        """.format(
                rowspan=rowspan,
                gauge_header=self.HTML_GAUGE_HEADER,
                gauge_img=self.HTML_GAUGE_IMG,
                style=self.css_info_td,
            )

            HTML_GAUGE = """
                    <td class="gauge-td" rowspan={rowspan} style="{style}">{gauge_img}</td>
            """.format(
                rowspan=rowspan,
                gauge_header=self.HTML_GAUGE_HEADER,
                gauge_img=self.HTML_GAUGE_IMG,
                style=self.css_info_td,
            )
        HTML_ROWS = []
        for row in self.other_indic:
            if 'img_path' not in row:
                row['img_path'] = ''
            HTML_ROWS.append(
            """
            <td class="gauge-td" style="{style}">
            <h3 style="{style_h3}"><img src="{filepath}" width="{width}px" />{title}</h3>
                {value}
            </td>
            </tr>
        """.format(
                title=row["name"],
                value=row["value"],
                style=self.css_info_td,
                style_h3=self.css_info_h3,
                filepath=row['img_path'],
                width=0
            )
        )
        if self.with_gauge_true:
            # insert Gauge in second order
            HTML_ROWS.insert(1, HTML_GAUGE)

        HTML = HTML_MAIN_INDIC + "<tr>\n".join(HTML_ROWS) + "\n<tr>\n</table>"
        return pn.panel(
            pn.pane.HTML(HTML),
            sizing_mode="stretch_both",
            css_classes=[re.sub(r"(?<!^)(?=[A-Z])", "-", type(self).__name__).lower()],
        )


indic_w_g_value_1 = {
    "name": "indic1_1",
    "indicators": [
        # dict(name="accès", main=True, value=85, max_value=100),
        dict(name="info", value=118),
        dict(name="Interfaces", value=53),
    ],
}

indic_w_g_value_2 = {
    "indicators": [
        # dict(name="Compétences", main=True, value=135, max_value=180),
        dict(name="indic3_2", value=115),
        dict(name="indic4", value=155),
    ]
}


class TopIndicators(OverallParameters):
    indicators_value_1 = param.Dict(default=indic_w_g_value_1)
    indicators_value_2 = param.Dict(default=indic_w_g_value_2)

    def get_name(self):
        return self.__class__.__name__

    def __init__(self, **params) -> None:
        super(TopIndicators, self).__init__(**params)
        self.indicators_value_1 = params.get("indicators_value_1", indic_w_g_value_1)
        self.indicators_value_2 = params.get("indicators_value_2", indic_w_g_value_2)

        self.score = params.get("score", (0, 250))
        self.localisation = params.get("localisation", "Jegun")

        self.indicator_w_gauge_1 = Indicators(**self.indicators_value_1)
        self.indicator_w_gauge_2 = Indicators(**self.indicators_value_2)

    @pn.depends("score", watch=True)
    def synthese(self):
        HTML = """
        <h3>Scores par axe de fragilité</h3>
        
        Un score supérieur à 100 indique une fragilité. Plus le score est élevé, plus le risque d'exclusion numérique est important.
        """
        return pn.pane.HTML(
            HTML,
            css_classes=[
                re.sub(r"(?<!^)(?=[A-Z])", "-", self.get_name() + "Synthese").lower()
            ],
        )

    @pn.depends("score", watch=True)
    def glob_stats(self):
        label = "Score Global"
        score_min, score_max = self.score
        HTML = """
        <b>{score_name}</b> | {score_min}->{score_max}<br>

        <b>{pop_name}</b> | {population}
        """.format(
            score_name=label,
            score_min=int(score_min),
            score_max=int(score_max),
            pop_name="Population",
            population=1055000,
        )
        return pn.pane.HTML(
            HTML,
            css_classes=[
                re.sub(r"(?<!^)(?=[A-Z])", "-", self.get_name() + "-Globstats").lower()
            ],
        )

    def score_par_axe(self, name, with_axe=False):
        indicator = []
        score_axe_total = 0

        info_loc = self.info_localisation()

        global_score = self.df_score

        local_score = self.df_score.xs(
            self.level_0_value, level=self.level_0_column_names
        )
        max_value_total = 0
        score_axe_total = 0
        n = 0
        for axis_key, axis_categories in TREEVIEW_CHECK_BOX.items():
            if axis_categories != {}:
                axis_name = axis_categories["nom"]
                if name in axis_name:
                    score_axe = int(local_score[axis_key])
                    max_value = int(global_score[axis_key].max())
                    score_axe_total += score_axe
                    max_value_total += max_value
                    indicator.append(
                        dict(
                            name=axis_name.replace(name + " ", ""),
                            value=score_axe,
                            max_value=max_value,
                        )
                    )
                    n += 1
        if with_axe:
            indicator.append(
                dict(
                    name=name,
                    main=True,
                    value=score_axe_total // n,
                    max_value=max_value_total // n,
                )
            )
        return indicator

    @pn.depends("score", "localisation", "point_ref", "df_score")
    def top_panel(self):
        HTML = """
        <h1>{loc}</h1>
        """.format(
            loc=self.localisation
        )

        indicator_1 = self.score_par_axe(name="Accès")
        indicator_2 = self.score_par_axe(name="Compétences")

        self.indicator_w_gauge_1.indicators = indicator_1
        self.indicator_w_gauge_2.indicators = indicator_2

        return pn.Row(
            pn.Column(
                HTML, self.synthese(), min_width=20 * 12
            ),  # , self.glob_stats()),
            # pn.Column(self.synthese()),
            pn.Column(self.indicator_w_gauge_1.view),
            pn.Column(self.indicator_w_gauge_2.view),
            css_classes=[
                re.sub(r"(?<!^)(?=[A-Z])", "-", self.get_name() + "TopPanel").lower()
            ],
            # min_height=200,
            min_width=900,
        )

    @pn.depends("score", "localisation")
    def view(self):
        HTML = """
        <h1>{loc}</h1>
        """.format(
            loc=self.localisation
        )

        return pn.Row(
            pn.Column(HTML, self.glob_stats(), pn.layout.VSpacer()),
            pn.layout.HSpacer(),
            pn.Column(self.synthese(), pn.layout.VSpacer()),
            pn.layout.HSpacer(),
            pn.Column(self.indicator_w_gauge_1.view, pn.layout.VSpacer()),
            pn.layout.HSpacer(),
            self.indicator_w_gauge_2.view,
            css_classes=[re.sub(r"(?<!^)(?=[A-Z])", "-", type(self).__name__).lower()],
        )


class test_class(param.Parameterized):
    some_parameter = param.Integer()

    def __init__(self, **params):
        super(test_class, self).__init__(**params)

    def view(self):
        return pn.Column(
            pn.widgets.FloatSlider(name="Number", margin=(10, 5, 5, 10)),
            pn.widgets.Select(
                name="Fruit", options=["Apple", "Orange", "Pear"], margin=(0, 5, 5, 10)
            ),
            pn.widgets.Button(name="Run", margin=(5, 10, 10, 10)),
            css_classes=["panel-widget-box"],
        )


def test_function():
    return pn.Column(
        pn.widgets.FloatSlider(name="Number", margin=(10, 5, 5, 10)),
        pn.widgets.Select(
            name="Fruit", options=["Apple", "Orange", "Pear"], margin=(0, 5, 5, 10)
        ),
        pn.widgets.Button(name="Run", margin=(5, 10, 10, 10)),
        css_classes=["panel-widget-box"],
    )
