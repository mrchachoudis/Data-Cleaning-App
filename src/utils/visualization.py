import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_missing_data(df):
    """Visualizes the missing data in the DataFrame."""
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
    plt.title('Missing Data Visualization')
    plt.xlabel('Columns')
    plt.ylabel('Rows')
    plt.show()

def plot_duplicates(df):
    """Visualizes the number of duplicates in the DataFrame."""
    duplicate_count = df.duplicated().sum()
    plt.figure(figsize=(6, 4))
    plt.bar(['Duplicates', 'Unique'], [duplicate_count, len(df) - duplicate_count], color=['red', 'green'])
    plt.title('Duplicate Records')
    plt.ylabel('Count')
    plt.show()

def plot_before_after_comparison(original_df, cleaned_df):
    """Plots a comparison of the original and cleaned DataFrames."""
    original_shape = original_df.shape
    cleaned_shape = cleaned_df.shape
    
    plt.figure(figsize=(8, 5))
    plt.bar(['Original Rows', 'Cleaned Rows'], [original_shape[0], cleaned_shape[0]], color=['blue', 'orange'])
    plt.title('Before and After Data Cleaning')
    plt.ylabel('Number of Rows')
    plt.show()

def plot_data_distribution(df, column):
    """Plots the distribution of a specified column in the DataFrame."""
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column], bins=30, kde=True)
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()