from pathlib import Path

import panel as pn
from jinja2 import Environment, FileSystemLoader

import mednum

css_mednum = [
    str(Path(__file__).parent / "statics" / "css" / "mednum.css"),
    str(Path(__file__).parent / "statics" / "css" / "landing-page.min.css"),
]

css = [
    "https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css",
    "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
] + css_mednum
js = {
    "$": "https://code.jquery.com/jquery-3.4.1.slim.min.js",
    "DataTable": "https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js",
}

pn.extension(css_files=css)

# use Jinja template
env = Environment(loader=FileSystemLoader("./templates"))
jinja_template = env.get_template("mednum.html")


# tmpl = pn.Template(template)
tmpl = pn.Template(jinja_template)
tmpl.add_variable("app_title", "<h1>Custom Template App</h1>")

mednumapp = mednum.MedNumApp(name="Sélection")

# Top indicator
tmpl.add_panel("sidebar", mednumapp.lat_widgets)
tmpl.add_panel("top", pn.Row(mednumapp.top_panel, sizing_mode="stretch_width")),
tmpl.add_panel(
    "main", mednumapp.tabs_view,
)

tmpl.servable()
