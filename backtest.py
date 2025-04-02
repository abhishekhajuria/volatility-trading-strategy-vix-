import backtrader as bt
from data_collector import get_vix_data
from market_regime_classifier import classify_market_regimes
from volatility_trading_strategy import VIXStrategy

def run_backtest():
    vix_data = get_vix_data()
    vix_data = classify_market_regimes(vix_data)
    
    vix_data_bt = bt.feeds.PandasData(dataname=vix_data)

    cerebro = bt.Cerebro()
    cerebro.adddata(vix_data_bt)
    cerebro.addstrategy(VIXStrategy)
    cerebro.broker.set_cash(100000)
    cerebro.broker.set_commission(commission=0.001)

    print(f'Starting Portfolio Value: {cerebro.broker.getvalue()}')
    cerebro.run()
    print(f'Ending Portfolio Value: {cerebro.broker.getvalue()}')
    cerebro.plot()

if __name__ == '__main__':
    run_backtest()
