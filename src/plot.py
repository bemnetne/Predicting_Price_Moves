import matplotlib.pyplot as plt
import pandas as pd

# Plot RSI
# ==========================================

def plot_rsi(df, ticker):

    plt.figure(figsize=(14, 5))

    plt.plot(
        df.index,
        df['RSI'],
        label='RSI'
    )

    plt.axhline(70, linestyle='--')
    plt.axhline(30, linestyle='--')

    plt.title(
        f'{ticker} Relative Strength Index'
    )

    plt.xlabel('Date')
    plt.ylabel('RSI')

    plt.legend()
    plt.grid(True)

    plt.show()
    # Plot MACD
# ==========================================

def plot_macd(df, ticker):

    plt.figure(figsize=(14, 5))

    plt.plot(
        df.index,
        df['MACD'],
        label='MACD'
    )

    plt.plot(
        df.index,
        df['Signal_Line'],
        label='Signal Line'
    )

    plt.title(
        f'{ticker} MACD Indicator'
    )

    plt.xlabel('Date')
    plt.ylabel('Value')

    plt.legend()
    plt.grid(True)

    plt.show()


def plot_bollinger_bands(
    df,
    ticker='AAPL',
    price_column='Close',
    date_column='Date',
    window=20
):

    plt.figure(figsize=(14, 6))

    # Closing Price
    plt.plot(
        df[date_column],
        df[price_column],
        label='Close Price'
    )

    # Middle Band
    plt.plot(
        df[date_column],
        df[f'BB_Middle_{window}'],
        label='Middle Band'
    )

    # Upper Band
    plt.plot(
        df[date_column],
        df[f'BB_Upper_{window}'],
        label='Upper Band'
    )

    # Lower Band
    plt.plot(
        df[date_column],
        df[f'BB_Lower_{window}'],
        label='Lower Band'
    )

    # Fill between bands
    plt.fill_between(
        df[date_column],
        df[f'BB_Lower_{window}'],
        df[f'BB_Upper_{window}'],
        alpha=0.1
    )

    plt.title(
        f'{ticker} Bollinger Bands (Last 2 Years)'
    )

    plt.xlabel('Date')
    plt.ylabel('Price')

    plt.legend()
    plt.grid(True)

    plt.show()

# ==========================================
# Plot Volatility
# ==========================================

def plot_volatility(df, ticker):

    plt.figure(figsize=(14, 5))

    plt.plot(
        df.index,
        df['Volatility']
    )

    plt.title(
        f'{ticker} Rolling Volatility'
    )

    plt.xlabel('Date')
    plt.ylabel('Volatility')

    plt.grid(True)

    plt.show()

# ==========================================
# Filter Last 2 Years
# ==========================================

def filter_last_two_years(
    df,
    date_column='Date'
):
    """
    Filter dataframe to only the latest 2 years.
    """

    # Convert to datetime
    df[date_column] = pd.to_datetime(
        df[date_column]
    )

    # Latest date
    latest_date = df[date_column].max()

    # Start date
    start_date = latest_date - pd.DateOffset(years=2)

    # Filter
    filtered_df = df[
        df[date_column] >= start_date
    ].copy()

    return filtered_df


# ==========================================
# Price Action with SMA and EMA
# ==========================================

def plot_price_with_moving_averages(
    df,
    ticker,
    date_column='Date',
    price_column='Close'
):

    # Filter last 2 years
    df = filter_last_two_years(
        df,
        date_column
    )

    plt.figure(figsize=(14, 6))

    # Close Price
    plt.plot(
        df[date_column],
        df[price_column],
        label='Close Price'
    )

    # SMA
    if 'SMA_20' in df.columns:
        plt.plot(
            df[date_column],
            df['SMA_20'],
            label='SMA 20'
        )

    # EMA
    if 'EMA_20' in df.columns:
        plt.plot(
            df[date_column],
            df['EMA_20'],
            label='EMA 20'
        )

    plt.title(
        f'{ticker} Price Action with Moving Averages (Last 2 Years)'
    )

    plt.xlabel('Date')
    plt.ylabel('Price')

    plt.legend()
    plt.grid(True)

    plt.show()


# ==========================================
# Price Action with Bollinger Bands
# ==========================================

def plot_price_with_bollinger_bands(
    df,
    ticker,
    date_column='Date',
    price_column='Close',
    window=20
):

    # Filter last 2 years
    df = filter_last_two_years(
        df,
        date_column
    )

    plt.figure(figsize=(14, 6))

    # Close Price
    plt.plot(
        df[date_column],
        df[price_column],
        label='Close Price'
    )

    # Bollinger Bands
    plt.plot(
        df[date_column],
        df[f'BB_Upper_{window}'],
        label='Upper Band'
    )

    plt.plot(
        df[date_column],
        df[f'BB_Middle_{window}'],
        label='Middle Band'
    )

    plt.plot(
        df[date_column],
        df[f'BB_Lower_{window}'],
        label='Lower Band'
    )

    # Fill Area
    plt.fill_between(
        df[date_column],
        df[f'BB_Lower_{window}'],
        df[f'BB_Upper_{window}'],
        alpha=0.1
    )

    plt.title(
        f'{ticker} Price Action with Bollinger Bands (Last 2 Years)'
    )

    plt.xlabel('Date')
    plt.ylabel('Price')

    plt.legend()
    plt.grid(True)

    plt.show()


# ==========================================
# Price Action with RSI
# ==========================================

