import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_html_components.Div import Div

from .small_multiples import SmallMultiples
from .stacked_areas import StackedAreas

from .time_utils import unix_timestamp_millis, get_marks_from_start_end, daterange
from datetime import datetime

from .interactables import DatePicker, Sliders, Graphs, Dropdowns, Button

class Template:

    def make_layout(self):
        return html.Div(
        [
        self.intro(),
        self.date_picker_card(),
        self.graphs(),
        self.footer()
        ], style={'padding': '0% 20%' }
        )
    
    def intro(self):
        return html.Div(children=[
                dcc.Store(id=Sliders.LastValue.id),
                html.H1(children='Compare Covid', 
                        className="app-header--title",       
                        style=Styles.title
                    ),
                dcc.Markdown(Texts.intro_markdown[0]),
        
                dcc.Markdown(Texts.intro_markdown[1]),

                dcc.Markdown(Texts.intro_markdown[2]),
                html.Br(),
                ])
    
    def date_picker_card(self):
        return dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.H5('Selecione um período:'),
                        dcc.DatePickerRange(
                            id= DatePicker.id,
                            min_date_allowed=daterange.min(),
                            max_date_allowed=daterange.max(),
                            initial_visible_month=datetime(2020, 3,1),
                            start_date=daterange.min(),
                            end_date=daterange.max(),
                            minimum_nights = 7
                        )],id=DatePicker.div_id),
                    dbc.Button('Esconder',id=Button.id,n_clicks=0, size='sm',style=Styles.date_picker_hide_button)]), 
                    style=Styles.date_picker_card,  
            )

    def graphs(self):
        return html.Div(
            [
            html.Br(),
            html.Br(),
            self.stacked_areas(),
            self.small_multiples()
            ])    
    
    def stacked_areas(self):
        return html.Div(
                [
                    html.H3('Gráficos de Comparações Entre Regiões Com Números Absolutos',),
                    dcc.Markdown(Texts.stacked_areas_markdown),
                    html.H5('Selecione uma métrica:'),
                    html.Div([
                        dcc.Dropdown(
                            id=Dropdowns.StackedAreas.id,
                            options=[{'label': StackedAreas.metrics[item], 'value': item} for item in StackedAreas.metrics],
                            value='casosAcumulado'
                        )
                    ]),
                    
                    html.Div([
                        dcc.Graph(id=Graphs.StackedAreas.id)]),
                        html.Div(
                            Sliders.StackedAreas.build(unix_timestamp_millis(daterange.min()),
                                                        unix_timestamp_millis(daterange.max())), 
                            id=Sliders.StackedAreas.div_id)
                ], style=Styles.graphs)
    
    def small_multiples(self):
        return html.Div(
                [
                    html.Div(
                    [
                        html.H3('Gráficos de Comparações Entre Estados Com Métricas',),
                        dcc.Markdown(Texts.small_multiples_markdown),
                        html.H5('Selecione uma métrica:'),
                        dcc.Dropdown(
                            id=Dropdowns.SmallMultiples.id,
                            options=[{'label': SmallMultiples.metrics[item], 'value': item} for item in SmallMultiples.metrics],
                            value='casosPorCemMilHab'
                        ),
                        
                        html.Div([
                            dcc.Graph(id=Graphs.SmallMultiples.id),
                        ]),

                        html.Div(
                            Sliders.SmallMultiples.build(unix_timestamp_millis(daterange.min()),
                                                        unix_timestamp_millis(daterange.max()) 
                        ), id=Sliders.SmallMultiples.div_id),
                        html.Br(),
                        html.Br(),
                    ])
                    
                ], style=Styles.graphs)
    
    def footer(self):
        return html.Footer([html.H6(Texts.footer[0]),
                            html.H6(Texts.footer[1])], 
                            style=Styles.footer)
    

class Texts:
    intro_markdown = [
            """Nosso projeto permite a comparação de infecções e óbitos por COVID-19 nos diferentes estados e
            regiões do Brasil. Os dados utilizados nesta aplicação são fornecidos pelo Governo Federal no site
            [Coronavirus Brasil](https://covid.saude.gov.br/).""",
            """Temos dois tipos de visualizações, uma para dados absolutos e outra para métricas que tentam normalizar
                os dados para que não haja uma distorção entre estados com muito e pouco populosos.""",
            """Para ambas, deve-se primeiro selecionar um período no tempo no qual os dados serão extraídos. O mínimo de escolha é
                ao menos uma semana, para que alterações no fluxo de envios de relatórios por parte das secretarias de saúde não
                distorçam os gráficos."""
        ]
    stacked_areas_markdown = """Esses gráficos visam facilitar a visualização das diferenças entre regiões levando em consideração o
                            número absoluto de infectados e mortos."""
    
    small_multiples_markdown = """Esses gráficos visam facilitar a visualização das diferenças entre estados e regiões, tentando reduzir a distorção causada
                        pela diferença populacional entre estados."""
    
    footer = ["""Aplicação desenvolvida como trabalho final da Disciplina Visualização de Dados do Departamento de Ciência da
                Computação da Universidade Federal de Minas Gerais""",
                'Autores: Daniel Miranda e Giovanni Martinelli']

class Styles:
    title = {
                'textAlign': 'center',
                'padding-top': '5%',
                'padding-bottom': '5%',
                'background': ''
                }
    date_picker_hide_button = {'padding-letf':'2%'}
    date_picker_card = {
                    'position':'sticky',
                    'top': '1%',
                    'padding-bottom': '0%',
                    'padding-left': '2%',
                    'padding-right': '2%',
                    'display': 'inline-block',
                    'z-index':'4'}
    graphs = {'padding-bottom': '5%'}
    footer = {'padding-top': '1%',
            'left': '0',
            'bottom': '4%',
             'width': '100%', 
             'text-align': 'left',
             'border-top': '1px solid'}