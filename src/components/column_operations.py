import streamlit as st
import pandas as pd
from utils.labels import get_label

def merge_columns(df, column1, column2, new_column, separator=' '):
    """
    Merge two columns into a new column with a specified separator.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the columns to merge
        column1 (str): The name of the first column to merge
        column2 (str): The name of the second column to merge
        new_column (str): The name of the new merged column
        separator (str): The separator to use between values (default is space)
    
    Returns:
        pd.DataFrame: The DataFrame with the new merged column
    """
    if column1 not in df.columns or column2 not in df.columns:
        raise ValueError(get_label('columns_not_exist').format(col1=column1, col2=column2))
    
    result_df = df.copy()
    # Convert columns to string before merging
    result_df[column1] = result_df[column1].astype(str)
    result_df[column2] = result_df[column2].astype(str)
    result_df[new_column] = result_df[column1] + separator + result_df[column2]
    
    return result_df

def split_column(df, column, new_column1, new_column2, separator=' '):
    """
    Split a column into two new columns based on a separator.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the column to split
        column (str): The name of the column to split
        new_column1 (str): The name of the first new column
        new_column2 (str): The name of the second new column
        separator (str): The separator to split on (default is space)
    
    Returns:
        pd.DataFrame: The DataFrame with the column split into two new columns
    """
    result_df = df.copy()
    result_df[[new_column1, new_column2]] = result_df[column].str.split(separator, n=1, expand=True)
    
    return result_df

def display_column_operations(df):
    """Display interface for column operations"""
    st.header(get_label("column_operations"))
    
    operation = st.selectbox(get_label("select_operation"), [
        get_label("merge_columns"),
        get_label("split_column")
    ])
    
    if operation == get_label("merge_columns"):
        col1 = st.selectbox(get_label("select_first_column_merge"), df.columns)
        col2 = st.selectbox(get_label("select_second_column_merge"), df.columns)
        new_col = st.text_input(get_label("enter_new_column_name"))
        separator = st.text_input(get_label("enter_separator"), " ")
        
        if st.button(get_label("merge")):
            try:
                st.session_state.data = merge_columns(df, col1, col2, new_col, separator)
                st.success(get_label("columns_merged").format(col1=col1, col2=col2, new_col=new_col))
                
                # Add to cleaning history
                from datetime import datetime
                st.session_state.cleaning_history.append({
                    "action": get_label("columns_merged").format(col1=col1, col2=col2, new_col=new_col),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            except Exception as e:
                st.error(str(e))
    
    elif operation == get_label("split_column"):
        col = st.selectbox(get_label("select_column_split"), df.select_dtypes(include=['object']).columns)
        new_col1 = st.text_input(get_label("enter_new_col1_name"))
        new_col2 = st.text_input(get_label("enter_new_col2_name"))
        separator = st.text_input(get_label("enter_separator"), " ")
        
        if st.button(get_label("split")):
            try:
                st.session_state.data = split_column(df, col, new_col1, new_col2, separator)
                st.success(get_label("column_split").format(col=col, new_col1=new_col1, new_col2=new_col2))
                
                # Add to cleaning history
                from datetime import datetime
                st.session_state.cleaning_history.append({
                    "action": get_label("column_split").format(col=col, new_col1=new_col1, new_col2=new_col2),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            except Exception as e:
                st.error(str(e))