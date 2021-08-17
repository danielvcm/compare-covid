# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
from dash_core_components.Markdown import Markdown
import dash_html_components as html
from dash_html_components.Div import Div
import plotly.express as px
from src.small_multiples import SmallMultiples
from src.stacked_areas import StackedAreas
from datetime import datetime
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.Div(children=[
        html.H1(children='Compare Covid'),
        dcc.Markdown("""Nosso projeto permite a comparação de infecções e óbitos por COVID-19 nos diferentes estados e
                    regiões do Brasil. Os dados utilizados nesta aplicação são fornecidos pelo Governo Federal no site
                    [Coronavirus Brasil](https://covid.saude.gov.br/)."""),
        dcc.Markdown("""Temos dois tipos de visualizações, uma para dados absolutos e outra para métricas que tentam normalizar
                    os dados para que não haja uma distorção entre estados com muito e pouco populosos. Para ambas, deve-se primeiro
                    selecionar um período no tempo no qual os dados serão extraídos. Sugerimos escolher ao menos uma semana, para
                    que alterações no fluxo de envios de relatórios por parte das secretarias de saúde não distorçam os gráficos."""),
        html.H5('Selecione um período:'),
        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=datetime(2020, 2, 25),
            max_date_allowed=datetime(2021, 6, 30),
            initial_visible_month=datetime(2020, 8, 9),
            start_date=datetime(2020, 8, 9),
            end_date=datetime(2020, 8, 15)
        )],style={'padding': '3% 5%'}),
    html.Div(
        [html.Div([html.H4('Gráficos de Comparações Entre Regiões Com Números Absolutos',),
            dcc.Markdown("""Esses gráficos visam facilitar a visualização das diferenças entre regiões levando em consideração o
                        número absoluto de infectados e mortos."""),
            html.H5('Selecione uma métrica:'),
            dcc.Dropdown(
                        id='metric-select-region',
                        options=[{'label': StackedAreas.metrics[item], 'value': item} for item in StackedAreas.metrics],
                        value='casosAcumulado'
                    ),
            html.Div([dcc.Graph(id='stacked-areas'
                        )],style={ 'display': 'inline', 'padding': '0 20'})],
                        style={ 'display': 'inline-block'}),
        html.Div([html.Div([html.H4('Gráficos de Comparações Entre Estados Com Métricas',),
                dcc.Markdown("""Esses gráficos visam facilitar a visualização das diferenças entre estados e regiões, tentando reduzir a distorção causada
                pela diferença populacional entre estados."""),
                html.H5('Selecione uma métrica:'),
                dcc.Dropdown(
                    id='metric-select',
                    options=[{'label': SmallMultiples.metrics[item], 'value': item} for item in SmallMultiples.metrics],
                    value='casosPorCemMilHab'
                ),
                html.Div([dcc.Graph(
                    id='small-multiples'
            )],style={ 'display': 'inline-block','padding': '0 20'})],
        style={ 'display': 'inline-block'})
        ])],style={'padding': '0% 5%' })])

@app.callback(
    dash.dependencies.Output('small-multiples', 'figure'),
    [dash.dependencies.Input('date-picker', 'start_date'),
    dash.dependencies.Input('date-picker', 'end_date'),
     dash.dependencies.Input('metric-select', 'value')])
def update_small_multiples(start_date, end_date, metric):
    small_multiples = SmallMultiples(start_date, end_date)
    fig = small_multiples.make_plot(metric)
    return fig

@app.callback(
    dash.dependencies.Output('stacked-areas', 'figure'),
    [dash.dependencies.Input('date-picker', 'start_date'),
    dash.dependencies.Input('date-picker', 'end_date'),
     dash.dependencies.Input('metric-select-region', 'value')])
def update_stacked_areas(start_date, end_date, metric):
    stacked_areas = StackedAreas(start_date, end_date)
    fig = stacked_areas.make_plot(metric)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)