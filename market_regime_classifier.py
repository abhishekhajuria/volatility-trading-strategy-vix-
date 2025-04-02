import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def classify_market_regimes(vix_data):
    """
    Classifies the market into different volatility regimes using KMeans clustering.
    """
    vix_data['VIX_rolling_mean'] = vix_data['Close'].rolling(window=20).mean()
    vix_data['VIX_rolling_std'] = vix_data['Close'].rolling(window=20).std()
    
    kmeans = KMeans(n_clusters=3, random_state=42)
    vix_data['Regime'] = kmeans.fit_predict(vix_data[['Close', 'VIX_rolling_mean', 'VIX_rolling_std']])
    
    plt.scatter(vix_data.index, vix_data['Close'], c=vix_data['Regime'], cmap='viridis')
    plt.title('VIX Data with Market Regimes')
    plt.show()
    
    return vix_data
