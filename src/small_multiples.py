from plotly.subplots import make_subplots
import plotly.graph_objects as go
from .parse_data import ParseData
import plotly.express as px
class SmallMultiples:
    REGIONS = ["Norte", "Sudeste","Nordeste", "Sul", "Centro-Oeste"]
    COLORS = ['#636EFA', '#EF553B', '#AB63FA', '#00CC96', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

    
    metrics = {"óbitosPorCasos": 'Porcentagem de óbitos por casos', "casosPorCemMilHab":'Casos por 100 mil habitantes', "óbitosPorCemMilHab":'Óbitos por 100 mil habitantes' }
    def __init__(self, start_date, end_date) -> None:
        parse_data = ParseData(start_date, end_date)
        self.complete_df = parse_data.generate_states_results()

    def get_coordinates(self, regiao):
        if regiao =="Norte":
            return 1, 1
        if regiao == "Sudeste":
            return 2, 2
        if regiao == "Nordeste":
            return 1, 2
        if regiao == "Centro-Oeste":
            return 2, 1
        if regiao == "Sul":
            return 3, 1
        else:
            return None, None
    
    def add_subplot_region(self, specifications):
        df_region = self.df_states[self.df_states['região'] == specifications['region']]
        self.fig.add_trace(go.Bar(name=specifications['region'], x=df_region['UF'], y=df_region[specifications['y']]),row=specifications['row'], col=specifications['col'])

    def make_plot(self, metric):
        df_br = self.complete_df[self.complete_df['UF']=='Brasil']
        self.df_states = self.complete_df[self.complete_df['UF']!='Brasil']
        self.fig = make_subplots(rows=3, cols=2)
        specifications = {'y': metric}
        for item in self.REGIONS:
            specifications['region'] = item
            specifications['row'], specifications['col'] = self.get_coordinates(item)
            self.add_subplot_region(specifications)
        hovertext = '{:0,.2f}'.format(df_br[metric].iloc[0])
        max_value = self.df_states[metric].max()
        self.fig.add_hline(y=df_br[metric].iloc[0],annotation_text = "Brasil", annotation_hovertext=hovertext)
        self.fig.update_yaxes(range=[0,max_value+(5*max_value/100)])
        self.fig.update_layout(height=900, width=700, title_text=self.metrics[metric],colorway=self.COLORS)
        return self.fig