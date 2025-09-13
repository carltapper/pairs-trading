import pandas as pd


# Compute residual spread and z-score for a given ticker pair
# Given a DataFrame of log-prices, a pair of ticker symbols, and
# regression parameters (intercept and slope), compute the spread
# (residual) and its z-score. 
# Returns a DataFrame with columns: ['spread', 'zscore'] indexed by date.

def calculate_spread_and_zscore(log_prices: pd.DataFrame, 
                                x_ticker: str,
                                y_ticker: str,
                                intercept: float, 
                                beta: float) -> pd.DataFrame:
   
    # Extract the two series:
    # x and y are pandas Series where each value is a log-price, 
    # and the index is the date (e.g. 2020-01-01). This allows us to align and operate on time series easily.
    x = log_prices[x_ticker]
    y = log_prices[y_ticker]

    # Compute residual spread: y - (alpha + beta * x)
    spread = y - (intercept + beta * x)

    # Compute statistics
    mean_spread = spread.mean()
    std_spread = spread.std()

    # Compute z-score. Z-score shows how far the spread is from its mean in units of standard deviation
    zscore = (spread - mean_spread) / std_spread

    # Return as DataFrame
    result = pd.DataFrame({
        'spread': spread,
        'zscore': zscore
    })
    return result
