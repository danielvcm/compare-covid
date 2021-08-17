from plotly.subplots import make_subplots
import plotly.graph_objects as go
from parse_data import ParseData

class SmallMultiples:
    REGIONS = ["Norte", "Sudeste", "Nordeste", "Centro-Oeste", "Sul"]

    def __init__(self, start_date, end_date) -> None:
        parse_data = ParseData(start_date, end_date)
        self.complete_df = parse_data.generate_states_results()

    def get_coordinates(self, i):
        if i ==0:
            return 1, 1
        if i == 1:
            return 2, 2
        if i == 2:
            return 1, 2
        if i == 3:
            return 2, 1
        if i == 4:
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
        for i in range(len(self.REGIONS)):
            specifications['region'] = self.REGIONS[i]
            specifications['row'], specifications['col'] = self.get_coordinates(i)
            self.add_subplot_region(specifications)
        hovertext = '{:0,.2f}'.format(df_br[metric].iloc[0])
        max_value = self.df_states[metric].max()
        self.fig.add_hline(y=df_br[metric].iloc[0],annotation_text = "Brasil", annotation_hovertext=hovertext)
        self.fig.update_yaxes(range=[0,max_value+(5*max_value/100)])
        self.fig.update_layout(height=800, width=600, title_text=metric)
        return self.fig