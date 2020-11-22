import param
import panel as pn


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


class TreeViewCheckBox(param.Parameterized):
    # tree_categories = param.Parameter()
    # all_checkbox = param.Boolean()
    box_size = param.Number()

    def __init__(self, tree_categories, **params):
        self.tree_categories = tree_categories
        # .get("tree_categories",

        try:
            all_checkbox_label = self.tree_categories["select_all"]
        except NameError as n:
            raise NameError("Define a dict containing the name of **select_all**")
        except:
            raise Exception

        try:
            self.options = self.tree_categories["select_options"]
        except NameError as n:
            raise NameError(
                "Define a dict containing a list of options in **select_options**"
            )
        except:
            raise Exception

        TreeViewCheckBox.box_size = (
            max(
                [len(word) for word in self.options]
                + [len(all_checkbox_label), TreeViewCheckBox.box_size]
            )
            * 10
        )

        self.all_checkbox = pn.widgets.Checkbox(name=all_checkbox_label)
        self.select_string = pn.widgets.CheckBoxGroup(
            name="Checkbox Group",
            value=[],
            options=self.options,
        )
        self.all_drop = pn.widgets.Checkbox(css_classes=["chck-custom"])

        self.init_tree_panel()
        super().__init__(**params)

    def checked_values(self):
        return [self.all_checkbox.name] + self.select_string.values
        # max([len(word) for word in self.options]+ [len(all_checkbox_label), TreeViewCheckBox.box_size]) * 10

    @param.depends("box_size", watch=True)
    def init_tree_panel(self):
        self._initial_tree = pn.Row(
            pn.Row(self.all_checkbox, max_width=self.box_size), self.all_drop
        )

    @pn.depends("all_checkbox.value", watch=True)
    def _update_all(self):
        if self.all_checkbox.value:
            self.select_string.value = self.select_string.options
        else:
            if len(self.options[:-1]) != len(self.select_string.value):
                self.select_string.value = []

    @pn.depends("select_string.value", watch=True)
    def _update_select_string(self):
        if len(self.options) == len(self.select_string.value):
            self.all_checkbox.value = True
        else:
            self.all_checkbox.value = False

    @pn.depends("all_drop.value")
    def panel(self):
        self._initial_tree = pn.Row(
            pn.Row(self.all_checkbox, max_width=self.box_size), self.all_drop
        )
        if self.all_drop.value:
            return pn.Column(self._initial_tree, self.select_string)

        else:
            return pn.Column(self._initial_tree)


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


class TreeViewCheckBoxCompo(param.Parameterized):
    OPTIONS_INT_NUM = [
        "Taux de pauvreté",
        "Equipement des ménages",
        "Couverture mobile",
        "Taux de couverture HD / THD",
    ]
    CATEGORIES_INT_NUM = {
        "select_all": "Accès aux interfaces numériques",
        "select_options": OPTIONS_INT_NUM,
    }

    OPTIONS_X_INFOS = ["Oui", "Non"]
    CATEGORIES_X_INFOS = {
        "select_all": "Accès à l'info",
        "select_options": OPTIONS_X_INFOS,
    }

    OPTIONS_X_COMP_ADMIN = ["Oui", "Non"]
    CATEGORIES_X_COMP_ADMIN = {
        "select_all": "Compétences adminitratives",
        "select_options": OPTIONS_X_COMP_ADMIN,
    }

    OPTIONS_X_COMP_USAGE = ["Oui", "Non"]
    CATEGORIES_X_COMP_USAGE = {
        "select_all": "Compétences usages numériques",
        "select_options": OPTIONS_X_COMP_USAGE,
    }

    ind_x_interfaces_num = TreeViewCheckBox(tree_categories=CATEGORIES_INT_NUM)
    ind_x_infos_num = TreeViewCheckBox(tree_categories=CATEGORIES_X_INFOS)
    ind_x_comp_admi = TreeViewCheckBox(tree_categories=CATEGORIES_X_COMP_ADMIN)
    ind_x_comp_uasge_num = TreeViewCheckBox(tree_categories=CATEGORIES_X_COMP_USAGE)

    indicateurs = pn.Column(
        pn.pane.Markdown("\n**Indicateurs**"),
        ind_x_interfaces_num.panel,
        ind_x_infos_num.panel,
        ind_x_comp_admi.panel,
        ind_x_comp_uasge_num.panel,
    )

    def __init__(self, **params):
        print(self.ind_x_interfaces_num.param)

    def panel(self):
        return self.indicateurs
