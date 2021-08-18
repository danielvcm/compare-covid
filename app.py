# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash

import dash_core_components as dcc
import dash_bootstrap_components as dbc
from src.interactables import DatePicker, Sliders, Button
from src.small_multiples import SmallMultiples
from src.stacked_areas import StackedAreas
from src.template import Template
from datetime import datetime


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

server = app.server

template = Template()
app.layout = template.make_layout()

# Callback to update sliders
@app.callback(
    [dash.dependencies.Output(component_id='date-slider-stacked-charts-div', component_property='children'),
     dash.dependencies.Output(component_id='date-slider-small-multiples-div', component_property='children')],
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])    
def update_slider(start_date, end_date):
    return Sliders.update_slider(start_date, end_date)
# Callback to update stacked-areas graph
@app.callback(
    dash.dependencies.Output('stacked-areas', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
    dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('metric-select-region', 'value')])
def update_stacked_areas(start_date, end_date, metric):
    stacked_areas = StackedAreas(start_date, end_date)
    fig = stacked_areas.make_plot(metric)
    return fig

# Callback to update small-multiples graph
@app.callback(
    dash.dependencies.Output('small-multiples', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
    dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('metric-select', 'value')])
def update_small_multiples(start_date, end_date, metric):
    small_multiples = SmallMultiples(start_date, end_date)
    fig = small_multiples.make_plot(metric)
    return fig

# Callback to update date-picker
@app.callback(
        [dash.dependencies.Output('date-picker-range', 'start_date'),
         dash.dependencies.Output('date-picker-range', 'end_date'),
         dash.dependencies.Output('last-value', 'data')],
        [dash.dependencies.Input('date-slider-stacked-charts', 'value'),
        dash.dependencies.Input('date-slider-small-multiples', 'value'),
        dash.dependencies.Input('last-value', 'data')]
    )
def update_date_picker_with_slider(first_slider_range_tuple, second_slider_range_tuple, last_values):
    """ 
        Workaround we use to have 2 sliders change a date picker.
        We use a variable called last values to figure out what slider changed (as we need to use a single callback)
        and update the date picker accordingly
    """
    return DatePicker.update_with_sliders(first_slider_range_tuple, second_slider_range_tuple, last_values)

@app.callback(
   dash.dependencies.Output(component_id='date-picker-div', component_property='style'),
   [dash.dependencies.Input(component_id='hide-date-picker', component_property='n_clicks')])
def show_hide_date_picker(clicked):
    return Button.show_hide_date_picker(clicked)

@app.callback(
   dash.dependencies.Output(component_id='hide-date-picker', component_property='children'),
   [dash.dependencies.Input(component_id='hide-date-picker', component_property='n_clicks')])
def update_button_text(clicked):
    return Button.update_button_text(clicked)

if __name__ == '__main__':
    app.run_server(debug=True)