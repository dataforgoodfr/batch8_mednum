import numpy
import pandas
import param
import panel
import holoviews


panel.extension()
holoviews.extension('bokeh')

# Create syntetic dataset
N= 1000
age = numpy.random.gamma(10, 1.5, N)
defects = numpy.clip(numpy.random.chisquare(5, N) * age - 10, 0, 1e100).astype(int)
df = pandas.DataFrame({'age': age, 'defects': defects})


class DashboardDefinition(param.Parameterized):
    age = param.Range((0, 20), (0, None), softbounds=(0, 30))
    histogram = param.ObjectSelector('defects', ['defects', 'age'])

    def filter_data(self, table):
        return table.select(age=self.age)

    @param.depends('age')
    def make_scatter(self):
        scatter = holoviews.Points(df, ['age', 'defects'])
        selected = self.filter_data(scatter)
        hv_obj = selected.options(responsive=True, aspect=3)
        return panel.panel(hv_obj)

    @param.depends('age', 'histogram')
    def make_histogram(self):
        table = holoviews.Table(df, self.histogram)
        table = self.filter_data(table)
        frequencies, edges = numpy.histogram(table[self.histogram], 25)
        hist = holoviews.Histogram((frequencies, edges))
        hv_obj = hist.options(responsive=True, aspect=4)
        return panel.panel(hv_obj)

    def layout(self):
        return panel.Column(panel.Row(self.param,
                                      self.make_scatter,
                                      sizing_mode='stretch_width'),
                            self.make_histogram,
                            sizing_mode='stretch_width')


dashboard = DashboardDefinition(name='Dashboard parameters')
dash_panel = dashboard.layout() 

# Define the dashboard
template = """
{% extends base %}

{% block preamble %}
<style>
div#dashboard {
    width: 80%;
    margin: 0 auto;
}
</style>
{% endblock preamble %}

{% block contents %}
<div id="dashboard">
  <h1>My dashboard</h1>
  {{ embed(roots.dash1) }}
</div>
{% endblock contents %}
"""
tmpl = panel.Template(template)
tmpl.add_panel('dash1', dash_panel)
tmpl.servable(title="My page title")

# Uncomment to preview dashboard in jupyter notebook
#dash_panel
