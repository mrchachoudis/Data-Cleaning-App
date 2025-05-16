import pandas as pd
import numpy as np
import re

def handle_missing_data(df, strategy='drop', fill_value=None):
    if strategy == 'drop':
        df_cleaned = df.dropna()
    elif strategy == 'impute':
        df_cleaned = df.fillna(fill_value)
    elif strategy == 'flag':
        df_cleaned = df.copy()
        df_cleaned['missing_flags'] = df.isnull().any(axis=1)
    else:
        raise ValueError("Invalid strategy. Choose 'drop', 'impute', or 'flag'.")
    return df_cleaned

def remove_duplicates(df, subset=None, keep='first'):
    return df.drop_duplicates(subset=subset, keep=keep)

def fix_inconsistent_formats(df, column, format_type='date'):
    if format_type == 'date':
        df[column] = pd.to_datetime(df[column], errors='coerce')
    elif format_type == 'currency':
        df[column] = df[column].replace({'\\$': '', ',': ''}, regex=True).astype(float)
    return df

def standardize_categorical_data(df, column):
    df[column] = df[column].str.lower().str.strip()
    return df

def correct_errors(df, column, error_conditions):
    for condition, correction in error_conditions.items():
        df.loc[df[column] == condition, column] = correction
    return df

def parse_text_data(df, column, separator=' '):
    split_columns = df[column].str.split(separator, expand=True)
    for i in range(split_columns.shape[1]):
        df[f'{column}_{i+1}'] = split_columns[i]
    return df

def convert_data_types(df, column, target_type):
    if target_type == 'int':
        df[column] = df[column].astype(int)
    elif target_type == 'float':
        df[column] = df[column].astype(float)
    elif target_type == 'str':
        df[column] = df[column].astype(str)
    elif target_type == 'datetime':
        df[column] = pd.to_datetime(df[column], errors='coerce')
    return df

def merge_columns(df, new_column_name, columns_to_merge, separator=' '):
    df[new_column_name] = df[columns_to_merge].astype(str).agg(separator.join, axis=1)
    return df

def split_column(df, column, new_column_names, separator=' '):
    split_columns = df[column].str.split(separator, expand=True)
    for i, new_column in enumerate(new_column_names):
        df[new_column] = split_columns[i]
    return df

def handle_noisy_data(df, column):
    df[column] = df[column].str.replace(r'\W+', '', regex=True).str.strip()
    return df

def reshape_data(df, id_vars, value_vars, var_name='variable', value_name='value'):
    return pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)

def clean_unstructured_data(df, column):
    df[column] = df[column].str.replace(r'\s+', ' ', regex=True).str.strip()
    return df