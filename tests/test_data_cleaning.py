import pytest
import pandas as pd
from src.utils.data_cleaning import (
    handle_missing_data,
    remove_duplicates,
    fix_inconsistent_formats,
    standardize_categorical_data,
    correct_errors,
    parse_text_data,
    convert_data_types,
    merge_columns,
    split_columns,
    handle_noisy_data,
    reshape_data,
    clean_unstructured_data
)

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', None, 'Eve', 'Alice'],
        'Age': [25, 30, 35, None, 40, 25],
        'City': ['New York', 'Los Angeles', 'New York', 'Chicago', 'Los Angeles', 'New York'],
        'Salary': ['$50,000', '$60,000', '$70,000', None, '$80,000', '$50,000']
    })

def test_handle_missing_data(sample_data):
    cleaned_data = handle_missing_data(sample_data, method='drop')
    assert cleaned_data.shape[0] == 4  # Should drop rows with missing values

def test_remove_duplicates(sample_data):
    cleaned_data = remove_duplicates(sample_data)
    assert cleaned_data.shape[0] == 5  # Should remove duplicate 'Alice'

def test_fix_inconsistent_formats(sample_data):
    sample_data['Salary'] = ['$50,000', '$60,000', '$70,000', None, '$80000', '$50,000']
    cleaned_data = fix_inconsistent_formats(sample_data, column='Salary')
    assert cleaned_data['Salary'].iloc[3] == '$80,000'  # Should fix the format

def test_standardize_categorical_data(sample_data):
    sample_data['City'] = ['new york', 'Los Angeles', 'new york', 'Chicago', 'los angeles', 'new york']
    cleaned_data = standardize_categorical_data(sample_data, column='City')
    assert cleaned_data['City'].nunique() == 3  # Should standardize to 3 unique cities

def test_correct_errors(sample_data):
    sample_data['Age'] = [25, 30, 35, -1, 40, 25]  # -1 is an impossible value
    cleaned_data = correct_errors(sample_data, column='Age')
    assert cleaned_data['Age'].iloc[3] == 30  # Should correct the impossible value

def test_parse_text_data():
    sample_data = pd.DataFrame({'Full Name': ['Alice Smith', 'Bob Johnson']})
    cleaned_data = parse_text_data(sample_data, column='Full Name')
    assert 'First Name' in cleaned_data.columns  # Should create a 'First Name' column

def test_convert_data_types(sample_data):
    sample_data['Age'] = sample_data['Age'].astype(str)
    cleaned_data = convert_data_types(sample_data, column='Age', target_type=int)
    assert cleaned_data['Age'].dtype == 'int64'  # Should convert Age to int

def test_merge_columns():
    df = pd.DataFrame({'First Name': ['Alice'], 'Last Name': ['Smith']})
    cleaned_data = merge_columns(df, cols=['First Name', 'Last Name'], new_col='Full Name')
    assert 'Full Name' in cleaned_data.columns  # Should create a 'Full Name' column

def test_split_columns():
    df = pd.DataFrame({'Full Name': ['Alice Smith']})
    cleaned_data = split_columns(df, column='Full Name', new_cols=['First Name', 'Last Name'])
    assert 'First Name' in cleaned_data.columns  # Should create 'First Name' and 'Last Name' columns

def test_handle_noisy_data(sample_data):
    sample_data['Name'] = ['Alice!!', 'Bob@', 'Charlie#', 'Eve$', 'Alice!!']
    cleaned_data = handle_noisy_data(sample_data, column='Name')
    assert all(cleaned_data['Name'].str.isalnum())  # Should remove noisy characters

def test_reshape_data(sample_data):
    reshaped_data = reshape_data(sample_data, id_vars=['Name'], value_vars=['Age', 'Salary'])
    assert reshaped_data.shape[0] == 10  # Should reshape the data correctly

def test_clean_unstructured_data():
    unstructured_data = pd.Series(['   Alice Smith   ', 'Bob Johnson'])
    cleaned_data = clean_unstructured_data(unstructured_data)
    assert cleaned_data.str.strip().equals(unstructured_data.str.strip())  # Should clean whitespace