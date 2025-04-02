# Volatility Trading Strategy using VIX Futures and Options

## Overview
This project implements a volatility trading strategy using VIX futures and options. The strategy involves:
- Speculating on volatility based on VIX levels.
- Hedging or speculating using VIX futures and options.
- Market regime classification using machine learning (KMeans clustering) for low, medium, and high volatility regimes.
- Backtesting the strategy using the Backtrader library.

## Requirements
- Python 3.7+
- Install dependencies using `pip install -r requirements.txt`.

   
## Key Features:
Strategy Logic: Buy when the VIX exceeds the long threshold (20), and sell when it falls below the short threshold (15).

Market Regime Analysis: Classifies market regimes using KMeans clustering based on VIX levels and rolling statistics (mean and std).

Stop-Loss Mechanism: Implements a 2% stop-loss to protect the portfolio from large losses.

Backtesting: Uses Backtrader to simulate the strategy over historical data and generates a plot of the results.
## Running the Project
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/volatility-trading-strategy-vix.git
   cd volatility-trading-strategy-vix

