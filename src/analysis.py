import pandas as pd
import talib


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