import panel as pn
import numpy as np
import holoviews as hv
import numpy as np
import panel as pn
from panel.widgets.select import AutocompleteInput
import param
from mednum.config import *
from mednum.loaders import read_merged_data

# from mednum.controlers.autocomplete import AutocompleteInput
from mednum.indicators.panels import TopIndicators, IndicatorsWithGauge
from pathlib import Path
import mednum

# import flamegraph
# flamegraph.start_profile_thread(fd=open("./perf.log", "w"))

css_mednum = [str(Path(__file__).parent / "statics" / "css" / "mednum.css")]

css = [
    "https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css",
    css_mednum[0],
]
js = {
    "$": "https://code.jquery.com/jquery-3.4.1.slim.min.js",
    "DataTable": "https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js",
}

# pn.config.js_files = js
# pn.config.css_files = css
# with open(css_mednum[0], 'r') as fin: raw_css = fin.read()

# pn.config.raw_css = [raw_css]
pn.extension(css_files=css_mednum)  # raw_css = [raw_css])

template = """
{% extends base %}

<!-- goes in body -->
{% block postamble %}
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
{% endblock %}

<!-- goes in body -->
{% block contents %}
{{ app_title }}
<p>This is a Panel app with a custom template allowing us to compose multiple Panel objects into a single HTML document.</p>
<br>
<div class="container-fluid">
<div class="row">
    <div class="col-sm-2">
          {{ embed(roots.sidebar) | indent(8) }}
    </div>
    <div class="col-sm-8 ml-auto">
      <div class="row">
      {{ embed(roots.top) | indent(8) }}
      </div>
      <div class="row">
          {{ embed(roots.main) | indent(8) }}
      </div>
    </div>
    
  </div>
</div>


{% endblock %}
"""
# {{ embed(roots.top) | indent(8) }}


tmpl = pn.Template(template)
tmpl.add_variable("app_title", "<h1>Custom Template App</h1>")

# pn.config.sizing_mode = "stretch_width"


# # Sidebar
# class AutoComplete(param.Parameterized):
#     nom_commune = param.String()


mednumapp = mednum.MedNumApp(name="Sélection")

# auto_complete_param = AutoComplete()
# auto_complete = pn.Param(auto_complete_param, widgets={"string_value": {"type": pn.widgets.AutocompleteInput, "options": NOM_COMMUNES}})
# score_widget = pn.widgets.IntRangeSlider()
# sidebar = pn.Column(auto_complete, score_widget)
#sidebar = pn.Column(mednumapp.lat_widgets())

# Top indicator
tmpl.add_panel("sidebar", mednumapp.lat_widgets)
tmpl.add_panel("top", pn.panel(mednumapp.top_panel, height=200)),
tmpl.add_panel("main", mednumapp.map_view) 
# tmpl.add_panel("main", mednumapp.table_view) 

tmpl.servable()
