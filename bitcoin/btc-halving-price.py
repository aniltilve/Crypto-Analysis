import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime
from coinmetrics.api_client import CoinMetricsClient



client = CoinMetricsClient()

df_btc_price = client.get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_btc_price['time'] = df_btc_price['time'].dt.tz_localize(None)

df_halving = df_btc_price[(df_btc_price['time'].isin([
    '2012-11-28',
    '2016-07-09',
    '2020-05-11',
    '2024-04-19'
]))]

df_halving['PriceUSD'] = np.log(df_halving['PriceUSD'])

def modelling_func(x, a, b, c, d):
    return a * np.log(x * b + c) + d


popt, pcov = curve_fit(modelling_func, df_halving.index.to_list(), df_halving['PriceUSD'])

dr_fit = pd.date_range(df_btc_price['time'].iloc[0], '2030-01-01')
fitIndexes = np.array([date_index + 1 for date_index in range(len(dr_fit))])

fittedPrices = modelling_func(fitIndexes, popt[0], popt[1], popt[2], popt[3])

#plotting
figure, axes = pyplot.subplots()
axes.grid(axis='both', which='major', color='silver')
axes.grid(axis='both', which='minor', color='gainsboro')
pyplot.tick_params(axis='y',which='minor')

axes.semilogy(df_btc_price['time'], df_btc_price['PriceUSD'])
axes.semilogy(dr_fit, np.exp(fittedPrices), color='orange')
axes.semilogy(df_halving['time'], np.exp(df_halving['PriceUSD']), color='orange', marker='o', linestyle='none')


pyplot.axvline(datetime.datetime(2012,11,28), color='black')
pyplot.axvline(datetime.datetime(2016,7,9), color='black')
pyplot.axvline(datetime.datetime(2020,5,11), color='black')
pyplot.axvline(datetime.datetime(2024,4,19), color='black')
pyplot.axvline(datetime.datetime(2028,2,18), color='black')

axes.xaxis.set_major_locator(dates.YearLocator(1,month=1,day=1))
axes.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
axes.xaxis.set_minor_locator(dates.MonthLocator(7))
axes.xaxis.set_major_formatter(dates.DateFormatter('%Y'))

currencyFormatter = ticker.StrMethodFormatter('${x:,.2f}')
axes.yaxis.set_minor_locator(ticker.LogLocator(base=10.0,subs=(0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9),numticks=500))
axes.yaxis.set_major_formatter(currencyFormatter)


pyplot.ylabel('BTC - Price in USD')
pyplot.ylim(0.1,1000000)
pyplot.xlim(datetime.datetime(2010,7,18), datetime.datetime(2030,1,1))
pyplot.show()