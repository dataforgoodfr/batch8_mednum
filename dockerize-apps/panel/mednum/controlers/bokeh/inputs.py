from bokeh.core.properties import Bool, List, PositiveInt, String
from bokeh.models.widgets.inputs import TextInput


class AutocompleteInput(TextInput):
    """Single-line input widget with auto-completion."""

    completions = List(
        String,
        help="""
    A list of completion strings. This will be used to guide the
    user upon typing the beginning of a desired value.
    """,
    )

    fuzzy_comparison = Bool(default=True, help="""Enable or disable fuzzy comparison""")

    fuzzy_threshold = PositiveInt(
        default=10,
        help="""
    The number of character difference to calculate Levensthein distance.
    """,
    )

    min_characters = PositiveInt(
        default=2,
        help="""
    The number of characters a user must type before completions are presented.
    """,
    )

    case_sensitive = Bool(default=True, help="""Enable or disable case sensitivity""")

    restrict = Bool(
        default=True,
        help="""
    Set to False in order to allow users to enter text that is not present in the list of completion strings.
    """,
    )