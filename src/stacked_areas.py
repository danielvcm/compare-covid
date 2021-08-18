from .parse_data import ParseData
import plotly.express as px
from .small_multiples import SmallMultiples
class StackedAreas:
    metrics = {'casosAcumulado': "Casos Acumulados",
               'obitosAcumulado': "Óbitos Acumulados"}
    
    def __init__(self, start_date, end_date) -> None:
        parse_data = ParseData(start_date, end_date)
        self.complete_df = parse_data.generate_regions_results()
    
    def make_plot(self, metric):
        fig = px.area(self.complete_df, x="data", y=metric, 
              color="regiao", line_group="estado",
              title=self.metrics[metric], 
              labels = {'data': "Data", metric: self.metrics[metric]},
              color_discrete_sequence=SmallMultiples.COLORS)
        fig.update_layout(height=700)
        return fig