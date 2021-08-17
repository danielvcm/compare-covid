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

from src.time_utils import unix_timestamp_millis, get_marks_from_start_end, daterange
from datetime import datetime


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

server = app.server


app.layout = html.Div(
    [
    html.Div(children=[
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
        html.H5('Selecione um período:'),
        html.Div(
            dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=datetime(2020, 2, 25),
            max_date_allowed=datetime(2021, 6, 30),
            initial_visible_month=datetime(2020, 8, 9),
            start_date=datetime(2020, 8, 9),
            end_date=datetime(2020, 8, 15)
            ), style={'padding-top': '1%',
                      'padding-bottom': '5%',
                      'padding-left': '2%' }
        )
        ], style={'padding': '0% 20%', }),
    html.Div(
        [
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
                html.Div(
                [
                    dcc.RangeSlider(
                        id='date-slider',
                        updatemode = 'mouseup', #don't let it update till mouse released
                        min = unix_timestamp_millis(daterange.min()),
                        max = unix_timestamp_millis(daterange.max()),
                        value = [unix_timestamp_millis(daterange.min()),
                                unix_timestamp_millis(daterange.max())],
                        marks=get_marks_from_start_end(daterange.min(),
                                                    daterange.max()))
                ], style={ 'display': 'inline', 'padding': '0 20', "align-content": "center"})
            
            ], style={ 'display': 'inline-block'}),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
        
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

                    html.Div([
                        dcc.RangeSlider(
                        id='date-slider_2',
                        updatemode = 'mouseup', #don't let it update till mouse released
                        min = unix_timestamp_millis(daterange.min()),
                        max = unix_timestamp_millis(daterange.max()),
                        value = [unix_timestamp_millis(daterange.min()),
                                unix_timestamp_millis(daterange.max())],
                        marks=get_marks_from_start_end(daterange.min(),
                                                        daterange.max())),
                    ]),
                ], style={ 'display': 'inline-block'})
            ])
        ], style={'padding': '0% 20%' })])

@app.callback(
        dash.dependencies.Output('small-multiples', 'figure'),
        [dash.dependencies.Input('date-slider', 'value'),
         dash.dependencies.Input('metric-select', 'value')]
    )
def update_small_multiples(selected_date_tuple, metric):
    start_date = datetime.fromtimestamp(selected_date_tuple[0])
    end_date = datetime.fromtimestamp(selected_date_tuple[1])
    small_multiples = SmallMultiples(start_date, end_date)
    fig = small_multiples.make_plot(metric)
    return fig

@app.callback(
        dash.dependencies.Output('stacked-areas', 'figure'),
        [dash.dependencies.Input('date-slider', 'value'),
         dash.dependencies.Input('metric-select-region', 'value')]
    )
def update_stacked_areas(selected_date_tuple, metric):
    start_date = datetime.fromtimestamp(selected_date_tuple[0])
    end_date = datetime.fromtimestamp(selected_date_tuple[1])

    stacked_areas = StackedAreas(start_date, end_date)
    fig = stacked_areas.make_plot(metric)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)