from src.time_utils import unix_timestamp_millis, get_marks_from_start_end, daterange, get_day_from_timestamp
import dash_core_components as dcc
from datetime import datetime

class DatePicker:
    def __init__(self):
        pass

    @staticmethod
    def update_with_sliders(first_slider_range_tuple, second_slider_range_tuple, last_values):
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
    

class Sliders:
    def __init__(self):
        pass

    @staticmethod
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

class Button:
    def __init__(self):
        pass
    @staticmethod
    def show_hide_date_picker(clicked):
        if clicked%2 == 0:
            return {'display': 'block'}
        if clicked%2 == 1:
            return {'display': 'none'}
    
    @staticmethod
    def update_button_text(clicked):
        if clicked%2 == 0:
            return 'Esconder'
        if clicked%2 == 1:
            return 'Calendário'
