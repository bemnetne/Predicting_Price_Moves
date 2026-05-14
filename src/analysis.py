import pandas as pd
import talib
import pynance as pn
import nltk

nltk.download('vader_lexicon')

from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def calculate_sma(df, column='Close', windows=[20,50,100]):
    """
    Calculate Simple Moving Average (SMA) using TA-Lib
    """

    for window in windows:

        sma_column = f'SMA_{window}'

        df[sma_column] = talib.SMA(
            df[column],
            timeperiod=window
        )

    return df


def calculate_ema(df, column='Close', windows=[20,50,100]):
    """
    Calculate Exponential Moving Average (EMA) using TA-Lib
    """

    for window in windows:

        ema_column = f'EMA_{window}'

        df[ema_column] = talib.EMA(
            df[column],
            timeperiod=window
        )

    return df
def calculate_rsi(df, column='Close', period=14):
    """
    Calculate Relative Strength Index (RSI)
    using TA-Lib
    """

    df['RSI'] = talib.RSI(
        df[column],
        timeperiod=period
    )

    return df
def identify_rsi_signals(df):

    # overbought
    df['Overbought'] = df['RSI'] > 70

    # oversold
    df['Oversold'] = df['RSI'] < 30

    return df
def calculate_macd(
    df,
    column='Close',
    fast_period=12,
    slow_period=26,
    signal_period=9
):
    """
    Calculate MACD using TA-Lib
    """

    macd, macd_signal, macd_hist = talib.MACD(
        df[column],
        fastperiod=fast_period,
        slowperiod=slow_period,
        signalperiod=signal_period
    )

    df['MACD'] = macd
    df['MACD_Signal'] = macd_signal
    df['MACD_Histogram'] = macd_hist

    return df
def calculate_macd_last_2_years(
    df,
    column='Close',
    date_column='Date',
    fast_period=12,
    slow_period=26,
    signal_period=9
):
    """
    Calculate MACD for the last 2 years
    using TA-Lib
    """

    # ensure datetime
    df[date_column] = pd.to_datetime(df[date_column])

    # sort by date
    df = df.sort_values(date_column)

    # get latest date
    last_date = df[date_column].max()

    # filter last 2 years
    df_2y = df[
        df[date_column] >= (
            last_date - pd.DateOffset(years=2)
        )
    ].copy()

    # calculate MACD
    macd, macd_signal, macd_hist = talib.MACD(
        df_2y[column],
        fastperiod=fast_period,
        slowperiod=slow_period,
        signalperiod=signal_period
    )

    # assign results
    df_2y['MACD'] = macd
    df_2y['MACD_Signal'] = macd_signal
    df_2y['MACD_Histogram'] = macd_hist

    return df_2y

def calculate_volatility(df, window=30):

    # Daily Returns
    df['Daily_Return'] = df['Close'].pct_change()

    # Rolling Volatility
    df['Volatility'] = (
        df['Daily_Return']
        .rolling(window=window)
        .std()
    )

    return df
# Bollinger Bands
# ==========================================

def calculate_bollinger_bands(
    df,
    price_column='Close',
    window=20,
    num_std=2
):
    """
    Calculate Bollinger Bands using pandas.
    """

    # Rolling Mean
    rolling_mean = (
        df[price_column]
        .rolling(window=window)
        .mean()
    )

    # Rolling Standard Deviation
    rolling_std = (
        df[price_column]
        .rolling(window=window)
        .std()
    )

    # Bands
    df[f'BB_Middle_{window}'] = rolling_mean

    df[f'BB_Upper_{window}'] = (
        rolling_mean + (num_std * rolling_std)
    )

    df[f'BB_Lower_{window}'] = (
        rolling_mean - (num_std * rolling_std)
    )

    return df
# Bollinger Bands(for last two years of the dataset)
# ==========================================
def calculate_bollinger_bands_2years(
    df,
    price_column='Close',
    date_column='Date',
    window=20,
    num_std=2
):
    """
    Calculate Bollinger Bands for only the
    last 2 years of the dataset.
    """

    # Ensure datetime format
    df[date_column] = pd.to_datetime(
        df[date_column]
    )

    # Get latest date
    latest_date = df[date_column].max()

    # Get starting date (2 years before)
    start_date = latest_date - pd.DateOffset(years=2)

    # Filter last 2 years
    filtered_df = df[
        df[date_column] >= start_date
    ].copy()

    # Rolling Mean
    rolling_mean = (
        filtered_df[price_column]
        .rolling(window=window)
        .mean()
    )

    # Rolling Standard Deviation
    rolling_std = (
        filtered_df[price_column]
        .rolling(window=window)
        .std()
    )

    # Bollinger Bands
    filtered_df[f'BB_Middle_{window}'] = rolling_mean

    filtered_df[f'BB_Upper_{window}'] = (
        rolling_mean + (num_std * rolling_std)
    )

    filtered_df[f'BB_Lower_{window}'] = (
        rolling_mean - (num_std * rolling_std)
    )

    return filtered_df
# Maximum Drawdown
# ==========================================

def calculate_max_drawdown(df):

    # Rolling Maximum Price
    rolling_max = df['Close'].cummax()

    # Drawdown
    drawdown = (
        (df['Close'] - rolling_max)
        / rolling_max
    )

    # Store drawdown values
    df['Drawdown'] = drawdown

    # Maximum Drawdown
    max_drawdown = drawdown.min()

    return max_drawdown, df
def get_sentiment_score(text):

    score = sia.polarity_scores(str(text))

    return score['compound']
def classify_sentiment(score):

    if score > 0.05:
        return 'Positive'

    elif score < -0.05:
        return 'Negative'

    else:
        return 'Neutral'