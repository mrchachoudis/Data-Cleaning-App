import pandas as pd
import streamlit as st
from utils.labels import get_label

def standardize_categorical_data(df, column_name):
    if column_name not in df.columns:
        st.error(get_label("column_not_exist").format(column=column_name))
        return df

    # Convert to string type for consistency
    df[column_name] = df[column_name].astype(str)

    # Standardize the categorical data
    df[column_name] = df[column_name].str.lower().str.strip()

    # Optionally, you can add more specific standardization rules here
    # For example, fixing common typos
    typos = {
        "male": ["m", "male", "man"],
        "female": ["f", "female", "woman"],
        "other": ["o", "other", "non-binary"]
    }

    for standard, variants in typos.items():
        for variant in variants:
            df[column_name] = df[column_name].replace(variant, standard)

    st.success(get_label("standardized_column").format(column=column_name))
    return df