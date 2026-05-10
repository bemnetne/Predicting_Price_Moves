import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from scipy import stats
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
from IPython.display import display



def load_data(filepath):
    """Load a stock CSV file and return a clean, date-indexed DataFrame."""
    df = pd.read_csv(filepath)
    # df['date'] = pd.to_datetime(df['date'])
    # df = df.set_index('date')
    # df = df.sort_index()
    # print(f"Loaded {len(df)} rows from '{filepath}'")
    return df


def remove_nulls(df):
    """Remove rows that have any missing values. Print a summary of what was removed."""
    before = len(df)
    display(df.isna().sum())
    df = df.dropna()
    after = len(df)
    removed = before - after
    if removed > 0:
        print(f"Removed {removed} row(s) with missing values. {after} rows remaining.")
    else:
        print(f"No missing values found. All {after} rows kept.")
    return df
def fill_nulls(df):
    """
    Fill missing values using forward fill.
    """

    if df.isnull().values.any():

        missing_count = df.isnull().sum().sum()

        print(
            f"Found {missing_count} missing values. "
            "Filling with forward fill."
        )

        df = df.ffill()

    else:
        print("No missing values found.")

    return df
def show_duplicates(df):
    """Remove rows that have any missing values. Print a summary of what was removed."""
    # dup_count = df.duplicated().sum()
    dup_count = df.duplicated().sum()
    print("Number of duplicate rows:", dup_count)
    duplicates = df[df.duplicated(keep=False)]
    print(duplicates)
    return df

