import yfinance as yf
import numpy as np
import pandas as pd

# Downloads adjusted closing prices for given tickers over a specified date range,
# computes the natural logarithm of the prices, and returns a DataFrame with NaNs removed.
def download_log_prices(tickers, start='2020-01-01', end='2025-01-01'):
    data = yf.download(tickers, start=start, end=end, threads=False)

    # Handle MultiIndex (with levels like 'Adj Close')
    if isinstance(data.columns, pd.MultiIndex):
        if 'Adj Close' in data.columns.get_level_values(0):
            data = data['Adj Close']
        elif 'Close' in data.columns.get_level_values(0):
            data = data['Close']
        else:
            raise ValueError("Could not find 'Adj Close' or 'Close' in downloaded data")
    else:
        # Single-level columns: assume the prices are correct
        pass
    # Remove any tickers that failed to download (NaNs)
    data = data.dropna(axis=1)
    return np.log(data).dropna()
