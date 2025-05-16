import streamlit as st
import pandas as pd
import numpy as np
import re
from utils.labels import get_label

def clean_unstructured_data(df):
    """
    Cleans unstructured data by applying various text processing techniques.
    
    Parameters:
    df (DataFrame): The input DataFrame containing unstructured data.
    
    Returns:
    DataFrame: The cleaned DataFrame.
    """
    # Example cleaning steps
    for column in df.columns:
        if df[column].dtype == 'object':
            # Remove leading and trailing whitespace
            df[column] = df[column].str.strip()
            # Convert to lowercase
            df[column] = df[column].str.lower()
            # Remove special characters
            df[column] = df[column].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
            # Replace multiple spaces with a single space
            df[column] = df[column].str.replace(r'\s+', ' ', regex=True)
    
    return df

def display_unstructured_data_cleaning(df):
    """
    Displays the unstructured data cleaning interface in Streamlit.
    
    Parameters:
    df (DataFrame): The input DataFrame containing unstructured data.
    """
    st.header(get_label("unstructured_data_cleaning"))
    
    if st.button(get_label("clean_data_btn")):
        cleaned_df = clean_unstructured_data(df)
        st.success(get_label("data_cleaned_success"))
        st.dataframe(cleaned_df)
        
        # Optionally, provide a download link for the cleaned data
        import base64
        csv = cleaned_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # Convert to base64
        href = f'<a href="data:file/csv;base64,{b64}" download="cleaned_data.csv">{get_label("download_cleaned_data")}</a>'
        st.markdown(href, unsafe_allow_html=True)