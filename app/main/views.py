import numpy as np
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.charts import Line
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from flask import Flask, render_template
from . import main
from ..models import Component


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/component/<int:id>/chart', methods=['GET'])
def chart(id):
    component = Component.query.get_or_404(id)
    ident = component.ident
    annual_risk = component.annual_risk
    inspect_int = component.inspect_int
    x = [0, inspect_int, inspect_int]
    y = [0, annual_risk, 0]
    hover = create_hover_tool()
    plot = create_rbi_chart(x, y, hover)
    script, div = components(plot)

    return render_template("chart.html", ident=ident, the_div=div,
                           the_script=script)


def create_hover_tool():
    """Generates the HTML for the Bokeh's hover data tool on our graph."""
    hover_html = """
        <div>
            <span class="hover-tooltip">Annual Risk: £@y{0.00}</span>
        </div>
        <div>
            <span class="hover-tooltip">Inspection Interval: @x yrs</span>
        </div>
    """
    return HoverTool(tooltips=hover_html)


def create_rbi_chart(x, y, hover_tool=None):

    tools = []
    if hover_tool:
        tools = [hover_tool, ]

    p = figure(plot_width=400, plot_height=400, tools=tools)
    p.line(x, y, line_width=2)
    p.xaxis.axis_label = 'Inspection Interval [yrs]'
    p.yaxis.axis_label = 'Annual Risk [£]'

    return p
