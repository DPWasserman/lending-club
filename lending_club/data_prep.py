import dask.dataframe as dd
import numpy as np
import pandas as pd

import sys
sys.path.append('../lending_club')
import config

def get_lending_club_data(data_location = config.APPROVED_LOANS_CSV, clean_file: bool = True):
       extension = str(data_location).split('.')[-1]
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
       if clean_file:
              accepted_loans = clean(accepted_loans)
       return accepted_loans

def clean(df):
       df = df.dropna(subset=['issue_d']) # If there is no issue date, this is not a "good" record
       df['id'] = df['id'].astype(int)
       df = df.set_index('id')
       df = df.loc[df['grade'].isin(['A','B','C','D','E']),:] # Remove grades in F or G
       return df

def create_features(df):
       df['annual_inc_total'] = df['annual_inc_joint'].fillna(df['annual_inc'])
       return df

def split_file_by_year(df):
       df['Year'] = df.issue_d.dt.year
       for year in df.Year.unique():
              year_excerpt_df = df.loc[df.Year==year,:]
              filename = config.DATAPATH / f'accepted-{year}.parquet'
              year_excerpt_df.to_parquet(filename, engine='fastparquet')