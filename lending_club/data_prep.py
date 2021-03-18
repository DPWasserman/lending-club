import dask.dataframe as dd
import pandas as pd

import sys
sys.path.append('../lending_club')
import config

def get_lending_club_data(data_location: str = config.APPROVED_LOANS_CSV):
       extension = data_location.split('.')[-1]
       if extension == 'csv':
              accepted_loans = dd.read_csv(data_location,
                                    dtype={'desc': 'object', 
                                           'id': 'object',
                                           'sec_app_earliest_cr_line': 'object'}, 
                                    parse_dates = ['issue_d',],
                                    low_memory=False)
       elif extension == 'parquet':
              accepted_loans = dd.read_parquet(data_location,
                                               engine='fastparquet')
       else:
              raise ValueError('Bad extension! Please try another file type.')
       return accepted_loans

def split_file_by_year(df):
       df = df.dropna(subset=['issue_d'])
       df['Year'] = df.issue_d.dt.year
       for year in df.Year.unique():
              year_excerpt_df = df.loc[df.Year==year,:]
              #filename = config.DATAPATH / f'accepted_{year}.csv'
              #year_excerpt_df.to_csv(filename, index=False)
              filename = config.DATAPATH / f'accepted-{year}.parquet'
              year_excerpt_df.to_parquet(filename, engine='fastparquet')