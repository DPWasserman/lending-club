import dask.array as da
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
                                    parse_dates = config.DATE_FEATURES,
                                    low_memory=False)
       elif extension == 'parquet':
              accepted_loans = dd.read_parquet(data_location,
                                               engine='fastparquet')
       elif extension == 'pickle':
              accepted_loans = pd.read_pickle(data_location)
       else:
              raise ValueError('Bad extension! Please try another file type.')

       if clean_file:
              accepted_loans = accepted_loans.loc[:, config.RAW_FEATURES]
              accepted_loans = clean(accepted_loans)
       
       if filename_to_save:
              save_extension = str(filename_to_save).split('.')[-1]
              if save_extension == 'parquet':
                     accepted_loans.to_parquet(config.DATAPATH / filename_to_save, engine='fastparquet')
              elif save_extension == 'csv':
                     accepted_loans.to_csv(config.DATAPATH / filename_to_save)
              else:
                     raise ValueError('Bad extension! Please try another file type for saving.')
       return accepted_loans

def clean(df):
       """Performs cleaning on the raw dataset"""
       df = df.dropna(subset=['issue_d', # If there is no issue date, this is not a "good" record
                              'annual_inc',
                              'dti',
                              'open_acc',
                              'pub_rec',
                              'pub_rec_bankruptcies',
                              'term'
                              ]) 
       df['id'] = df['id'].astype(int)
       df = df.set_index('id')
       df = df.loc[df['grade'].isin(['A','B','C','D','E']),:] # Remove grades in F or G
       df = df.loc[df['loan_status'].isin(['Charged Off','Fully Paid']),:] # Remove loans that have not finalized
       df = df[df.annual_inc < 2e7] # Remove outliers
       df['emp_length'] = df['emp_length'].fillna('-1 years (N/A)') # Impute -1 years when no employee length is given
       return df

def refine_features(df):
       """Creates features on the processed Pandas dataset"""
       if pd.api.types.is_string_dtype(df['term']):
              df['term'] = df.term.astype(str).str.extract('(\d+)').astype(int)
       if pd.api.types.is_string_dtype(df['emp_length']):
              df['emp_length'] = np.where(df['emp_length'].str.find('<')>-1, # <1 Years = 0 
                                          '0 years',
                                          df['emp_length'])
              df['emp_length'] = df['emp_length'].str.extract('([-]?\d+)')
              df['emp_length'] = df['emp_length'].astype(int)
       if pd.api.types.is_string_dtype(df.loan_status):
              df['loan_status'] = np.where(df['loan_status']=='Charged Off',0, 1) # Charged Off = 0; Fully Paid = 1
       if pd.api.types.is_string_dtype(df.sub_grade):
              df['sub_grade'] = df['sub_grade'].replace({'A1':1,'A2':2,'A3':3,'A4':4,'A5':5,
                                                         'B1':6,'B2':7,'B3':8,'B4':9,'B5':10,
                                                         'C1':11,'C2':12,'C3':13,'C4':14,'C5':15,
                                                         'D1':16,'D2':17,'D3':18,'D4':19,'D5':20,
                                                         'E1':21,'E2':22,'E3':23,'E4':24,'E5':25})
              df['sub_grade'] = df['sub_grade'].astype(int)
       df['days_since_first_credit'] = (df.issue_d - df.earliest_cr_line).dt.days
       df['fico_score_average'] = (df['fico_range_high'] + df['fico_range_low'])/2
       df['PnL'] = df['total_pymnt'] - df['loan_amnt'] # Simple profit (Note: Time dimension is ignored)
       return df

def split_file_by_year(df):
       """Takes the dataframe and breaks it up by year into parquet files"""
       df['Year'] = df.issue_d.dt.year
       for year in df.Year.unique():
              year_excerpt_df = df.loc[df.Year==year,:]
              filename = config.DATAPATH / f'accepted-{year}.parquet'
              year_excerpt_df.to_parquet(filename, engine='fastparquet')

def make_binary(df):
       """Convert columns to binary"""
       X = df['application_type'].to_dask_array()
       df['application_type_indiv']= da.where(x =='Individual',1,0)
       y = df['disbursement_method'].to_dask_array()
       df['disbursement_method_cash']= da.where(y =='Cash',1,0)
       df = df.drop(['application_type','disbursement_method'], axis=1)
       return df

