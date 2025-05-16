import streamlit as st
import pandas as pd
from utils.data_cleaning import handle_missing_data
from utils.labels import get_label

def display_missing_data_options(data):
    st.header(get_label("handle_missing_data"))
    
    # Display missing data information
    missing_info = data.isnull().sum()
    st.write(get_label("missing_values_count"))
    st.write(missing_info[missing_info > 0])
    
    # Options for handling missing data
    option = st.selectbox(get_label("choose_option_missing"), 
                           [get_label("drop_rows"), get_label("impute_values"), get_label("flag_missing")])
    
    fill_value = None
    if option == get_label("impute_values"):
        fill_value = st.text_input(get_label("enter_value_impute"))
    if st.button(get_label("apply")):
        cleaned_data = None
        if option == get_label("drop_rows"):
            cleaned_data = data.dropna()
            st.success(get_label("dropped_rows"))
        elif option == get_label("impute_values"):
            if fill_value:
                cleaned_data = data.fillna(fill_value)
                st.success(get_label("imputed_values").format(value=fill_value))
            else:
                st.error(get_label("please_enter_value"))
        elif option == get_label("flag_missing"):
            cleaned_data = data.copy()
            cleaned_data['missing_flag'] = cleaned_data.isnull().any(axis=1)
            st.success(get_label("flagged_missing"))
        if cleaned_data is not None:
            st.session_state.data = cleaned_data
            st.write(get_label("cleaned_data"))
            st.dataframe(cleaned_data)

def handle_missing_data():
    if st.session_state.data is not None:
        display_missing_data_options(st.session_state.data)
    else:
        st.warning(get_label("please_upload"))