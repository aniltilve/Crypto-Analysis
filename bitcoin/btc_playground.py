import requests
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from coinmetrics.api_client import CoinMetricsClient




# Convert to DataFrame
df =  CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df['time'] = pd.to_datetime(df['time'])
df['PriceUSD'] = df['PriceUSD'].astype(float)

# Convert date to numeric (days since first record)
df['Days'] = (df['time'] - df['time'].min()).dt.days

# Fit a Gamma GLM with log link function
model = smf.glm('PriceUSD ~ Days', data=df, 
                family=sm.families.Gamma(sm.families.links.log())).fit()

# Print summary of the model
print(model.summary())

# Predict prices using the model
df['Predicted'] = model.predict(df['Days'])

# Plot actual vs predicted Bitcoin price
plt.figure(figsize=(10,5))
plt.scatter(df['Days'], df['PriceUSD'], label="Actual Prices", alpha=0.5)
plt.plot(df['Days'], df['Predicted'], color='red', label="Gamma GLM Prediction")
plt.xlabel("Days Since Start")
plt.ylabel("Bitcoin Price (USD)")
plt.title("Bitcoin Price Prediction Using Gamma GLM")
plt.legend()
plt.show()
