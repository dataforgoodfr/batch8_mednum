import panel as pn
import param
from param.parameterized import depends

OBJECTS = ["China", "Thailand", "Japan"]


class AppAuto(param.Parameterized):
    string_value = param.ObjectSelector(default="China", objects=OBJECTS)
    string_value2 = param.ObjectSelector(default="China", objects=OBJECTS)

    def __init__(self, **params) -> None:
        super().__init__(**params)
        self.auto = pn.Param(
            self,
            parameters=["string_value"],
            widgets={
                "string_value": {
                    "type": pn.widgets.AutocompleteInput,
                    # "options": OBJECTS,
                    "case_sensitive":False
                }
            },
        )

    @pn.depends("string_value", watch=True)
    def get_opts(self):
        pass

    def view(self):
        return pn.Column(
            self.auto,
            self.string_value,  # self.string_value2
        )