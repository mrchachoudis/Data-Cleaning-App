import pandas as pd
from utils.labels import get_label

def convert_to_numeric(df, columns):
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    # Optionally, add a message: st.success(get_label('converted_to_numeric'))
    return df

def convert_to_datetime(df, columns):
    for column in columns:
        df[column] = pd.to_datetime(df[column], errors='coerce')
    # Optionally, add a message: st.success(get_label('converted_to_datetime'))
    return df

def convert_to_string(df, columns):
    for column in columns:
        df[column] = df[column].astype(str)
    # Optionally, add a message: st.success(get_label('converted_to_string'))
    return df

def type_conversion(df, conversions):
    if 'numeric' in conversions:
        df = convert_to_numeric(df, conversions['numeric'])
    if 'datetime' in conversions:
        df = convert_to_datetime(df, conversions['datetime'])
    if 'string' in conversions:
        df = convert_to_string(df, conversions['string'])
    return df