def plot_price_and_rsi(
    df,
    ticker,
    date_column='Date',
    price_column='Close'
):

    # Filter last 2 years
    df = filter_last_two_years(
        df,
        date_column
    )

    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        figsize=(14, 8),
        sharex=True
    )

    # Price
    ax1.plot(
        df[date_column],
        df[price_column],
        label='Close Price'
    )

    ax1.set_title(
        f'{ticker} Price Action (Last 2 Years)'
    )

    ax1.set_ylabel('Price')

    ax1.legend()
    ax1.grid(True)

    # RSI
    ax2.plot(
        df[date_column],
        df['RSI'],
        label='RSI'
    )

    ax2.axhline(70, linestyle='--')
    ax2.axhline(30, linestyle='--')

    ax2.set_title(
        'Relative Strength Index'
    )

    ax2.set_xlabel('Date')
    ax2.set_ylabel('RSI')

    ax2.legend()
    ax2.grid(True)

    plt.show()


# ==========================================
# Price Action with MACD
# ==========================================

def plot_price_and_macd(
    df,
    ticker,
    date_column='Date',
    price_column='Close'
):

    # Filter last 2 years
    df = filter_last_two_years(
        df,
        date_column
    )

    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        figsize=(14, 8),
        sharex=True
    )

    # Price
    ax1.plot(
        df[date_column],
        df[price_column],
        label='Close Price'
    )

    ax1.set_title(
        f'{ticker} Price Action (Last 2 Years)'
    )

    ax1.set_ylabel('Price')

    ax1.legend()
    ax1.grid(True)

    # MACD
    ax2.plot(
        df[date_column],
        df['MACD'],
        label='MACD'
    )

    ax2.plot(
        df[date_column],
        df['MACD_Signal'],
        label='Signal Line'
    )

    ax2.bar(
        df[date_column],
        df['MACD_Histogram'],
        alpha=0.3
    )

    ax2.set_title(
        'MACD Indicator'
    )

    ax2.set_xlabel('Date')
    ax2.set_ylabel('MACD')

    ax2.legend()
    ax2.grid(True)

    plt.show()
def plot_sentiment_vs_returns_all(
    merged_datasets
):
    """
    Plot sentiment score against daily returns
    for all stock datasets.
    """

    plt.figure(figsize=(14, 8))

    # Loop through datasets
    for ticker, df in merged_datasets.items():

        plt.scatter(
            df['Sentiment_Score'],
            df['daily_return'],
            alpha=0.5,
            label=ticker
        )
        

    plt.title(
        'Sentiment Score vs Daily Stock Return'
    )

    plt.xlabel('Sentiment Score')

    plt.ylabel('Daily Return (%)')

    plt.legend()

    plt.grid(True)

    plt.show()

def plot_sentiment_category_distribution(
    merged_datasets
):
    """
    Visualize sentiment category counts
    for all stock datasets.
    """

    plt.figure(figsize=(12, 6))

    # Store plotting data
    categories = ['Positive', 'Neutral', 'Negative']

    x = range(len(categories))

    width = 0.15

    # Loop through datasets
    for i, (ticker, df) in enumerate(
        merged_datasets.items()
    ):

        # Count categories
        counts = (
            df['sentiment_category']
            .value_counts()
            .reindex(categories, fill_value=0)
        )

        # Plot bars
        plt.bar(
            [p + (i * width) for p in x],
            counts.values,
            width=width,
            label=ticker
        )

    # Labels
    plt.xticks(
        [p + width * 2 for p in x],
        categories
    )

    plt.title(
        'Sentiment Category Distribution '
        'Across Stocks'
    )

    plt.xlabel('Sentiment Category')

    plt.ylabel('Count')

    plt.legend()

    plt.grid(True, axis='y')

    plt.show()

def classify_sentiment(score):
    """
    Classify sentiment score.
    """

    if score > 0.05:
        return 'Positive'

    elif score < -0.05:
        return 'Negative'

    else:
        return 'Neutral'


# ==========================================
# Plot Average Daily Return
# Per Sentiment Category
# ==========================================

def plot_average_return_by_sentiment(
    merged_datasets
):
    """
    Classify daily sentiment and plot
    average daily return per category.
    """

    # Store all results
    combined_results = []

    # --------------------------------------
    # Process each stock
    # --------------------------------------

    for ticker, df in merged_datasets.items():

        temp_df = df.copy()

        # Daily average sentiment category
        temp_df['sentiment_category'] = (
            temp_df['Sentiment_Score']
            .apply(classify_sentiment)
        )

        # Average daily return by category
        grouped = (
            temp_df
            .groupby('sentiment_category')['daily_return']
            .mean()
            .reset_index()
        )

        grouped['Ticker'] = ticker

        combined_results.append(grouped)

    # --------------------------------------
    # Combine all stocks
    # --------------------------------------

    final_df = pd.concat(
        combined_results,
        ignore_index=True
    )

    # --------------------------------------
    # Pivot for plotting
    # --------------------------------------

    pivot_df = final_df.pivot(
        index='Ticker',
        columns='sentiment_category',
        values='daily_return'
    )

    # Ensure order
    pivot_df = pivot_df[
        ['Negative', 'Neutral', 'Positive']
    ]

    # --------------------------------------
    # Plot
    # --------------------------------------

    pivot_df.plot(
        kind='bar',
        figsize=(12, 6)
    )

    plt.title(
        'Average Daily Return by Sentiment Category'
    )

    plt.xlabel('Stock')

    plt.ylabel('Average Daily Return (%)')

    plt.grid(True, axis='y')

    plt.legend(
        title='Sentiment Category'
    )

    plt.show()
