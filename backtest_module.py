import pandas as pd

# Simple mean-reversion strategy backtest
def backtest_strategy(spread_df, entry_z=1.0, exit_z=0.0):
    position = 0  # 1 = long, -1 = short, 0 = flat
    pnl = []
    spread = spread_df['spread']
    zscore = spread_df['zscore']

    for i in range(1, len(spread)):
        prev_spread = spread.iloc[i - 1]
        curr_spread = spread.iloc[i]
        z = zscore.iloc[i]

        daily_return = 0

        # Entry rules
        if position == 0:
            if z > entry_z:
                position = -1  # Short spread
            elif z < -entry_z:
                position = 1  # Long spread

        # Exit rule
        elif abs(z) < exit_z:
            position = 0

        # PnL: change in spread * position
        daily_return = position * (curr_spread - prev_spread)
        pnl.append(daily_return)

    # Pad the first day with 0
    pnl = [0] + pnl
    return pd.Series(pnl, index=spread_df.index).cumsum()