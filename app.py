# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd

from dash_core_components.Markdown import Markdown
from dash_html_components.Div import Div

from src.small_multiples import SmallMultiples
from src.stacked_areas import StackedAreas

from src.time_utils import unix_timestamp_millis, get_marks_from_start_end, daterange, get_day_from_timestamp
from datetime import datetime


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

server = app.server


app.layout = html.Div(
    [
    html.Div(children=[
        dcc.Store(id='last-value'),
        html.H1(children='Compare Covid', 
                className="app-header--title",       
                style={
                    'textAlign': 'center',
                    'padding-top': '5%',
                    'padding-bottom': '5%',
                    'background': ''
                }
            ),
        
        dcc.Markdown("""Nosso projeto permite a comparação de infecções e óbitos por COVID-19 nos diferentes estados e
                    regiões do Brasil. Os dados utilizados nesta aplicação são fornecidos pelo Governo Federal no site
                    [Coronavirus Brasil](https://covid.saude.gov.br/)."""),
        
        dcc.Markdown("""Temos dois tipos de visualizações, uma para dados absolutos e outra para métricas que tentam normalizar
                    os dados para que não haja uma distorção entre estados com muito e pouco populosos."""),

        dcc.Markdown("""Para ambas, deve-se primeiro selecionar um período no tempo no qual os dados serão extraídos. Sugerimos escolher
                    ao menos uma semana, para que alterações no fluxo de envios de relatórios por parte das secretarias de saúde não
                    distorçam os gráficos."""),
        html.Br(),
        
        ], style={'padding': '0% 20%', }),
    html.Div(
        [
        dbc.Card(
            dbc.CardBody([
            html.Div([ html.H5('Selecione um período:'),
            dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=datetime(2020, 2, 25),
            max_date_allowed=datetime(2021, 6, 30),
            initial_visible_month=datetime(2020, 3, 9),
            start_date=datetime(2020, 8, 9),
            end_date=datetime(2020, 8, 15),
            minimum_nights = 7
            )],id='date-picker-div'),
            dbc.Button('Esconder',id='hide-date-picker',n_clicks=0, size='sm',style={'padding-letf':'2%'})]), style={
                    'position':'sticky',
                        'top': '1%',
                      'padding-bottom': '0%',
                      'padding-left': '2%',
                      'padding-right': '2%',
                      'display': 'inline-block',
                      'z-index':'4'},
            
        ),
        html.Br(),
        html.Br(),
        html.Div(
            [
                html.H3('Gráficos de Comparações Entre Regiões Com Números Absolutos',),
                dcc.Markdown("""Esses gráficos visam facilitar a visualização das diferenças entre regiões levando em consideração o
                        número absoluto de infectados e mortos."""),
                html.H5('Selecione uma métrica:'),
                html.Div([
                    dcc.Dropdown(
                        id='metric-select-region',
                        options=[{'label': StackedAreas.metrics[item], 'value': item} for item in StackedAreas.metrics],
                        value='casosAcumulado'
                    ),
                ], style={ 'display': 'inline'}),
                
                html.Div([dcc.Graph(id='stacked-areas')], style={'display': 'true','padding': '0'}),
                html.Div(children = dcc.RangeSlider(
                        id='date-slider-stacked-charts',
                        updatemode = 'mouseup', #don't let it update till mouse released
                        min = unix_timestamp_millis(daterange.min()),
                        max = unix_timestamp_millis(daterange.max()),
                        value = [unix_timestamp_millis(daterange.min()),
                                unix_timestamp_millis(daterange.max())],
                        marks=get_marks_from_start_end(daterange.min(),
                            daterange.max())), 
                        id='date-slider-stacked-charts-div', style={ 'display': 'inline', 'padding': '0 20', "align-content": "center"})
            
            ], style={ 'display': 'inline-block', 'padding-bottom': '5%'}),
        
            html.Div(
            [
                html.Div(
                [
                    html.H3('Gráficos de Comparações Entre Estados Com Métricas',),
                    dcc.Markdown("""Esses gráficos visam facilitar a visualização das diferenças entre estados e regiões, tentando reduzir a distorção causada
                    pela diferença populacional entre estados."""),
                    html.H5('Selecione uma métrica:'),
                    dcc.Dropdown(
                        id='metric-select',
                        options=[{'label': SmallMultiples.metrics[item], 'value': item} for item in SmallMultiples.metrics],
                        value='casosPorCemMilHab'
                    ),
                    
                    html.Div([
                        dcc.Graph(id='small-multiples'),
                    ], style={ 'display': 'inline-block'}),

                    html.Div(children = dcc.RangeSlider(
                        id='date-slider-small-multiples',
                        updatemode = 'mouseup', #don't let it update till mouse released
                        min = unix_timestamp_millis(daterange.min()),
                        max = unix_timestamp_millis(daterange.max()),
                        value = [unix_timestamp_millis(daterange.min()),
                                unix_timestamp_millis(daterange.max())],
                        
                        marks=get_marks_from_start_end(daterange.min(), daterange.max())
                    
                    ), id='date-slider-small-multiples-div'),
                    html.Br(),
                    html.Br(),
                ], style={ 'display': 'inline-block'})
                
            ]),
            html.Footer([html.H6("""Aplicação desenvolvida como trabalho final da Disciplina Visualização de Dados do Departamento de Ciência da Computação da Universidade Federal de Minas Gerais"""),
                                html.H6('Autores: Daniel Miranda e Giovanni Martinelli')], style={'padding-top': '1%',
                                'left': '0','bottom': '4%',  'width': '100%',  'text-align': 'left', 'border-top': '1px solid'})
        ], style={'padding': '0% 20%' })])

