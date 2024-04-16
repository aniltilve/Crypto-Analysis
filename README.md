# Crypto-Analysis

Python scripts that analyze crypto prices. These scripts require the Anaconda libraries. Price data is in CSV format from Coinmetrics (downloaded as Excel converted to CSV)

# btc-price-forecast.py

This script traces upper bound and lower bound curves to predict Bitcoin price over a user-specified interval. The curves are generated performing a linear regression with a natural log transformation (i.e. y = a * ln(x) + b) on manually selected upper and lower bound data points (manual selection seems to provide more accurate results than an algorithm like RANSAC from my experimentation). An offset is added to the x values to better fit the curves to the upper and lower extremes of the price data. The fair value is calculated as the midpoint between the upper and lower bound curves.

Below is a sample run of the script. The script can predict realistic values over the next four years (as Bitcoin's price is believed by many to be influenced by its four-year halving cycle)

![btc-price-forecast.py](btc_price.jpeg?raw=true)

# doge-adr-bal-ntv-1m.py

This script traces upper bound and lower bound curves to predict the number of addresses holding 1 million or more Dogecoin over a user-specified interval. The curves are generated performing a linear regression (i.e. y = a * x + b) on manually selected upper and lower bound data points (manual selection seems to provide more accurate results than an algorithm like RANSAC from my experimentation).

![btc-price-forecast.py](doge_adr_bal_ntv_1m_count.png?raw=true)
