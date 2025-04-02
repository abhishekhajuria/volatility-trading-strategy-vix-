import yfinance as yf

def get_vix_data(start_date='2000-01-01', end_date='2025-01-01'):
    """
    Fetches historical VIX data from Yahoo Finance.
    """
    vix_data = yf.download('^VIX', start=start_date, end=end_date)
    vix_data['Date'] = vix_data.index
    vix_data.reset_index(drop=True, inplace=True)
    return vix_data
