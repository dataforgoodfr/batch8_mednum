import pathlib
from panel.template import DefaultTheme
from panel.template.base import BasicTemplate
from panel.template import VanillaTemplate
from panel.template.material import MaterialDefaultTheme
import param
import base64


# class MednumTemplate(VanillaTemplate):
#     """
#     MednumTemplate is built on top of BasicTemplate web components.
#     """

#     # header_color = "#000000"
#     # header_background = "#000000"
#     logo_path = pathlib.Path(__file__).parent / "statics" / "logo-MEDNUM.png"

#     _css = pathlib.Path(__file__).parent.parent / "statics" / "css" / "mednum.css"

#     # _template = pathlib.Path(__file__).parent / "mednum.html"

#     # def __init__(self, **params):
#     #     super(MednumTemplate, self).__init__(**params)

#         # with open(self.logo_path, "rb") as image_file:
#         #     img_b64 = str(base64.b64encode(image_file.read()))
#         #     self.logo = img_b64

#     def _apply_root(self, name, model, tags):
#         if "main" in tags:
#             model.margin = (10, 15, 10, 10)


# class MednumDefaultTheme(DefaultTheme):

#     # css = param.Filename(
#     #     default=pathlib.Path(__file__).parent.parent / "statics" / "css" / "mednum.css"
#     # )

#     _template = MednumTemplate



class MednumTemplate(BasicTemplate):
    """
    MednumTemplate
    """

    _css = pathlib.Path(__file__).parent / 'bootstrap.css'

    _template = pathlib.Path(__file__).parent / 'bootstrap.html'

    # _modifiers = {
    #     Card: {
    #         'children': {'margin': (10, 10)},
    #         'button_css_classes': ['card-button'],
    #         'margin': (10, 5)
    #     },
    # }

    _resources = {
        'css': {
            'bootstrap': "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
        },
        'js': {
            'bootstrap': "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js",
            'jquery': "https://code.jquery.com/jquery-3.4.1.slim.min.js"
        }
    }


class MednumDefaultTheme(DefaultTheme):

    css = param.Filename(default=pathlib.Path(__file__).parent / 'default.css')

    _template = MednumTemplate
