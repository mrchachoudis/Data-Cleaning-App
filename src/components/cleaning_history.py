import streamlit as st
import pandas as pd
import json
from datetime import datetime
from utils.file_operations import generate_csv_download_link

def display_cleaning_history():
    """
    Displays the history of cleaning operations and allows exporting the cleaning report
    """
    st.header("Cleaning History")
    
    if not st.session_state.cleaning_history:
        st.info("No cleaning operations have been performed yet.")
        return
    
    # Display cleaning history as a table
    history_df = pd.DataFrame(st.session_state.cleaning_history)
    st.dataframe(history_df)
    
    # Create a cleaning report
    st.subheader("Cleaning Report")
    
    # Display report summary
    df = st.session_state.data
    original_df = st.session_state.original_data
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Original Rows", st.session_state.cleaning_report["original_rows"])
        st.metric("Original Columns", st.session_state.cleaning_report["original_columns"])
    with col2:
        st.metric("Current Rows", len(df))
        st.metric("Current Columns", len(df.columns))
    with col3:
        row_diff = len(df) - st.session_state.cleaning_report["original_rows"]
        col_diff = len(df.columns) - st.session_state.cleaning_report["original_columns"]
        st.metric("Row Difference", row_diff, delta_color="inverse" if row_diff < 0 else "normal")
        st.metric("Column Difference", col_diff, delta_color="inverse" if col_diff < 0 else "normal")
    
    # Option to export cleaning report
    st.subheader("Export Cleaning Report")
    
    # Update report with final statistics
    report = st.session_state.cleaning_report.copy()
    report.update({
        "final_rows": len(df),
        "final_columns": len(df.columns),
        "row_reduction": f"{(1 - len(df)/len(original_df))*100:.2f}%",
        "completion_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    
    # Convert to JSON for display
    report_json = json.dumps(report, indent=2)
    st.code(report_json, language="json")
    
    # Download options
    col1, col2 = st.columns(2)
    with col1:
        # Download report as JSON
        st.download_button(
            label="Download Report (JSON)",
            data=report_json,
            file_name="cleaning_report.json",
            mime="application/json",
        )
    
    with col2:
        # Download cleaned data
        st.markdown(generate_csv_download_link(df, "cleaned_data.csv"), unsafe_allow_html=True)