import dask.dataframe as dd
import numpy as np
import pandas as pd

import sys
sys.path.append('../lending_club')
import config

def get_lending_club_data(data_location = config.APPROVED_LOANS_CSV, clean_file: bool = True, filename_to_save: str = None):
       """
       Reads file into memory as a dataframe. 
       Will optionally clean the file.txt
       Will optionally save back to disk in the data folder as a parquet file
       """
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
       if filename_to_save:
              accepted_loans.to_parquet(config.DATAPATH / filename_to_save, engine='fastparquet')
       return accepted_loans

def clean(df):
       """Performs cleaning on the raw dataset"""
       df = df.dropna(subset=['issue_d']) # If there is no issue date, this is not a "good" record
       df['id'] = df['id'].astype(int)
       df = df.set_index('id')
       df = df.loc[df['grade'].isin(['A','B','C','D','E']),:] # Remove grades in F or G
       return df

def create_features(df):
       """Creates features on the raw dataset"""
       df['annual_inc_total'] = df['annual_inc_joint'].fillna(df['annual_inc'])
       return df

def split_file_by_year(df):
       """Takes the dataframe and breaks it up by year into parquet files"""
       df['Year'] = df.issue_d.dt.year
       for year in df.Year.unique():
              year_excerpt_df = df.loc[df.Year==year,:]
              filename = config.DATAPATH / f'accepted-{year}.parquet'
              year_excerpt_df.to_parquet(filename, engine='fastparquet')