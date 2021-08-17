import time
import pandas as pd

from dateutil.relativedelta import relativedelta
from datetime import datetime

DATE_START_DEFAULT = datetime(2020, 2, 25)
DATE_END_DEFAULT = datetime(2021, 6, 30)

daterange = pd.date_range(start = DATE_START_DEFAULT,
                          end   = DATE_END_DEFAULT,
                          freq  = 'MS', # Using frequency of months
                          closed= None
                        )

# Utility functions to make graph slider work with datetime object
def unix_timestamp_millis(dt):
    ''' Convert datetime to unix timestamp '''
    return int(time.mktime(dt.timetuple()))

def unix_to_datetime(unix):
    ''' Convert unix timestamp to datetime. '''
    return pd.to_datetime(unix, unit='s')

def get_marks_from_start_end(start, end):
    ''' Returns dict with one item per month
    {1440080188.1900003: '2015-08',
    '''
    result = []
    current = start
    while current <= end:
        result.append(current)
        current += relativedelta(months=1)
    return {unix_timestamp_millis(m):(str(m.strftime('%d/%m/%Y'))) for m in result}