import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils.labels import get_label

def correct_errors(df):
    """
    Function to correct errors in the data.
    This includes identifying outliers and impossible values.
    """
    # Example: Identify and replace outliers in a numeric column
    for column in df.select_dtypes(include=[np.number]).columns:
        if df[column].isnull().any():
            continue  # Skip if there are missing values
        
        # Calculate the z-scores
        z_scores = (df[column] - df[column].mean()) / df[column].std()
        
        # Identify outliers
        outliers = df[np.abs(z_scores) > 3]
        
        # Replace outliers with the median
        median_value = df[column].median()
        df[column] = np.where(np.abs(z_scores) > 3, median_value, df[column])
        
        # Log the cleaning step
        st.session_state.cleaning_history.append({
            "action": get_label("corrected_outliers_action").format(column=column, median=median_value),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Add to cleaning report
        st.session_state.cleaning_report["cleaning_steps"].append({
            "action": get_label("corrected_outliers_report").format(column=column),
            "method": get_label("replaced_with_median"),
            "outliers_count": len(outliers),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    st.success(get_label("errors_corrected"))
    return df

def check_for_impossible_values(df):
    """
    Check for impossible values in the data based on column names and types.
    """
    issues_found = False
    
    # Check age columns for impossible values
    age_columns = [col for col in df.columns if 'age' in col.lower()]
    for col in age_columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # Check for negative ages or extremely high ages
            if (df[col] < 0).any() or (df[col] > 120).any():
                issues_found = True
                st.warning(get_label("impossible_age").format(col=col))
    
    # Check percentage columns for values outside 0-100
    pct_columns = [col for col in df.columns if any(x in col.lower() for x in ['percent', 'pct', '%'])]
    for col in pct_columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            if (df[col] < 0).any() or (df[col] > 100).any():
                issues_found = True
                st.warning(get_label("impossible_pct").format(col=col))
    
    return issues_found

def display_error_correction_options(df):
    """
    Function to display options for error correction in the Streamlit app.
    """
    st.header(get_label("error_correction"))
    
    # Check for potential data issues
    st.subheader(get_label("data_issues_detection"))
    issues_found = check_for_impossible_values(df)
    
    if not issues_found:
        st.success(get_label("no_obvious_issues"))
    
    # Options for different error corrections
    st.subheader(get_label("correct_data_errors"))
    
    option = st.selectbox(
        get_label("select_correction_method"),
        [get_label("correct_outliers"), get_label("fix_negative_values"), get_label("cap_percentile")]
    )
    
    if option == get_label("correct_outliers"):
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) == 0:
            st.warning(get_label("no_numeric_outlier"))
        else:
            selected_cols = st.multiselect(get_label("select_columns_outliers"), numeric_cols)
            z_threshold = st.slider(get_label("zscore_threshold"), 2.0, 5.0, 3.0, 0.1)
            
            if selected_cols and st.button(get_label("detect_fix_outliers")):
                modified_df = df.copy()
                outliers_found = False
                
                for col in selected_cols:
                    # Calculate z-scores
                    z_scores = np.abs((modified_df[col] - modified_df[col].mean()) / modified_df[col].std())
                    outlier_mask = z_scores > z_threshold
                    outlier_count = outlier_mask.sum()
                    
                    if outlier_count > 0:
                        outliers_found = True
                        st.write(get_label("found_outliers").format(count=outlier_count, col=col))
                        
                        # Replace outliers with median
                        median_val = modified_df[col].median()
                        modified_df.loc[outlier_mask, col] = median_val
                        
                        # Add to history
                        st.session_state.cleaning_history.append({
                            "action": get_label("replaced_outliers_action").format(count=outlier_count, col=col, median=median_val),
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                
                if outliers_found:
                    st.session_state.data = modified_df
                    st.success(get_label("outliers_replaced"))
                else:
                    st.info(get_label("no_outliers_found"))
    
    elif option == get_label("fix_negative_values"):
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) == 0:
            st.warning(get_label("no_numeric_columns"))
        else:
            selected_cols = st.multiselect(get_label("select_columns_negative"), numeric_cols)
            fix_method = st.radio(get_label("how_fix_negative"), [get_label("set_zero"), get_label("set_abs"), get_label("remove_rows")])
            
            if selected_cols and st.button(get_label("fix_negative_values")):
                modified_df = df.copy()
                negative_found = False
                
                for col in selected_cols:
                    negative_mask = modified_df[col] < 0
                    negative_count = negative_mask.sum()
                    
                    if negative_count > 0:
                        negative_found = True
                        
                        if fix_method == get_label("set_zero"):
                            modified_df.loc[negative_mask, col] = 0
                            action = get_label("set_negative_zero").format(count=negative_count, col=col)
                        
                        elif fix_method == get_label("set_abs"):
                            modified_df.loc[negative_mask, col] = modified_df.loc[negative_mask, col].abs()
                            action = get_label("set_negative_abs").format(count=negative_count, col=col)
                        
                        elif fix_method == get_label("remove_rows"):
                            modified_df = modified_df[~negative_mask]
                            action = get_label("removed_negative_rows").format(count=negative_count, col=col)
                        
                        st.session_state.cleaning_history.append({
                            "action": action,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                
                if negative_found:
                    st.session_state.data = modified_df
                    st.success(get_label("negative_fixed"))
                else:
                    st.info(get_label("no_negative_found"))
    
    elif option == get_label("cap_percentile"):
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) == 0:
            st.warning(get_label("no_numeric_columns"))
        else:
            selected_cols = st.multiselect(get_label("select_columns_cap"), numeric_cols)
            lower_percentile = st.slider(get_label("lower_percentile"), 0, 10, 5)
            upper_percentile = st.slider(get_label("upper_percentile"), 90, 100, 95)
            
            if selected_cols and st.button(get_label("cap_values")):
                modified_df = df.copy()
                caps_applied = False
                
                for col in selected_cols:
                    lower_bound = modified_df[col].quantile(lower_percentile/100)
                    upper_bound = modified_df[col].quantile(upper_percentile/100)
                    
                    # Count values outside bounds
                    below_count = (modified_df[col] < lower_bound).sum()
                    above_count = (modified_df[col] > upper_bound).sum()
                    
                    if below_count > 0 or above_count > 0:
                        caps_applied = True
                        
                        # Cap the values
                        modified_df[col] = modified_df[col].clip(lower=lower_bound, upper=upper_bound)
                        
                        # Add to history
                        action = get_label("capped_values").format(col=col, lower=lower_percentile, upper=upper_percentile)
                        if below_count > 0:
                            action += get_label("below_limit").format(count=below_count)
                        if above_count > 0:
                            action += get_label("above_limit").format(count=above_count)
                            
                        st.session_state.cleaning_history.append({
                            "action": action,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                
                if caps_applied:
                    st.session_state.data = modified_df
                    st.success(get_label("values_capped"))
                else:
                    st.info(get_label("no_values_outside"))
    
    # Button to apply general error correction
    if st.button(get_label("apply_general_error_correction")):
        st.session_state.data = correct_errors(df)
        st.success(get_label("general_error_applied"))

# This function can be called from the main app to integrate error correction functionality.