import statsmodels.api as sm
from itertools import combinations


# Loop over all unique ticker pairs in the log_prices DataFrame,
# run an OLS regression log(Y) ~ const + log(X), record R-squared,
# and return the pair with the highest R^2 along with its fitted model.
def find_best_pair(log_prices):

    best_r2 = -1.0     # Initialize with a very low R^2 to ensure any valid pair will be better
    best_pair = None   # Placeholder for the ticker pair with the highest R^2
    best_model = None  # Placeholder for the regression model corresponding to the best pair

    # Iterate through every combination of two different tickers
    for x_ticker, y_ticker in combinations(log_prices.columns, 2):
       
        
        x = log_prices[x_ticker]
        y = log_prices[y_ticker]

        # Add a constant term (a column of 1s) to allow the model to estimate the intercept (alpha)
        try:
            X = sm.add_constant(x)
            model = sm.OLS(y, X).fit() # Fit an OLS regression model: y = alpha + beta * x
        except: 
            continue
        r2 = model.rsquared

        # Keep track of the pair with the highest R^2
        if r2 > best_r2:
            best_r2 = r2
            best_pair = (x_ticker, y_ticker)
            best_model = model

    return best_pair, best_model
