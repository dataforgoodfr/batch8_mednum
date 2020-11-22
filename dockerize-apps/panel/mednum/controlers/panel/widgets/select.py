"""
Defines various Select widgets which allow choosing one or more items
from a list of options.
"""
from __future__ import absolute_import, division, unicode_literals

from collections import OrderedDict
from distutils.version import LooseVersion

import bokeh
import param
from bokeh.models.widgets import AutocompleteInput as _BkAutocompleteInput
from panel.widgets.base import Widget

# from .base import Widget
bokeh_version = LooseVersion(bokeh.__version__)



_AutocompleteInput_rename = {'name': 'title', 'options': 'completions'}
if bokeh_version < '2.3.0':
    # disable restrict keyword
    _AutocompleteInput_rename['restrict'] = None

class AutocompleteInputMednum(Widget):

    min_characters = param.Integer(default=2, doc="""
        The number of characters a user must type before
        completions are presented.""")

    options = param.List(default=[])

    placeholder = param.String(default='')

    value = param.Parameter(default=None)
    
    case_sensitive = param.Boolean(default=True)

    restrict = param.Boolean(default=True)

    _widget_type = _BkAutocompleteInput

    _rename = _AutocompleteInput_rename

    def __init__(self, **params):
        options = params.get('options')
        if isinstance(options, OrderedDict):
            params['options'] = list(params['options'].keys()) +[k.lower() for k in params['options'].keys()]
        super(AutocompleteInputMednum, self).__init__(**params)