# Pairs Trading Project


This is a simple project that explores pairs trading, a type of strategy that looks for two stocks that often move in the same way. If the relationship between them suddenly becomes unusual, the idea is to place trades based on the assumption that things will return to normal.

The strategy is based on mean reversion. If two stocks usually move together, but one moves away, we assume it will come back again.

I started this project to learn more about algorithmic trading and data-driven strategies. The goal was to understand how a pairs trading model works in practice and simulate what would happen if we followed it over time. While the dashboard wasn't part of the original plan, it turned out to be a useful way to explore the results and test different stock combinations. Hopefully, this gives a good overview of both the strategy and how it might be implemented.

---

## How it works

1. Download historical log-prices of stocks from Nasdaq-100.
2. Try every possible pair and run a simple linear regression (OLS) on them.
3. Find the pair with the highest R² value – this means they moved most closely together in the past.
4. Calculate the spread between them and track its z-score (how unusual the current spread is).
5. If the z-score is high, we assume the spread will shrink (mean reversion). If low, it will expand.
6. Based on this, simulate trades to see how much profit we would have made.

---

## Files in the project

### main.py
This file runs the full process:
- Downloads prices
- Finds the best stock pair using R²
- Fits a model to that pair
- Calculates spread and z-score
- Simulates trades (backtest)
- Shows z-score and cumulative profit in simple plots

Use this if you just want to test the full logic.

### dashboard.py
This file creates an interactive dashboard:
- You can select any two tickers yourself
- It shows prices, z-score, spread, and simulated profit
- The model is trained only on a part of the data, and the rest is used to test it

Good if you want to try different pairs or present results.

### strategy.py
Handles the calculation of spread and z-score.

### backtest_module.py
Simulates the strategy (when to buy/sell) and calculates profit.

### data_loader.py
Downloads historical data using yfinance and converts it to log-prices.

### model.py
Contains logic to fit regression models for a stock pair.

### visualization.py
Used in main.py to show plots like spread and z-score.

---

## Requirements

pip install yfinance pandas plotly dash statsmodels scikit-learn

---

## Notes
This is just a basic simulation. No trading costs are included. It’s just a way to understand the idea of mean reversion and how some stocks behave similarly over time.

---

## Author
Carl Tapper Johansen
