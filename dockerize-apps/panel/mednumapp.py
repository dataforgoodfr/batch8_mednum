import holoviews as hv
import numpy as np
import panel as pn
import param
# from controlers.autocomplete import AutocompleteInput
import mednum as mind

pn.extension()

# from jinja2 import Environment, FileSystemLoader
# loader = FileSystemLoader("templates")
# env = Environment(loader=loader)
# jinja_template = env.get_template("mednum.html.j2")

# tmpl = pn.Template(jinja_template)

# tmpl.add_panel("sidenav", app_auto)  # hv.Curve([1, 2, 3]))
# tmpl.add_panel("B", hv.Curve([1, 2, 3]))

# tmpl.servable()

class App(param.Parameterized):
    string_value = param.String(default="China")

##############


##############

bootstrap = pn.template.BootstrapTemplate(title='Bootstrap Template')
mednumapp = mind.MedNumApp(name="Sélection Med")
# overall = mind.overallparameters.OverallParameters()


# OBJECTS = ["China", "Thailand", "Japan"]
# app_auto = AutocompleteInput(default="China", object=OBJECTS)

# OBJECTS = ["oi", "oiiii"]


pn.config.sizing_mode = "stretch_width"

xs = np.linspace(0, np.pi)
freq = pn.widgets.FloatSlider(name="Frequency", start=0, end=10, value=2)
phase = pn.widgets.FloatSlider(name="Phase", start=0, end=np.pi)


# @pn.depends(freq=freq, phase=phase)
# def sine(freq, phase):
#     return hv.Curve((xs, np.sin(xs * freq + phase))).opts(
#         responsive=True, min_height=400
#     )


# @pn.depends(freq=freq, phase=phase)
# def cosine(freq, phase):
#     return hv.Curve((xs, np.cos(xs * freq + phase))).opts(
#         responsive=True, min_height=400
#     )


#bootstrap.sidebar.append(overall)
bootstrap.sidebar.append(mednumapp)
bootstrap.sidebar.append(phase)

bootstrap.main.append(
    pn.Row(
    #     pn.Card(hv.DynamicMap(sine), title="Sine"),
    #     pn.Card(hv.DynamicMap(cosine), title="Cosine"),
    )
)
bootstrap.servable()
