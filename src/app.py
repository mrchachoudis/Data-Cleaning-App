import streamlit as st
import pandas as pd
from datetime import datetime
import os
from utils.file_operations import read_csv_file, generate_csv_download_link
from components.overview import display_data_overview
from components.missing_data import handle_missing_data
from components.duplicates import remove_duplicates
from components.formatting import fix_inconsistent_formats
from components.categorical import standardize_categorical_data
from components.error_correction import correct_errors, display_error_correction_options
from components.text_parsing import parse_text_data
from components.type_conversion import type_conversion
from components.column_operations import display_column_operations
from components.noisy_data import handle_noisy_data
from components.reshape import reshape_data
from components.unstructured_data import clean_unstructured_data
from components.cleaning_history import display_cleaning_history
from utils.labels import get_label

# Set page configuration
st.set_page_config(
    page_title="Data Cleaner App",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_file = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
with open(css_file, "r") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'original_data' not in st.session_state:
    st.session_state.original_data = None
if 'cleaning_history' not in st.session_state:
    st.session_state.cleaning_history = []
if 'file_name' not in st.session_state:
    st.session_state.file_name = ""
if 'cleaning_report' not in st.session_state:
    st.session_state.cleaning_report = {}

# Add language selector at the top right
st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] > div:last-child {
        display: flex;
        justify-content: flex-end;
    }
    </style>