# Callback to update sliders
@app.callback(
    [dash.dependencies.Output(component_id='date-slider-stacked-charts-div', component_property='children'),
     dash.dependencies.Output(component_id='date-slider-small-multiples-div', component_property='children')],
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])    
def update_slider(start_date, end_date):
    start_datetime = datetime.strptime(start_date[:10], "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date[:10], "%Y-%m-%d")
    start_date_unix_first_slider = unix_timestamp_millis(start_datetime)
    end_date_unix_first_slider = unix_timestamp_millis(end_datetime)

    # We generate new sliders when we change the date because we can just change its values
    date_slider_stacked_charts = dcc.RangeSlider(
                        id='date-slider-stacked-charts',
                        updatemode = 'mouseup', #don't let it update till mouse released
                        min = unix_timestamp_millis(daterange.min()),
                        max = unix_timestamp_millis(daterange.max()),
                        value = [start_date_unix_first_slider,
                                end_date_unix_first_slider],
                        
                        marks=get_marks_from_start_end(daterange.min(),
                            daterange.max()))
    
    date_slider_small_multiples = dcc.RangeSlider(
                        id='date-slider-small-multiples',
                        updatemode = 'mouseup', #don't let it update till mouse released
                        min = unix_timestamp_millis(daterange.min()),
                        max = unix_timestamp_millis(daterange.max()),
                        value = [start_date_unix_first_slider,
                                end_date_unix_first_slider],
                        
                        marks=get_marks_from_start_end(daterange.min(),
                            daterange.max()))

    return date_slider_stacked_charts, date_slider_small_multiples

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
    first_slider_days = [get_day_from_timestamp(unix_ts) for unix_ts in first_slider_range_tuple]
    second_slider_days = [get_day_from_timestamp(unix_ts) for unix_ts in second_slider_range_tuple]
    
    # Get last slider values if they exist
    if last_values:
        last_values_tmp = []
        for unix_ts_tuple in last_values:
            for date in unix_ts_tuple:
                # We convert back from string (if we use a dcc.Store datetime turns into string)
                last_values_tmp.append(datetime.strptime(date, "%Y-%m-%d").date())
        last_values = [(last_values_tmp[0], last_values_tmp[1]), (last_values_tmp[2], last_values_tmp[3])]

    # Now we check which slider change and update the value for date picker accordingly
    
    if last_values == None:
        last_values = (first_slider_days, second_slider_days)
        return first_slider_days[0], first_slider_days[1], last_values

    if second_slider_days[0] != last_values[1][0] or second_slider_days[1] != last_values[1][1]:
        # Second slider changed
        last_values = (second_slider_days, second_slider_days)
        return second_slider_days[0], second_slider_days[1], last_values

    if first_slider_days[0] != last_values[0][0] or first_slider_days[1] != last_values[0][1]:
        # First slider changed
        last_values = (first_slider_days, first_slider_days)
        return first_slider_days[0], first_slider_days[1], last_values

@app.callback(
   dash.dependencies.Output(component_id='date-picker-div', component_property='style'),
   [dash.dependencies.Input(component_id='hide-date-picker', component_property='n_clicks')])
def show_hide_element(clicked):
    if clicked%2 == 0:
        return {'display': 'block'}
    if clicked%2 == 1:
        return {'display': 'none'}

@app.callback(
   dash.dependencies.Output(component_id='hide-date-picker', component_property='children'),
   [dash.dependencies.Input(component_id='hide-date-picker', component_property='n_clicks')])
def show_hide_element(clicked):
    if clicked%2 == 0:
        return 'Esconder'
    if clicked%2 == 1:
        return 'Calendário'
if __name__ == '__main__':
    app.run_server(debug=True)