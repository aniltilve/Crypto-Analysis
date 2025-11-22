import numpy as np
from matplotlib import (
    pyplot as plt
)
import pandas as pd

df_btc = pd.read_csv('./Bitcoin/BTCUSD.csv')
df_xau = pd.read_csv('./Commodities/Gold/XAUUSD.csv')


returns_btc = df_btc['close'].pct_change().dropna()
returns_gold = df_xau['close'].pct_change().dropna()

returns_btc, returns_gold = returns_btc.align(returns_gold, join='inner')


# Cross-correlation with proper alignment
lags = range(-1460, 1460)
corrs = []

for lag in lags:
    shifted = returns_gold.shift(lag)
    # Drop missing values after shifting
    valid = pd.concat([returns_btc, shifted], axis=1).dropna()
    corr = valid.iloc[:, 0].corr(valid.iloc[:, 1])
    corrs.append(corr)


plt.figure(figsize=(10,5))
plt.scatter(lags, corrs, color='black')
plt.axvline(0, color='red', linestyle='--')
plt.title("Cross-Correlation Between Bitcoin and Gold Returns")
plt.xlabel("Lag (days)")
plt.ylabel("Correlation")
plt.grid(True, alpha=0.3)
plt.show()
