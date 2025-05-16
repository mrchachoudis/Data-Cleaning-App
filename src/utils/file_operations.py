import pandas as pd
import os
import json
import base64
from io import StringIO

def read_csv_file(uploaded_file):
    """
    Reads an uploaded CSV file into a pandas DataFrame.

    Args:
        uploaded_file: The file object from a Streamlit file uploader.
                       Expected to have a .read() method or be directly readable by pandas.read_csv().

    Returns:
        pd.DataFrame: The DataFrame created from the CSV file.

    Raises:
        Exception: If there is an error reading or parsing the CSV file.
    """
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        raise Exception(f"Error reading CSV file: {str(e)}")

def read_csv(file_path):
    """Read a CSV file and return a DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    return pd.read_csv(file_path)

def write_csv(dataframe, file_path):
    """Write a DataFrame to a CSV file."""
    dataframe.to_csv(file_path, index=False)

def generate_csv_download_link(df: pd.DataFrame, filename: str = "cleaned_data.csv", button_text: str = "Download CSV File") -> str:
    """
    Generates an HTML download link for a pandas DataFrame to be saved as a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to be downloaded.
        filename (str, optional): The desired name for the downloaded CSV file. 
                                  Defaults to "cleaned_data.csv".
        button_text (str, optional): The text to display on the download button/link.
                                     Defaults to "Download CSV File".

    Returns:
        str: An HTML string representing the download link.
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{button_text}</a>'
    return href

def save_cleaning_report(report, file_path):
    """Save the cleaning report as a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(report, f)

def load_cleaning_report(file_path):
    """Load a cleaning report from a JSON file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The report file {file_path} does not exist.")
    with open(file_path, 'r') as f:
        return json.load(f)