# Crypto-Analysis

Python scripts that analyze crypto prices. These scripts require the Anaconda libraries. Price data is in CSV format from Coinmetrics (downloaded as Excel converted to CSV)

# btc-price-forecast.py

This script traces upper bound and lower bound curves to predict Bitcoin price over a user-specified interval. The curves are generated using a linear regression with a natural log transformation as the modelling function (i.e. y = a * ln(x) + b). The fair value is calculated as the midpoint between the upper and lower bound curves. Below is a sample run of the script.

![btc-price-forecast.py](btc_price.jpeg?raw=true)
