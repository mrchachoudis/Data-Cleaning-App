import pandas as pd
import numpy as np
from utils.labels import get_label

def fix_date_format(df, column_name, date_format="%Y-%m-%d"):
    """Fix inconsistent date formats in a specified column."""
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce').dt.strftime(date_format)
    return df

def fix_phone_numbers(df, column_name):
    """Standardize phone numbers to a consistent format."""
    df[column_name] = df[column_name].replace(r'\D', '', regex=True)  # Remove non-digit characters
    df[column_name] = df[column_name].apply(lambda x: f"+1-{x[:3]}-{x[3:6]}-{x[6:]}" if len(x) == 10 else x)
    return df

def fix_currency_format(df, column_name):
    """Standardize currency formats in a specified column."""
    df[column_name] = df[column_name].replace(r'[\$,]', '', regex=True).astype(float)
    return df

def fix_inconsistent_formats(df, column_name, format_type):
    """Apply specific format fixing based on the type."""
    if format_type == 'date':
        return fix_date_format(df, column_name)
    elif format_type == 'phone':
        return fix_phone_numbers(df, column_name)
    elif format_type == 'currency':
        return fix_currency_format(df, column_name)
    else:
        raise ValueError(get_label("unsupported_format_type"))