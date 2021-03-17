import dask.dataframe as dd
import pandas as pd

import sys
sys.path.append('../lending_club')
import config

def get_lending_club_data(data_location: str = config.APPROVED_LOANS_CSV):
    accepted_loans = dd.read_csv(data_location, 
                       dtype={'desc': 'object',
                              'id': 'object',
                              'sec_app_earliest_cr_line': 'object'}, 
                       low_memory=False)
    return accepted_loans