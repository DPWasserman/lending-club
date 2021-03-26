import os
from pathlib import Path

DATAPATH = Path('..') / 'data'
if not os.path.exists(DATAPATH):
    os.mkdir(DATAPATH)

APPROVED_LOANS_CSV = DATAPATH / 'accepted_2007_to_2018Q4.csv'

if not os.path.exists(APPROVED_LOANS_CSV):
    raise OSError(f'{APPROVED_LOANS_CSV} does not exist! Please place in the data directory.')

# These are the features that need to be parsed as dates
DATE_FEATURES = ['earliest_cr_line','issue_d','last_pymnt_d',]

# These are the features to be extracted from the original data file
RAW_FEATURES = ['id',
                'addr_state', # Need to dummify
                'annual_inc',
                'application_type', # Need to binarize 
                'disbursement_method', # Need to binarize
                'dti',
                'earliest_cr_line',
                'emp_length', # Need to convert to number and add NAs
                'emp_title', # Needs to be encoded
                'fico_range_high', # Used to derive the average
                'fico_range_low', # Used to derive the average
                'grade', # Need to dummify or be ordinal encoded
                'home_ownership', # Need to dummify
                'initial_list_status', # Need to dummify (binarize)
                'inq_last_6mths',
                'installment',
                'int_rate',
                'issue_d',
                'last_pymnt_d',
                'loan_amnt',
                'loan_status',
                'open_acc', 
                'pub_rec', 
                'pub_rec_bankruptcies',
                'purpose', # Need to dummify
                'sub_grade', # Need to dummify or be ordinal encoded
                'term', # Need to convert to integer from string
                'total_pymnt',
                'verification_status',
                'zip_code' # Need to dummify
            ]

# These are the features for modeling purposes
SELECTED_FEATURES = [#'id', Identification feature (Index)
                     'addr_state', # Need to dummify
                     'annual_inc',
                     'application_type', # Need to binarize 
                     'days_since_first_credit', # Derived field
                     'disbursement_method', # Need to binarize
                     'dti',
                     #'earliest_cr_line', Used to derive days_since_first_credit
                     'emp_length', # Need to convert to number and add NAs
                     'emp_title', # Needs to be encoded
                     'fico_score_average', # Derived field
                     #'fico_range_high', # Used to derive the average
                     #'fico_range_low', # Used to derive the average
                     #'grade', # Need to dummify or be ordinal encoded
                     'home_ownership', # Need to dummify
                     'initial_list_status', # Need to dummify (binarize)
                     'installment',
                     'int_rate',
                     'issue_d',
                     'loan_amnt',
                     'open_acc', 
                     'pub_rec', 
                     'pub_rec_bankruptcies',
                     'purpose', # Need to dummify
                     'sub_grade', # Need to dummify or be ordinal encoded
                     'term', # Need to convert to integer from string
                     'verification_status',
                     'zip_code' # Need to dummify
                    ]

# This is the target column to be predicted
TARGET_COL = 'loan_status' # Only look at Fully Paid/Charged Off

# These variables need to be dummified
VARS_TO_DUMMIFY = [ #'addr_state', # Removed since zip_code is more granular
                    'application_type',
                    'disbursement_method', 
                    #'emp_title', # Removed because of the high variety
                    #'grade', # Removed since sub_grade is considered
                    'home_ownership', 
                    'initial_list_status', 
                    'purpose',  
                    'verification_status',
                    'zip_code'
                    ]