""", unsafe_allow_html=True)

cols = st.columns([1, 0.15])
with cols[1]:
    lang = st.selectbox("", ["English", "Ελληνικά"], key="language_select", label_visibility="collapsed")
    st.session_state["language"] = 'el' if lang == "Ελληνικά" else 'en'

# Function to run the app
def main():
    # Logo and title in branded wrapper
    st.markdown("""
    <div class="logo-title">
        <h1>{}</h1>
    </div>
    """.format(get_label('title')), unsafe_allow_html=True)
    
    # Add descriptive subtitle
    st.markdown(f"<p style='font-size: 1.2rem; margin-bottom: 2rem;'>{get_label('app_description')}</p>", unsafe_allow_html=True)
    
    # Sidebar for file upload and basic information
    with st.sidebar:
        st.markdown(f"<h3>🗂 {get_label('upload')}</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(get_label('choose_file'), type=["csv"])
        
        # Add sidebar separator and info section
        st.markdown("<hr>", unsafe_allow_html=True)
        
        if uploaded_file is not None:
            try:
                st.session_state.file_name = uploaded_file.name
                df = read_csv_file(uploaded_file)
                
                # File info display
                st.markdown(f"<div class='card'><h4>📊 {get_label('file_info')}</h4>", unsafe_allow_html=True)
                st.markdown(f"**{get_label('filename')}:** {uploaded_file.name}", unsafe_allow_html=True)
                st.markdown(f"**{get_label('dimensions')}:** {len(df)} {get_label('rows')}, {len(df.columns)} {get_label('columns')}", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Store the original data
                if st.session_state.data is None or st.session_state.file_name != uploaded_file.name:
                    st.session_state.original_data = df.copy()
                    st.session_state.data = df.copy()
                    
                    # Initialize cleaning report
                    st.session_state.cleaning_report = {
                        "filename": uploaded_file.name,
                        "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "original_rows": len(df),
                        "original_columns": len(df.columns),
                        "cleaning_steps": []
                    }
                    
                    st.success(get_label('success_loaded').format(filename=uploaded_file.name))
                
                # Show reset button if data is loaded
                if st.session_state.data is not None and st.session_state.original_data is not None:
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(get_label('reset'), key="reset_btn", help=get_label('reset_tooltip')):
                            st.session_state.data = st.session_state.original_data.copy()
                            st.session_state.cleaning_history = []
                            st.session_state.cleaning_report["cleaning_steps"] = []
                            st.success(get_label('reset_success'))
                    
                    # Add export options with clear labeling
                    st.markdown(f"<h4>📤 {get_label('export_options')}</h4>", unsafe_allow_html=True)
                    st.markdown(generate_csv_download_link(st.session_state.data, button_text=get_label('download_csv')), unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(get_label('error').format(error=str(e)))
        else:
            # Show welcome message when no file is uploaded
            st.markdown(f"""
            <div class="card">
                <h4>👋 {get_label('welcome')}</h4>
                <p>{get_label('upload_instruction')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Create tabs for different operations
    if st.session_state.data is not None:
        tabs = st.tabs([
            get_label("data_overview"),
            get_label("missing_data"),
            get_label("duplicates"),
            get_label("format_fixing"),
            get_label("categorical_data"),
            get_label("error_correction_tab"),
            get_label("text_parsing_tab"),
            get_label("type_conversion_tab"),
            get_label("column_operations_tab"),
            get_label("noisy_data_tab"),
            get_label("reshape_data_tab"),
            get_label("unstructured_data_tab"),
            get_label("cleaning_history_tab")
        ])
        
        # Tab 1: Data Overview
        with tabs[0]:
            display_data_overview(st.session_state.data)
        
        # Tab 2: Missing Data
        with tabs[1]:
            handle_missing_data()
        
        # Tab 3: Duplicates
        with tabs[2]:
            result = remove_duplicates(st.session_state.data)
            if result is not None:
                st.session_state.data = result
        
        # Tab 4: Format Fixing
        with tabs[3]:
            st.header(get_label("fix_inconsistent_formats"))
            column = st.selectbox(
                get_label("select_column_to_fix_format"), 
                st.session_state.data.columns,
                help=get_label("select_column_to_fix_format_tooltip")
            )
            
            # Define display and canonical values for format types
            format_options_display = [get_label("date"), get_label("phone_number"), get_label("currency")]
            format_options_values = ["date", "phone_number", "currency"]

            selected_display_format = st.selectbox(
                get_label("select_format_type"), 
                format_options_display,
                help=get_label("select_format_type_tooltip")
            )
            
            if st.button(get_label("fix_format_button")):
                try:
                    # Map selected display format back to its canonical value
                    selected_value_format = format_options_values[format_options_display.index(selected_display_format)]
                    
                    # Store the original format type for the history message
                    original_format_label = selected_display_format

                    st.session_state.data = fix_inconsistent_formats(st.session_state.data, column, selected_value_format)
                    
                    # Add to cleaning history
                    st.session_state.cleaning_history.append({
                        "action": get_label("fixed_format_action").format(format_type=original_format_label, column=column),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    st.success(get_label("format_fixed_success").format(column=column))
                except Exception as e:
                    st.error(get_label('error_generic').format(error=str(e)))
        
        # Tab 5: Categorical Data
        with tabs[4]:
            st.header(get_label("categorical_data"))
            column = st.selectbox(get_label("select_categorical_column_to_standardize"), st.session_state.data.select_dtypes(include=['object']).columns)
            
            if st.button(get_label("standardize")):
                try:
                    st.session_state.data = standardize_categorical_data(st.session_state.data, column)
                    
                    # Add to cleaning history
                    st.session_state.cleaning_history.append({
                        "action": f"Standardized categorical data in column '{column}'",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                except Exception as e:
                    st.error(get_label('error_generic').format(error=str(e)))
        
        # Tab 6: Error Correction
        with tabs[5]:
            display_error_correction_options(st.session_state.data)
        
        # Tab 7: Text Parsing
        with tabs[6]:
            st.header(get_label("text_parsing_tab"))
            parse_option = st.selectbox(get_label("select_parsing_option"), [get_label("split_full_names"), get_label("extract_keywords"), get_label("clean_text_column"), get_label("parse_dates")])
            
            if parse_option == get_label("split_full_names"):
                col = st.selectbox(get_label("select_column_full_names"), st.session_state.data.select_dtypes(include=['object']).columns)
                if st.button(get_label("split_names")):
                    try:
                        from components.text_parsing import split_full_name
                        st.session_state.data = split_full_name(st.session_state.data, col)
                        st.success(get_label("split_names_success").format(col=col))
                    except Exception as e:
                        st.error(get_label('error_generic').format(error=str(e)))
            
            elif parse_option == get_label("clean_text_column"):
                col = st.selectbox(get_label("select_text_column_clean"), st.session_state.data.select_dtypes(include=['object']).columns)
                if st.button(get_label("clean_text_btn")):
                    try:
                        from components.text_parsing import clean_text_column
                        st.session_state.data = clean_text_column(st.session_state.data, col)
                        st.success(get_label("clean_text_success").format(col=col))
                    except Exception as e:
                        st.error(get_label('error_generic').format(error=str(e)))
        
        # Tab 8: Type Conversion
        with tabs[7]:
            st.header(get_label("type_conversion_tab"))
            conversion_type = st.selectbox(get_label("select_conversion_type"), [get_label("string_to_number"), get_label("string_to_date"), get_label("number_to_string")])
            
            if conversion_type == get_label("string_to_number"):
                cols = st.multiselect(get_label("select_columns_to_convert_numeric"), st.session_state.data.select_dtypes(include=['object']).columns)
                if st.button(get_label("convert_to_numeric")):
                    conversions = {'numeric': cols}
                    st.session_state.data = type_conversion(st.session_state.data, conversions)
                    st.success(get_label("converted_to_numeric"))
            
            elif conversion_type == get_label("string_to_date"):
                cols = st.multiselect(get_label("select_columns_to_convert_datetime"), st.session_state.data.select_dtypes(include=['object']).columns)
                if st.button(get_label("convert_to_datetime")):
                    conversions = {'datetime': cols}
                    st.session_state.data = type_conversion(st.session_state.data, conversions)
                    st.success(get_label("converted_to_datetime"))
            
            elif conversion_type == get_label("number_to_string"):
                cols = st.multiselect(get_label("select_columns_to_convert_string"), st.session_state.data.select_dtypes(include=['number']).columns)
                if st.button(get_label("convert_to_string")):
                    conversions = {'string': cols}
                    st.session_state.data = type_conversion(st.session_state.data, conversions)
                    st.success(get_label("converted_to_string"))
        
        # Tab 9: Column Operations
        with tabs[8]:
            display_column_operations(st.session_state.data)
        
        # Tab 10: Noisy Data
        with tabs[9]:
            st.header(get_label("noisy_data_tab"))
            text_cols = st.multiselect(get_label("select_text_columns_to_clean"), st.session_state.data.select_dtypes(include=['object']).columns)
            
            if st.button(get_label("remove_noise")):
                if text_cols:
                    st.session_state.data = handle_noisy_data(st.session_state.data, text_cols)
                    st.session_state.cleaning_history.append({
                        "action": get_label("removed_noise_action"),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.success(get_label("noisy_data_cleaned"))
                else:
                    st.warning(get_label("please_select_text_column"))
        
        # Tab 11: Reshape Data
        with tabs[10]:
            reshape_data(st.session_state.data)
        
        # Tab 12: Unstructured Data
        with tabs[11]:
            st.header(get_label("unstructured_data_tab"))
            if st.button(get_label("clean_data_btn")):
                try:
                    st.session_state.data = clean_unstructured_data(st.session_state.data)
                    st.session_state.cleaning_history.append({
                        "action": get_label("cleaned_unstructured_data_action"),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.success(get_label("data_cleaned_success"))
                except Exception as e:
                    st.error(get_label('error_generic').format(error=str(e)))
        
        # Tab 13: Cleaning History
        with tabs[12]:
            display_cleaning_history()
    else:
        # Show landing page content when no file is loaded
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            <div class="card">
                <h2>{get_label('app_features')}</h2>
                <ul>
                    <li>{get_label('feature_overview')}</li>
                    <li>{get_label('feature_missing')}</li>
                    <li>{get_label('feature_duplicates')}</li>
                    <li>{get_label('feature_format')}</li>
                    <li>{get_label('feature_more')}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="card">
                <h2>{get_label('getting_started')}</h2>
                <p>{get_label('getting_started_text')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Add footer
    st.markdown("""
    <footer>
        <p style="font-size: 1.2em; color: #03dac6;">Data Cleaner App © 2025 | Developed by M.C. ❤️ | <a href="https://github.com/mrchachoudis/data-cleaning-app" target="_blank">Link to the app</a></p>
    </footer>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()