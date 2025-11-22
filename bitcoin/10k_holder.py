import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient

def GetStdLineLabel(z_score):
    dec_places = 3 if z_score > 3 else 2

    if z_score > 0:
        return f'μ + {z_score}σ ({100 - stats.norm.cdf(z_score) * 100:.{dec_places}f}% chance of going higher)'
    elif z_score < 0:
        return f'μ - {abs(z_score)}σ ({stats.norm.cdf(z_score) * 100:.{dec_places}f}% chance of going lower)'
    else:
        return 'Mean Trendline (μ)'

# Data ETL

client = CoinMetricsClient()

df_btc_adr_bal = client.get_asset_metrics(assets='BTC', metrics=['AdrBalNtv10KCnt'], page_size=10000).to_dataframe()
df_btc_adr_bal['timeOrdinal'] = df_btc_adr_bal['time'].apply(lambda x: x.toordinal())
df_btc_adr_bal['time'] = df_btc_adr_bal['time'].dt.tz_localize(None)
df_btc_adr_bal['AdrBalNtv10KCnt'] = df_btc_adr_bal['AdrBalNtv10KCnt'].astype(float)

model = np.poly1d(np.polyfit(df_btc_adr_bal['timeOrdinal'], df_btc_adr_bal['AdrBalNtv10KCnt'], 2))
line = np.linspace(df_btc_adr_bal['timeOrdinal'].iloc[0], df_btc_adr_bal['timeOrdinal'].iloc[-1], len(df_btc_adr_bal))
fit = model(line)
resid = df_btc_adr_bal['AdrBalNtv10KCnt'] - fit
std = np.std(resid)
p0 = np.percentile(resid, 0)
p100 = np.percentile(resid, 100)


dr_forecast = pd.date_range(df_btc_adr_bal['time'].iloc[0], '2030-01-01')
df_forecast_ord = dr_forecast.to_series().apply(lambda x: x.toordinal())
line_forecast = np.linspace(df_forecast_ord[0], df_forecast_ord[-1], len(df_forecast_ord))
forecast = model(line_forecast)

# Plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.025, right=0.98, top=0.985, bottom=0.04)
ax.grid(axis='both', which='major', color='silver')
ax.grid(axis='both', which='minor', color='gainsboro')


ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

ax.axvline(dt.datetime(2012, 11, 28), color='black', label='Bitcoin halving')
ax.axvline(dt.datetime(2016, 7, 9), color='black')
ax.axvline(dt.datetime(2020, 5, 11), color='black')
ax.axvline(dt.datetime(2024, 4, 19), color='black')

ax.plot(
    df_btc_adr_bal['time'], 
    np.array(df_btc_adr_bal['AdrBalNtv10KCnt']), 
    label='Addresses with 10k or more BTC',
    zorder=4
)

std_lines = [
    {'z-score': 0, 'color': 'gray'},
    {'z-score': -2.5, 'color': 'limegreen'},
    {'z-score': -2, 'color': 'limegreen'},
    {'z-score': -1.5, 'color': 'chartreuse'},
    {'z-score': -1, 'color': 'chartreuse'},
    {'z-score': -0.5, 'color': 'yellowgreen'},
    {'z-score': 0.5, 'color': 'gold'},
    {'z-score': 1, 'color': 'orange'},
    {'z-score': 1.5, 'color': 'orange'},
    {'z-score': 2, 'color': 'darkorange'},
    {'z-score': 2.5, 'color': 'darkorange'},
]

""" for std_line in std_lines:
    ax.plot(
        dr_forecast, 
        forecast + std_line['z-score'] * std,
        color = std_line['color'],
        linewidth=1,
        linestyle='solid' if std_line['z-score'] % 1 == 0 else 'dashed',
        zorder=3,
        label=GetStdLineLabel(std_line['z-score'])
    ) """

ax.plot(dr_forecast, forecast, color='tab:orange', label='Fit')
ax.plot(dr_forecast, forecast+p0, color='tab:green', label='Support')
ax.plot(dr_forecast, forecast+p100, color='tab:red', label='Resistance')


plt.ylim(0, 150)
plt.xlim(df_btc_adr_bal['time'].iloc[0], dr_forecast[-1])
plt.legend(title='Legend')
plt.show()