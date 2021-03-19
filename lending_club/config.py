import os
from pathlib import Path

DATAPATH = Path('..') / 'data'
if not os.path.exists(DATAPATH):
    os.mkdir(DATAPATH)

APPROVED_LOANS_CSV = DATAPATH / 'accepted_2007_to_2018Q4.csv'

if not os.path.exists(APPROVED_LOANS_CSV):
    raise OSError(f'{APPROVED_LOANS_CSV} does not exist! Please place in the data directory.')

SELECTED_FEATURES = [  

                    ]