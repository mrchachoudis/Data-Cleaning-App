def validate_dataframe(df):
    """Validate the DataFrame to ensure it meets certain criteria."""
    if df is None or df.empty:
        raise ValueError("DataFrame is empty or not loaded.")
    
    # Check for required columns (example: 'id' and 'name')
    required_columns = ['id', 'name']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Check for duplicate rows
    if df.duplicated().any():
        raise ValueError("DataFrame contains duplicate rows.")

    # Check for missing values
    if df.isnull().values.any():
        raise ValueError("DataFrame contains missing values.")

    return True

def validate_column_types(df, expected_types):
    """Validate the data types of the DataFrame columns."""
    for column, expected_type in expected_types.items():
        if column in df.columns:
            actual_type = df[column].dtype
            if actual_type != expected_type:
                raise TypeError(f"Column '{column}' expected type '{expected_type}', but got '{actual_type}'.")

def validate_data_cleaning_steps(cleaning_steps):
    """Validate the cleaning steps to ensure they are documented correctly."""
    if not isinstance(cleaning_steps, list):
        raise ValueError("Cleaning steps should be a list.")
    
    for step in cleaning_steps:
        if not isinstance(step, dict) or 'action' not in step:
            raise ValueError("Each cleaning step must be a dictionary with an 'action' key.")

    return True