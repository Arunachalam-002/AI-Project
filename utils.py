# utils.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def moving_average(series, window):
    return series.rolling(window=window, min_periods=1).mean()

def RSI(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period, min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period, min_periods=1).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)  # neutral for initial

def plot_signals(df, buy_signals, sell_signals, title="Signals"):
    plt.figure(figsize=(14,6))
    plt.plot(df.index, df['Close'], label='Close', alpha=0.6)
    # Plot MAs if present
    if 'MA_short' in df.columns:
        plt.plot(df.index, df['MA_short'], linestyle='--', label='MA_short')
    if 'MA_long' in df.columns:
        plt.plot(df.index, df['MA_long'], linestyle='--', label='MA_long')

    # convert lists/numpy arrays to mask-based plotting
    buys_x = [df.index[i] for i, v in enumerate(buy_signals) if not (pd.isna(v))]
    buys_y = [v for v in buy_signals if not (pd.isna(v))]
    sells_x = [df.index[i] for i, v in enumerate(sell_signals) if not (pd.isna(v))]
    sells_y = [v for v in sell_signals if not (pd.isna(v))]

    if buys_x:
        plt.scatter(buys_x, buys_y, marker='^', color='g', s=100, label='Buy')
    if sells_x:
        plt.scatter(sells_x, sells_y, marker='v', color='r', s=100, label='Sell')

    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)

    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()
