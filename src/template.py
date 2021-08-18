import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from .small_multiples import SmallMultiples
from .stacked_areas import StackedAreas

from .time_utils import unix_timestamp_millis, get_marks_from_start_end, daterange
from datetime import datetime

def make_layout():
    return html.Div(
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

        dcc.Markdown("""Para ambas, deve-se primeiro selecionar um período no tempo no qual os dados serão extraídos. O mínimo de escolha é
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
            min_date_allowed=daterange.min(),
            max_date_allowed=daterange.max(),
            initial_visible_month=datetime(2020, 3,1),
            start_date=daterange.min(),
            end_date=daterange.max(),
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