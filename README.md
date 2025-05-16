# Data Cleaner Application

## Overview
The Data Cleaner Application is a Streamlit-based tool designed to facilitate the cleaning and preprocessing of CSV data files. Users can upload their datasets and perform various data cleaning operations, ensuring their data is ready for analysis.

## Features
- **Upload CSV Files**: Users can easily upload their CSV files for processing.
- **Data Cleaning Operations**:
  - Handling Missing Data: Options to drop, impute, or flag missing values.
  - Removing Duplicates: Identify and remove duplicate entries with options for exact and fuzzy matching.
  - Fixing Inconsistent Formats: Standardize formats for dates, phone numbers, and currencies.
  - Standardizing Categorical Data: Correct typos and inconsistencies in categorical variables.
  - Error Correction: Identify and correct outliers and impossible values.
  - Text Parsing: Split full names, extract keywords, and more.
  - Type Conversion: Convert data types, such as strings to dates or numbers.
  - Merging/Splitting Columns: Combine or separate columns as needed.
  - Handling Noisy Data: Remove irrelevant characters and extra spaces.
  - Reshaping Data: Pivot, melt, or transpose data for better analysis.
  - Cleaning Unstructured Data: Process and clean scraped or unstructured datasets.
  
## Documentation
Each cleaning step is documented for reproducibility, allowing users to track the changes made to their datasets.

## Installation
To set up the project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/mrchachoudis/Data-Cleaning-App
pip install -r requirements.txt
```

## Usage
To run the application, execute the following command:

```bash
# This command assumes src/ is at the root
streamlit run src/app.py 
```

Once the application is running, navigate to the web interface to upload your CSV file and start cleaning your data.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.

## Project Motivation
This project was created as part of my data analyst portfolio to demonstrate my skills in data cleaning and preprocessing. Working with real-world data often requires significant cleaning before analysis can begin, and I wanted to build a tool that makes this process more efficient and user-friendly.

## Technologies Used
- Python
- Streamlit
- Pandas
- Numpy
- Scikit-learn
- Matplotlib
- Seaborn
- NLTK
- FuzzyWuzzy
- Python-Levenshtein
- Openpyxl

## Screenshots
[Coming soon - Screenshots of the application in action]

## Future Enhancements
- Support for additional file formats (Excel, JSON, Parquet)
- Advanced visualization options for data exploration
- Ability to save and load cleaning workflows
- Custom validation rules for different data types
