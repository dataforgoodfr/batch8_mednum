from panel.template import DefaultTheme
import panel as pn
import holoviews as hv
import base64

from templates import MednumTemplate, MednumDefaultTheme
from debbuger import initialize_panel_server_debugger_if_needed
# pn.template.MaterialTemplate
# DefaultTheme.find_theme(MednumTemplate)
mednum_tmpl =pn.template.VanillaTemplate(title='Mednum', theme=MednumDefaultTheme)


mednum_tmpl.header.append('OK')
mednum_tmpl.sidebar.append("PL")

mednum_tmpl.main.append(
    pn.Row(
      'A', hv.Curve([1, 3, 3])
    )
)

mednum_tmpl.servable();