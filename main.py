import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():

    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'META', 'NVDA', 'TSLA', 'ADBE', 'INTU',
        'PEP', 'COST', 'CSCO', 'ORCL', 'QCOM', 'TXN', 'AVGO', 'AMD', 'PYPL', 'NFLX',
        'ADI', 'INTC', 'AMAT', 'CRM', 'NOW', 'ISRG', 'REGN', 'VRTX', 'LRCX', 'BKNG'
    ]


    # Download and log-transform price data
    from data_loader import download_log_prices
    log_prices = download_log_prices(tickers)


    # Find the best pair and model
    from model import find_best_pair
    best_pair, best_model = find_best_pair(log_prices)
    if best_model is None:
        print("No valid model could be fitted. Please check if any tickers failed to download.")
        exit()
        
    x_ticker = best_pair[0]
    y_ticker = best_pair[1]
    intercept = best_model.params['const']
    beta = best_model.params[x_ticker]

    # Calculate spread and z-score
    from strategy import calculate_spread_and_zscore
    spread_df = calculate_spread_and_zscore(log_prices, x_ticker, y_ticker, intercept, beta)

    # Run the backtest to calculate cumulative profit and loss based on trading signals
    from backtest_module import backtest_strategy
    cumulative_pnl = backtest_strategy(spread_df)

    #Plot
    from visualization import plot_zscore, plot_cumulative_pnl, plot_prices
    plot_zscore(spread_df, x_ticker, y_ticker)
    plot_cumulative_pnl(cumulative_pnl, x_ticker, y_ticker)
    plot_prices(log_prices, x_ticker, y_ticker)

if __name__ == "__main__":
    main()

