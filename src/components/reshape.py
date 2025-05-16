import streamlit as st
import pandas as pd
from utils.labels import get_label
from datetime import datetime

def reshape_data(df):
    """
    Reshape data using pivot, melt or transpose operations.
    
    Args:
        df (pd.DataFrame): The input DataFrame to reshape
    """
    st.header(get_label("reshape_data"))
    
    if df is not None:
        operation = st.selectbox(get_label("select_reshape_operation"), [
            get_label("pivot"), 
            get_label("melt"), 
            get_label("transpose")
        ])
        
        if operation == get_label("pivot"):
            index_col = st.selectbox(get_label("select_index_column"), df.columns.tolist())
            columns_col = st.selectbox(get_label("select_columns_column"), df.columns.tolist())
            values_col = st.selectbox(get_label("select_values_column"), df.columns.tolist())
            
            if st.button(get_label("pivot_data")):
                try:
                    # Perform pivot operation
                    pivoted_df = df.pivot(index=index_col, columns=columns_col, values=values_col)
                    st.session_state.data = pivoted_df.reset_index()
                    
                    # Add to cleaning history
                    st.session_state.cleaning_history.append({
                        "action": f"Pivoted data using {index_col} as index, {columns_col} as columns, and {values_col} as values",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    st.success(get_label("data_pivoted"))
                    st.write(st.session_state.data.head())
                except Exception as e:
                    st.error(f"Error during pivot operation: {str(e)}")
        
        elif operation == get_label("melt"):
            id_vars = st.multiselect(get_label("select_id_vars"), df.columns.tolist())
            value_vars = st.multiselect(get_label("select_value_vars"), df.columns.tolist())
            
            if st.button(get_label("melt_data")):
                try:
                    # Check if at least one id variable is selected
                    if not id_vars:
                        st.warning("Please select at least one identifier variable.")
                        return
                    
                    # Perform melt operation
                    melted_df = pd.melt(df, id_vars=id_vars, value_vars=value_vars if value_vars else None)
                    st.session_state.data = melted_df
                    
                    # Add to cleaning history
                    st.session_state.cleaning_history.append({
                        "action": f"Melted data using {', '.join(id_vars)} as identifier variables",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    st.success(get_label("data_melted"))
                    st.write(st.session_state.data.head())
                except Exception as e:
                    st.error(f"Error during melt operation: {str(e)}")
        
        elif operation == get_label("transpose"):
            if st.button(get_label("transpose_data")):
                try:
                    # Perform transpose operation
                    transposed_df = df.transpose()
                    st.session_state.data = transposed_df
                    
                    # Add to cleaning history
                    st.session_state.cleaning_history.append({
                        "action": "Transposed data",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    st.success(get_label("data_transposed"))
                    st.write(st.session_state.data.head())
                except Exception as e:
                    st.error(f"Error during transpose operation: {str(e)}")
    else:
        st.warning(get_label("please_upload_reshape"))