import streamlit as st
import pandas as pd
from utils.labels import get_label

# Pre-check if thefuzz is available
try:
    from thefuzz import process
    THEFUZZ_AVAILABLE = True
except ImportError:
    THEFUZZ_AVAILABLE = False

def remove_duplicates(data):
    if data is not None:
        st.subheader(get_label("remove_duplicates"))
        
        # Option to remove exact duplicates
        if st.checkbox(get_label("remove_exact_duplicates")):
            original_shape = data.shape
            data = data.drop_duplicates()
            st.success(get_label("removed_exact_duplicates").format(count=original_shape[0] - data.shape[0]))
        
        # Option for fuzzy matching duplicates
        if st.checkbox(get_label("remove_fuzzy_duplicates")):
            try:
                from thefuzz import process
                
                column_to_check = st.selectbox(get_label("select_column_fuzzy"), data.columns)
                threshold = st.slider(get_label("set_similarity_threshold"), 0, 100, 90)
                
                # Convert unique values to strings and skip NaN
                unique_values = data[column_to_check].unique()
                unique_values_str = [str(x) for x in unique_values if not pd.isna(x)]
                duplicates = []
                
                for value in unique_values_str:
                    matches = process.extract(value, unique_values_str, limit=None)
                    similar_values = [match[0] for match in matches if match[1] >= threshold and match[0] != value]
                    duplicates.extend(similar_values)
                
                duplicates = set(duplicates)
                original_shape = data.shape
                # Compare as strings
                data = data[~data[column_to_check].astype(str).isin(duplicates)]
                st.success(get_label("removed_fuzzy_duplicates").format(count=original_shape[0] - data.shape[0]))
            except ImportError:
                st.warning(get_label("fuzzy_required"))
                return None
        
        return data
    else:
        st.warning(get_label("no_data_remove_duplicates"))