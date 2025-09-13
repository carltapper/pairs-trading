import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import statsmodels.api as sm
import webbrowser
from threading import Timer
from sklearn.model_selection import train_test_split  

from data_loader import download_log_prices
from strategy import calculate_spread_and_zscore
from backtest_module import backtest_strategy

host = 'localhost'
port = 8050

def open_browser():
    webbrowser.open_new(f'http://{host}:{port}')

# Define tickers
TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'META', 'NVDA', 'TSLA', 'ADBE', 'INTU',
    'PEP', 'COST', 'CSCO', 'ORCL', 'QCOM', 'TXN', 'AVGO', 'AMD', 'PYPL', 'NFLX',
    'ADI', 'INTC', 'AMAT', 'CRM', 'NOW', 'ISRG', 'REGN', 'VRTX', 'LRCX', 'BKNG'
]

log_prices = None

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Pairs Trading Dashboard', style={'textAlign': 'center'}),

    html.Div([
        dcc.Dropdown(
            id='x-ticker',
            options=[{'label': t, 'value': t} for t in TICKERS],
            value='AAPL'
        ),
        dcc.Dropdown(
            id='y-ticker',
            options=[{'label': t, 'value': t} for t in TICKERS],
            value='MSFT'
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div(id='r2-output', style={'marginTop': 20, 'textAlign': 'center'}),

    dcc.Graph(id='price-plot'),
    dcc.Graph(id='zscore-plot'),
    dcc.Graph(id='spread-plot'),
    dcc.Graph(id='pnl-plot')
])

@app.callback(
    [Output('r2-output', 'children'),
     Output('price-plot', 'figure'),
     Output('zscore-plot', 'figure'),
     Output('spread-plot', 'figure'),
     Output('pnl-plot', 'figure')],
    [Input('x-ticker', 'value'),
     Input('y-ticker', 'value')]
)
def update_dashboard(x_ticker, y_ticker):
    if x_ticker == y_ticker:
        fig = go.Figure()
        fig.add_annotation(
            text="Select two different tickers",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=20)
        )
        return (
            "Error: Tickers must be different",
            fig, fig, fig, fig
        )


    full_log_prices = log_prices[[x_ticker, y_ticker]].dropna()

    # Prepare input and target series
    X = full_log_prices[[x_ticker]]  # input features
    Y = full_log_prices[y_ticker]    # target variable

    # Split into training and testing sets without shuffling (preserve time order)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, shuffle=False)

    # Train linear regression model on training set
    X_train_const = sm.add_constant(X_train)
    model = sm.OLS(Y_train, X_train_const).fit()
    intercept = model.params['const']
    beta = model.params[x_ticker]
    r2 = model.rsquared

    # Prepare test data as a DataFrame with matching columns
    test_log_prices = pd.DataFrame({
        x_ticker: X_test[x_ticker],
        y_ticker: Y_test
    })
   
    # Compute spread and z-score based on model parameters and test data
    spread_df = calculate_spread_and_zscore(test_log_prices, x_ticker, y_ticker, intercept, beta)
    cumulative_pnl = backtest_strategy(spread_df)

    print("\n\n\n\n\n\nZ-score:", spread_df['zscore'].head())
    print("Spread:", spread_df['spread'].head())
    print("PnL:", cumulative_pnl.head())
    price_fig = go.Figure()
    price_fig.add_trace(go.Scatter(x=test_log_prices.index, y=test_log_prices[x_ticker], name=x_ticker))
    price_fig.add_trace(go.Scatter(x=test_log_prices.index, y=test_log_prices[y_ticker], name=y_ticker))
    price_fig.update_layout(title='Log Prices (Test Data)', title_x=0.5, yaxis_title='Log Price')

    z = spread_df['zscore']
    z_fig = go.Figure()
    z_fig.add_trace(go.Scatter(x=z.index, y=z, name='Z-score'))
    z_fig.add_hline(y=1.0, line=dict(dash='dash', color='red'))
    z_fig.add_hline(y=-1.0, line=dict(dash='dash', color='green'))
    z_fig.add_hline(y=0.0, line=dict(color='black'))
    z_fig.update_layout(title='Z-score Over Time',title_x=0.5, yaxis_title='Z-score')

    spread_fig = go.Figure()
    spread_fig.add_trace(go.Scatter(x=spread_df.index, y=spread_df['spread'], name='Spread'))
    spread_fig.update_layout(title='Spread Over Time', title_x=0.5, yaxis_title='Spread')

    pnl_fig = go.Figure()
    pnl_fig.add_trace(go.Scatter(x=cumulative_pnl.index, y=cumulative_pnl.values, name='Cumulative PnL'))
    pnl_fig.update_layout(title='Cumulative PnL', title_x=0.5, yaxis_title='Cumulative PnL')
    print(spread_df[['spread', 'zscore']].head())
    return (
        f'R² value: {r2:.4f}',
        price_fig,
        z_fig,
        spread_fig,
        pnl_fig
    )

if __name__ == '__main__':
    log_prices = download_log_prices(TICKERS)

    Timer(1, open_browser).start()
    app.run(debug=True, host=host, port=port)
