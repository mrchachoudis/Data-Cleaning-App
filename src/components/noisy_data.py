import pandas as pd
import re
from utils.labels import get_label

def remove_noisy_data(df, text_columns):
    """
    Remove noisy data from specified text columns in the DataFrame.
    
    Parameters:
    df (pd.DataFrame): The DataFrame from which to remove noisy data.
    text_columns (list): List of column names that contain text data to be cleaned.
    
    Returns:
    pd.DataFrame: The cleaned DataFrame with noisy data removed.
    """
    for column in text_columns:
        if column in df.columns:
            # Remove extra spaces
            df[column] = df[column].str.strip()
            # Remove irrelevant characters (e.g., special characters)
            df[column] = df[column].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x) if isinstance(x, str) else x)
            # Remove duplicate spaces
            df[column] = df[column].str.replace(r'\s+', ' ', regex=True)
    
    return df

def handle_noisy_data(df, text_columns):
    """
    Handle noisy data by providing options to the user for cleaning text columns.
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the data to be cleaned.
    text_columns (list): List of text columns to clean.
    
    Returns:
    pd.DataFrame: The cleaned DataFrame after handling noisy data.
    """
    cleaned_df = remove_noisy_data(df, text_columns)
    # Optionally, you could add a message here if you want to show feedback in the UI
    # For example: st.success(get_label("noisy_data_cleaned"))
    return cleaned_df