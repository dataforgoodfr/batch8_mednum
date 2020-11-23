import param
import panel as pn

from panel.widgets.base import CompositeWidget, Widget
from panel.widgets.select import MultiSelect, CheckBoxGroup
from panel.layout import Column, VSpacer, Row
from panel.widgets.input import Checkbox

def css2dict(css_str):
    css_style = {}
    for style in css_str.replace(";", "").split("\n"):
        if style:
            try:
                k, v = style.split(":")
                css_style[k.strip()] = v.strip()
            except Exception as e:
                print(e)
                print(style)
                pass
    return css_style


class TreeViewCheckBox(CompositeWidget, MultiSelect):
    _composite_type = Column
    box_size = param.Number(default=100)
    select_all = param.String()
    select_options = param.List()

    def __init__(self, **params):
        super(TreeViewCheckBox, self).__init__(**params)
        options = list(params.get('options', {}).keys())

        try:
            self.select_all= options.pop(0)
        except NameError as n:
            raise NameError("Define a dict containing the name of **select_all**")
        except:
            raise Exception
        
        try:
            self.select_options= options
        except NameError as n:
            raise NameError("Define a dict containing a list of options in **select_options**")
        except:
            raise Exception
        TreeViewCheckBox.box_size = max([len(word) for word in self.select_options]+ [len(self.select_all), TreeViewCheckBox.box_size]) * 10
        
        self.all_selector = Checkbox(name=self.select_all)
        self.all_selector.param.watch(self._update_all, 'value')

        self.selected_options = CheckBoxGroup(
            name='Checkbox Group', value=[], options=self.select_options,
        )
        self.selected_options.param.watch(self._update_selected_options, 'value')

        self.all_drop = Checkbox(css_classes=['chck-custom'])
        self.all_drop.param.watch(self._show_drop_down, 'value')

        # Define Layout
        self._composite[:]  = [ #HTML(self._css_injection, width=0, height=0, margin=0, sizing_mode="fixed"),
            Column(
                Row(
                    Row(
                        self.all_selector, 
                        max_width=self.box_size
                    ), 
                    self.all_drop
                ), 
                max_width=self.box_size
            )
        ]
        
    def _update_all(self, event):
        if self.all_selector.value:
            self.selected_options.value = self.select_options
            self.value = [self.all_selector.name] + self.select_options
        else:
            if len(self.select_options[:-1]) != len(self.selected_options.value):
                self.selected_options.value = []
                self.value = []
    
    def _update_selected_options(self, event):
        if len(self.select_options) == len(self.selected_options.value):
            self.all_selector.value = True
        else:
            self.all_selector.value = False
        self.value = self.selected_options.value

    def _show_drop_down(self, event):
        if self.all_drop.value:
            self._composite.append(self.selected_options)
        else:
            self._composite[:] = self._composite[:-1]

    def _get_model(self, doc, root=None, parent=None, comm=None):
        return self._composite._get_model(doc, root, parent, comm)


class Export(param.Parameterized):
    export_data = param.Action(
        lambda x: x.timestamps.append(dt.datetime.utcnow()),
        doc="""Exporter les résultats""",
        precedence=0.7,
    )
    edit_report = param.Action(
        lambda x: x.timestamps.append(dt.datetime.utcnow()),
        doc="""Editer un rapport""",
        precedence=0.7,
    )


class Score(param.Parameterized):
    score = param.Range(default=(0, 250), bounds=(0, 250))


class Localisation(param.Parameterized):
    localisation = param.String(default="Marseille", label="", doc="A string")


class Reference(param.Parameterized):
    point_ref = param.ListSelector(
        objects=["Pays", "Région", "Département", "Intercommune", "Commune"],
        label="Point de référence",
    )

    donnees_infra = param.Action(
        lambda x: x, doc="""Données Infra-Communales""", precedence=0.7
    )


# class TreeViewCheckBoxCompo(param.Parameterized):
#     OPTIONS_INT_NUM = [
#         "Taux de pauvreté",
#         "Equipement des ménages",
#         "Couverture mobile",
#         "Taux de couverture HD / THD",
#     ]
#     CATEGORIES_INT_NUM = {
#         "select_all": "Accès aux interfaces numériques",
#         "select_options": OPTIONS_INT_NUM,
#     }

#     OPTIONS_X_INFOS = ["Oui", "Non"]
#     CATEGORIES_X_INFOS = {
#         "select_all": "Accès à l'info",
#         "select_options": OPTIONS_X_INFOS,
#     }

#     OPTIONS_X_COMP_ADMIN = ["Oui", "Non"]
#     CATEGORIES_X_COMP_ADMIN = {
#         "select_all": "Compétences adminitratives",
#         "select_options": OPTIONS_X_COMP_ADMIN,
#     }

#     OPTIONS_X_COMP_USAGE = ["Oui", "Non"]
#     CATEGORIES_X_COMP_USAGE = {
#         "select_all": "Compétences usages numériques",
#         "select_options": OPTIONS_X_COMP_USAGE,
#     }

#     ind_x_interfaces_num = TreeViewCheckBox(tree_categories=CATEGORIES_INT_NUM)
#     ind_x_infos_num = TreeViewCheckBox(tree_categories=CATEGORIES_X_INFOS)
#     ind_x_comp_admi = TreeViewCheckBox(tree_categories=CATEGORIES_X_COMP_ADMIN)
#     ind_x_comp_uasge_num = TreeViewCheckBox(tree_categories=CATEGORIES_X_COMP_USAGE)

#     indicateurs = pn.Column(
#         pn.pane.Markdown("\n**Indicateurs**"),
#         ind_x_interfaces_num.panel,
#         ind_x_infos_num.panel,
#         ind_x_comp_admi.panel,
#         ind_x_comp_uasge_num.panel,
#     )

#     def __init__(self, **params):
#         super().__init__(**params)
#         print(self.ind_x_interfaces_num.param)

#     def panel(self):
#         return self.indicateurs
