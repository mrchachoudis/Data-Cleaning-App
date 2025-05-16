import pandas as pd
import re
import streamlit as st
from datetime import datetime
from utils.labels import get_label

def split_full_name(df, full_name_column):
    """Split a full name column into first name and last name"""
    if full_name_column not in df.columns:
        st.error(f"Column '{full_name_column}' not found.")
        return df
    
    # Create a copy of the dataframe
    result_df = df.copy()
    
    # Split the full name into first and last name
    result_df[[get_label("first_name_col"), get_label("last_name_col")]] = df[full_name_column].str.split(' ', n=1, expand=True)
    
    # Add to cleaning history
    st.session_state.cleaning_history.append({
        "action": get_label("split_full_names_action").format(col=full_name_column),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    return result_df

def extract_keywords(df, text_column, keywords):
    """Extracts specified keywords from a given text column."""
    if text_column not in df.columns:
        raise ValueError(get_label("column_not_exist").format(column=text_column))
    
    # Create a new column to store extracted keywords
    df[f"{text_column}_keywords"] = df[text_column].apply(
        lambda text: ','.join([kw for kw in keywords if isinstance(text, str) and re.search(r'\\b' + re.escape(kw) + r'\\b', text, re.IGNORECASE)])
    )
    
    # Add to cleaning history
    st.session_state.cleaning_history.append({
        "action": get_label("extracted_keywords_action").format(col=text_column),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    return df

def clean_text_column(df, text_column):
    """Cleans a text column by removing unwanted characters and extra spaces."""
    if text_column not in df.columns:
        raise ValueError(get_label("column_not_exist").format(column=text_column))
    
    # Clean the text
    df[text_column] = df[text_column].astype(str).str.replace(r'[\w\s]', '', regex=True).str.strip()
    
    # Add to cleaning history
    st.session_state.cleaning_history.append({
        "action": get_label("cleaned_text_action").format(col=text_column),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    return df

def parse_dates(df, date_column, format='%Y-%m-%d'):
    """Parses a date column into datetime format."""
    if date_column not in df.columns:
        raise ValueError(get_label("column_not_exist").format(column=date_column))
    
    # Convert to datetime
    df[date_column] = pd.to_datetime(df[date_column], format=format, errors='coerce')
    
    # Add to cleaning history
    st.session_state.cleaning_history.append({
        "action": get_label("parsed_dates_action").format(col=date_column, fmt=format),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    return df

def parse_text_data(df):
    """Display interface for text parsing options"""
    st.header(get_label("text_parsing"))
    
    option = st.selectbox(get_label("select_parsing_option"), [
        get_label("split_full_names"),
        get_label("extract_keywords"),
        get_label("clean_text_column"),
        get_label("parse_dates")
    ])
    
    if option == get_label("split_full_names"):
        # Select column containing full names
        text_columns = df.select_dtypes(include=['object']).columns.tolist()
        if not text_columns:
            st.error(get_label("no_text_columns"))
            return df
        
        full_name_col = st.selectbox(get_label("select_column_full_names"), text_columns)
        
        if st.button(get_label("split_names")):
            try:
                df = split_full_name(df, full_name_col)
                st.success(get_label("split_names_success").format(col=full_name_col))
            except Exception as e:
                st.error(get_label("error_generic").format(error=str(e)))
    
    elif option == get_label("extract_keywords"):
        # Select text column and keywords to extract
        text_columns = df.select_dtypes(include=['object']).columns.tolist()
        if not text_columns:
            st.error(get_label("no_text_columns"))
            return df
        
        text_col = st.selectbox(get_label("select_text_column"), text_columns)
        keywords = st.text_input(get_label("enter_keywords")).split(',')
        
        if st.button(get_label("extract_keywords_btn")) and keywords:
            try:
                df = extract_keywords(df, text_col, [k.strip() for k in keywords if k.strip()])
                st.success(get_label("extract_keywords_success").format(col=text_col))
            except Exception as e:
                st.error(get_label("error_generic").format(error=str(e)))
    
    elif option == get_label("clean_text_column"):
        # Select text column to clean
        text_columns = df.select_dtypes(include=['object']).columns.tolist()
        if not text_columns:
            st.error(get_label("no_text_columns"))
            return df
        
        text_col = st.selectbox(get_label("select_text_column_clean"), text_columns)
        
        if st.button(get_label("clean_text_btn")):
            try:
                df = clean_text_column(df, text_col)
                st.success(get_label("clean_text_success").format(col=text_col))
            except Exception as e:
                st.error(get_label("error_generic").format(error=str(e)))
    
    elif option == get_label("parse_dates"):
        # Select column with dates and format
        columns = df.columns.tolist()
        date_col = st.selectbox(get_label("select_column_dates"), columns)
        
        date_format = st.selectbox(get_label("select_date_format"), [
            "%Y-%m-%d",  # 2023-01-31
            "%m/%d/%Y",  # 01/31/2023
            "%d/%m/%Y",  # 31/01/2023
            "%B %d, %Y", # January 31, 2023
            "%d-%b-%Y",  # 31-Jan-2023
            get_label("custom")
        ])
        
        if date_format == get_label("custom"):
            date_format = st.text_input(get_label("enter_custom_date_format"))
        
        if st.button(get_label("parse_dates_btn")) and date_format:
            try:
                df = parse_dates(df, date_col, date_format)
                st.success(get_label("parse_dates_success").format(col=date_col))
            except Exception as e:
                st.error(get_label("error_generic").format(error=str(e)))
    
    return df