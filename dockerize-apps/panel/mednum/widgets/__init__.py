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
    option_descriptions = param.List()    
    all_selector = None
    
    def __init__(self, **params):
        super(TreeViewCheckBox, self).__init__(**params)

        self.select_all = params.get('select_all', "") 
        self.select_options = params.get('select_options', "") 
        
        self.option_descriptions = params.get('description', [])

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

