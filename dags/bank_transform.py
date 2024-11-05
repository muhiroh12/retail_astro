import pandas as pd
import numpy as np

def clean_transform_filter(file_path):
    # Load CSV data into DataFrame
    df = pd.read_csv(file_path, sep=',')
    
    # Example cleaning: Drop rows with null values
    df_clean = df.dropna()
    
    # Example transformation: Convert date column to datetime format
    df_clean['job'] = df_clean['job'].str.replace('.','', regex=False)
    df_clean['education'] = df_clean['education'].str.replace('.','-', regex=False)
    df_clean['pdays'] = df_clean['pdays'].replace(999, np.nan)
    
    df_filtered = df_clean[~df_clean.isin(['unknown']).any(axis=1)]
    
    df_filtered['nr.employed'] = df_filtered['nr.employed'].astype(int)
    
    df_filtered.rename(columns={
        'default': 'default_credit',
        'contact': 'contact_target',
        'dt_customer': 'dt_year',
        'emp.var.rate': 'emp_var_rate',
        'cons.price.idx': 'cons_price_idx',
        'cons.conf.idx': 'cons_conf_idx',
        'nr.employed': 'nr_employed',
        'y': 'target_decision'
    }, inplace=True)
    
    # Save cleaned and transformed data to a new CSV
    transformed_file_path = 'include/dataset/bank-additional-full-cleaned.csv'
    df_filtered.to_csv(transformed_file_path, index=False)
    
    # Return the path of the cleaned file for the next task
    return transformed_file_path
