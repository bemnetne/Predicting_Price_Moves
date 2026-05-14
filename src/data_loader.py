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
import nltk

nltk.download('vader_lexicon')

from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()


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

def prepare_dates(news_df, stock_df):

    # convert dates
    news_df['date'] = pd.to_datetime(
        news_df['date'],
        format='mixed',
        errors='coerce',
        utc=True
    )

    stock_df['Date'] = pd.to_datetime(
        stock_df['Date'],
        errors='coerce'
    )

    # remove timezone
    news_df['date'] = (
        news_df['date']
        .dt.tz_localize(None)
    )

    stock_df['Date'] = (
        stock_df['Date']
        .dt.tz_localize(None)
    )

    return news_df, stock_df

import pandas as pd


import pandas as pd


def align_news_and_stock_dates(
    news_df,
    amzn_df,
    meta_df,
    goog_df,
    aapl_df,
    nvda_df,
    news_date_col='date',
    stock_date_col='Date'
):
    """
    Align news dates to the nearest next trading day
    for multiple stock datasets.
    """

    # ==========================================
    # Copy DataFrames
    # ==========================================

    news_df = news_df.copy()

    stock_data = {
        'AAPL': aapl_df.copy(),
        'AMZN': amzn_df.copy(),
        'META': meta_df.copy(),
        'GOOG': goog_df.copy(),
        'NVDA': nvda_df.copy()
    }

    # ==========================================
    # Normalize News Dates
    # ==========================================

    news_df['date_only'] = (
        pd.to_datetime(news_df[news_date_col])
        .dt.normalize()
    )

    news_df = news_df.sort_values(
        'date_only'
    )

    aligned_results = {}

    # ==========================================
    # Align Each Stock Dataset
    # ==========================================

    for ticker, stock_df in stock_data.items():

        # Normalize stock dates
        stock_df[stock_date_col] = (
            pd.to_datetime(stock_df[stock_date_col])
            .dt.normalize()
        )

        # Sort values
        stock_df = stock_df.sort_values(
            stock_date_col
        )

        # Merge nearest next trading day
        aligned_df = pd.merge_asof(
            news_df,
            stock_df,
            left_on='date_only',
            right_on=stock_date_col,
            direction='forward'
        )

        # Rename aligned trading date
        aligned_df.rename(
            columns={
                stock_date_col: 'trading_date'
            },
            inplace=True
        )

        # Store result
        aligned_results[ticker] = aligned_df

    return aligned_results


def prepare_dates_cluster(
    news_df,
    amzn_df,
    meta_df,
    goog_df,
    aapl_df,
    nvda_df
):
    """
    Prepare and normalize date columns
    for news and stock datasets.
    """

    # ==========================================
    # Copy DataFrames
    # ==========================================

    news_df = news_df.copy()

    amzn_df = amzn_df.copy()

    meta_df = meta_df.copy()

    goog_df = goog_df.copy()

    aapl_df = aapl_df.copy()

    nvda_df = nvda_df.copy()

    # ==========================================
    # Convert News Dates
    # ==========================================

    news_df['date'] = pd.to_datetime(
        news_df['date'],
        format='mixed',
        errors='coerce',
        utc=True
    )

    # Remove timezone
    news_df['date'] = (
        news_df['date']
        .dt.tz_localize(None)
    )

    # ==========================================
    # Function to Prepare Stock Dates
    # ==========================================

    def clean_stock_dates(stock_df):

        stock_df['Date'] = pd.to_datetime(
            stock_df['Date'],
            errors='coerce'
        )

        stock_df['Date'] = (
            stock_df['Date']
            .dt.tz_localize(None)
        )

        return stock_df

    # ==========================================
    # Clean All Stock DataFrames
    # ==========================================

    amzn_df = clean_stock_dates(amzn_df)

    meta_df = clean_stock_dates(meta_df)

    goog_df = clean_stock_dates(goog_df)

    aapl_df = clean_stock_dates(aapl_df)

    nvda_df = clean_stock_dates(nvda_df)

    return (
        news_df,
        amzn_df,
        meta_df,
        goog_df,
        aapl_df,
        nvda_df
    )
