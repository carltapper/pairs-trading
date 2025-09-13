import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd

def plot_zscore(spread_df: pd.DataFrame, x_ticker: str, y_ticker: str):
    z = spread_df['zscore']
    plt.figure(figsize=(12, 4))
    plt.plot(z, label='Z-score')
    plt.axhline(1.0, color='red', linestyle='--', label='Entry Short (+1)')
    plt.axhline(-1.0, color='green', linestyle='--', label='Entry Long (-1)')
    plt.axhline(0.0, color='black', linestyle='-')
    plt.title(f'Z-score over Time for Pair: {x_ticker} & {y_ticker}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def plot_cumulative_pnl(cumulative_pnl: pd.Series, x_ticker: str, y_ticker: str):
    plt.figure(figsize=(12, 4))
    plt.plot(cumulative_pnl, label='Cumulative PnL', color='purple')
    plt.title(f'Cumulative Profit and Loss for Pair: {x_ticker} & {y_ticker}')
    plt.xlabel('Date')
    plt.ylabel('PnL')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_prices(log_prices: pd.DataFrame, x_ticker: str, y_ticker: str):
    plt.figure(figsize=(12, 4))
    plt.plot(log_prices[x_ticker], label=f'{x_ticker} (log-price)')
    plt.plot(log_prices[y_ticker], label=f'{y_ticker} (log-price)')
    plt.title('Log-Prices of Selected Tickers')
    plt.xlabel('Date')
    plt.ylabel('Log-Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


