import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import config

def divide_by_term(df, term_length:int):
    latest_year = 2018 - (term_length // 12)
    print(latest_year)
    termed_df = df[df['term']==term_length]
    print(f'df shape: {termed_df.shape}')
    termed_df['Year'] = termed_df.issue_d.dt.year
    termed_df = termed_df[termed_df['Year']<=latest_year]
    print(f'df shape: {termed_df.shape}')
    return termed_df

def split_data(df, target_col=config.TARGET_COL, test_size=0.3, random_state=None):
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    return train_test_split(X, y, test_size=0.3, random_state=random_state)