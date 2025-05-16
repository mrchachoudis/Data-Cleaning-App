import streamlit as st
import pandas as pd
from utils.labels import get_label

def display_data_overview(data: pd.DataFrame):
    """
    Display summary information about the loaded dataset.
    
    Shows statistics, data types, missing values, sample rows and dataset shape.
    
    Args:
        data: DataFrame to analyze
    """
    st.header(get_label("data_overview"))
    
    if data is not None:
        st.subheader(get_label("basic_statistics"))
        st.write(data.describe(include='all'))

        st.subheader(get_label("data_types"))
        st.write(data.dtypes)

        st.subheader(get_label("missing_values"))
        st.write(data.isnull().sum())

        st.subheader(get_label("sample_data"))
        st.write(data.head())

        st.subheader(get_label("shape_of_data"))
        st.write(get_label("rows_cols").format(rows=data.shape[0], cols=data.shape[1]))
    else:
        st.warning(get_label("no_data_display"))