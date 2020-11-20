import pathlib
from panel.template import DefaultTheme
from panel.template import VanillaTemplate
import param
import base64

class MednumTemplate(VanillaTemplate):
    """
    MednumTemplate is built on top of BasicTemplate web components.
    """
    header_color = "#000000"

    logo_path = pathlib.Path(__file__).parent / "static" / "logo-MEDNUM.svg"
    
    _css = pathlib.Path(__file__).parent / "mednum.css"

    _template = pathlib.Path(__file__).parent / "mednum.html"

    def __init__(self):
        super(MednumTemplate, self).__init__()

        with open(self.logo_path, "rb") as image_file:
            self.logo = base64.b64encode(image_file.read())

        

    def _apply_root(self, name, model, tags):
        if "main" in tags:
            model.margin = (10, 15, 10, 10)


class MednumDefaultTheme(DefaultTheme):

    css = param.Filename(default=pathlib.Path(__file__).parent / "default.css")

    _template = MednumTemplate
