"""
volatility_trading_strategy.py

This Python script implements a volatility trading strategy using VIX futures and options. 
The strategy involves the following steps:

1. **Data Collection**: 
   - Downloads historical VIX index data from Yahoo Finance using the `yfinance` library.
   
2. **Market Regime Classification**: 
   - Uses KMeans clustering to classify market regimes based on VIX levels (low, medium, and high volatility).
   
3. **Strategy Implementation**: 
   - Implements a trading strategy in Backtrader where the system takes long positions in VIX futures when volatility is expected to rise and short positions when volatility is expected to decrease. 
   - The strategy also includes a stop-loss mechanism to minimize potential losses.
   
4. **Backtesting**: 
   - Backtests the strategy using historical data to evaluate its performance (portfolio growth, risk metrics, etc.).
   - Provides a visual plot of the backtest results.

Dependencies:
- `yfinance` for data collection from Yahoo Finance.
- `backtrader` for backtesting the strategy.
- `pandas`, `numpy`, `matplotlib` for data analysis and visualization.
- `scikit-learn` for machine learning-based market regime classification.

Usage:
1. Clone the repository and install dependencies.
2. Run the script to fetch VIX data, run the strategy, and visualize the results.

Note: Modify the strategy parameters and backtest period as necessary to fit your analysis.
"""

import pandas as pd
import yfinance as yf
import backtrader as bt
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Step 1: Data Collection - Download Historical VIX Data from Yahoo Finance
def get_vix_data(start_date='2000-01-01', end_date='2025-01-01'):
    # Using yfinance to fetch VIX data
    vix_data = yf.download('^VIX', start=start_date, end=end_date)
    vix_data['Date'] = vix_data.index
    vix_data.reset_index(drop=True, inplace=True)
    return vix_data

# Step 2: Market Regime Classification using K-Means Clustering
def classify_market_regimes(vix_data):
    # We will use KMeans to cluster VIX levels into different market regimes
    vix_data['VIX_rolling_mean'] = vix_data['Close'].rolling(window=20).mean()
    vix_data['VIX_rolling_std'] = vix_data['Close'].rolling(window=20).std()
    
    # Using KMeans to classify data into 3 clusters: Low, Medium, High volatility regimes
    kmeans = KMeans(n_clusters=3, random_state=42)
    vix_data['Regime'] = kmeans.fit_predict(vix_data[['Close', 'VIX_rolling_mean', 'VIX_rolling_std']])
    
    # Plotting the clusters
    plt.scatter(vix_data.index, vix_data['Close'], c=vix_data['Regime'], cmap='viridis')
    plt.title('VIX Data with Market Regimes')
    plt.show()
    
    return vix_data

# Step 3: Define the Volatility Strategy in Backtrader
class VIXStrategy(bt.Strategy):
    # Define the parameters for the strategy
    params = (
        ('long_threshold', 20),  # Long VIX futures when VIX > 20
        ('short_threshold', 15), # Short VIX futures when VIX < 15
        ('stop_loss', 0.02),     # Stop loss at 2%
    )
    
    def __init__(self):
        # Initialize the moving averages or signals
        self.vix_data = self.datas[0]
        self.buy_signal = self.vix_data.Close > self.params.long_threshold
        self.sell_signal = self.vix_data.Close < self.params.short_threshold
        self.stop_price = 0
        
    def next(self):
        # Implement the strategy logic based on VIX levels
        if self.buy_signal[0]:
            if not self.position:  # If no position, buy
                self.buy()
                self.stop_price = self.data.close[0] * (1 - self.params.stop_loss)  # Set stop loss
            
        elif self.sell_signal[0]:
            if not self.position:  # If no position, sell short
                self.sell()
                self.stop_price = self.data.close[0] * (1 + self.params.stop_loss)  # Set stop loss

        # Implement stop loss exit
        if self.position and self.position.size > 0 and self.data.close[0] < self.stop_price:
            self.sell()  # Exit long position
        elif self.position and self.position.size < 0 and self.data.close[0] > self.stop_price:
            self.buy()  # Exit short position

# Step 4: Backtesting the Strategy
def run_backtest():
    # Load historical VIX data
    vix_data = get_vix_data()
    
    # Classify market regimes using KMeans
    vix_data = classify_market_regimes(vix_data)
    
    # Convert VIX data into Backtrader DataFrame
    vix_data_bt = bt.feeds.PandasData(dataname=vix_data)

    # Initialize Backtrader's Cerebro engine
    cerebro = bt.Cerebro()
    cerebro.adddata(vix_data_bt)
    
    # Add strategy to Cerebro engine
    cerebro.addstrategy(VIXStrategy)
    
    # Set initial cash
    cerebro.broker.set_cash(100000)
    
    # Set commission (example: 0.1% per trade)
    cerebro.broker.set_commission(commission=0.001)
    
    # Print starting cash
    print(f'Starting Portfolio Value: {cerebro.broker.getvalue()}')
    
    # Run the backtest
    cerebro.run()
    
    # Print final cash
    print(f'Ending Portfolio Value: {cerebro.broker.getvalue()}')

    # Plot the results
    cerebro.plot()

# Step 5: Main Function to Execute the Project
if __name__ == '__main__':
    run_backtest()
