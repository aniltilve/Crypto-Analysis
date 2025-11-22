import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from coinmetrics.api_client import CoinMetricsClient
from datetime import timedelta

# Initialize the CoinMetrics client
client = CoinMetricsClient()

# Fetch Bitcoin price data
data = client.get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()

# Preprocessing data
data['time'] = pd.to_datetime(data['time'])
data.set_index('time', inplace=True)
data = data.sort_index()
data['PriceUSD'] = data['PriceUSD'].astype(float)

# Handle missing values (if any)
data['PriceUSD'] = data['PriceUSD'].ffill()

# Check for stationarity (Augmented Dickey-Fuller Test)
def check_stationarity(series):
    result = adfuller(series)
    print("ADF Statistic:", result[0])
    print("p-value:", result[1])
    print("Critical Values:", result[4])
    if result[1] <= 0.05:
        print("The series is stationary.")
    else:
        print("The series is not stationary.")

check_stationarity(data['PriceUSD'])

# Differencing to make the series stationary if needed
data_diff = data['PriceUSD'].diff().dropna()

check_stationarity(data_diff)

# Split data into training and testing sets
train_data = data['PriceUSD'][:-365]
test_data = data['PriceUSD'][-365:]

# Fit SARIMA model
model = SARIMAX(train_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 365), enforce_stationarity=False, enforce_invertibility=False)
model_fit = model.fit(disp=False)

# Forecast for one year ahead
forecast_steps = 365
forecast = model_fit.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=train_data.index[-1] + timedelta(days=1), periods=forecast_steps)
forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(data['PriceUSD'], label='Actual Prices')
plt.plot(forecast_series, label='Forecasted Prices', color='orange')
plt.title('Bitcoin Price Forecast Using SARIMA')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# Print forecast
print("Forecasted Prices:")
print(forecast_series)
