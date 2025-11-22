import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.lines as mlines
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient
import scipy.stats as stats



df_btc_act_sply = CoinMetricsClient().get_asset_metrics(
    assets='BTC', 
    metrics=[
        'SplyCur',
        'SplyActEver',
        'SplyAct10yr',
        'SplyAct5yr',
        'SplyAct4yr',
        'SplyAct3yr',
        'SplyAct2yr',
        'SplyAct1yr',
        'SplyAct180d',
        'SplyAct90d',
        'SplyAct30d',
        'SplyAct7d',
        'SplyAct1d'
    ], 
    page_size=10000
).to_dataframe()

df_btc_act_sply['time'] = df_btc_act_sply['time'].dt.tz_localize(None)
df_btc_act_sply = df_btc_act_sply.drop(columns=['asset'])

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.035, right=0.98, top=0.98, bottom=0.04)

plt.fill_between(df_btc_act_sply['time'], df_btc_act_sply['SplyActEver'], df_btc_act_sply['SplyCur'], label='Current supply', alpha=0.8, zorder=2)
plt.fill_between(df_btc_act_sply['time'], df_btc_act_sply['SplyAct10yr'], df_btc_act_sply['SplyActEver'], label='Supply that was ever active', alpha=0.8, zorder=2)
plt.fill_between(df_btc_act_sply['time'], df_btc_act_sply['SplyAct5yr'], df_btc_act_sply['SplyAct10yr'], label='Supply that was active in the last 10 years', alpha=0.8, zorder=2)
plt.fill_between(df_btc_act_sply['time'], df_btc_act_sply['SplyAct4yr'], df_btc_act_sply['SplyAct5yr'], label='Supply that was active in the last 5 years', alpha=0.8, zorder=2)
plt.fill_between(df_btc_act_sply['time'], df_btc_act_sply['SplyAct3yr'], df_btc_act_sply['SplyAct4yr'], label='Supply that was active in the last 4 years', alpha=0.8, zorder=2)
plt.fill_between(df_btc_act_sply['time'], df_btc_act_sply['SplyAct2yr'], df_btc_act_sply['SplyAct3yr'], label='Supply that was active in the last 3 years', alpha=0.8, zorder=2)
plt.fill_between(df_btc_act_sply['time'], df_btc_act_sply['SplyAct1yr'], df_btc_act_sply['SplyAct2yr'], label='Supply that was active in the last 2 years', alpha=0.8, zorder=2)
plt.fill_between(df_btc_act_sply['time'], df_btc_act_sply['SplyAct180d'], df_btc_act_sply['SplyAct1yr'], label='Supply that was active in the last Year', alpha=0.8, zorder=2)
plt.fill_between(df_btc_act_sply['time'], df_btc_act_sply['SplyAct90d'], df_btc_act_sply['SplyAct180d'], label='Supply that was active in the last 6 months', alpha=0.8, zorder=2)
plt.fill_between(df_btc_act_sply['time'], df_btc_act_sply['SplyAct30d'], df_btc_act_sply['SplyAct90d'], label='Supply that was active in the last 3 months', alpha=0.8, zorder=2)
plt.fill_between(df_btc_act_sply['time'], df_btc_act_sply['SplyAct7d'], df_btc_act_sply['SplyAct30d'], hatch='........', label='Supply that was active in the last month', alpha=0.8, zorder=2)
plt.fill_between(df_btc_act_sply['time'], df_btc_act_sply['SplyAct1d'], df_btc_act_sply['SplyAct7d'], hatch='\\\\\\\\\\\\', label='Supply that was active in the last week', alpha=0.8, zorder=2)
plt.fill_between(df_btc_act_sply['time'], 0, df_btc_act_sply['SplyAct1d'], hatch='........', label='Supply that was active in the last day', alpha=0.8, zorder=2)

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))


ax.yaxis.set_major_locator(ticker.MultipleLocator(1e6))
ax.yaxis.set_major_formatter(ticker.EngFormatter())

plt.grid(which='major', axis='both', alpha=0.75, zorder=1)
plt.grid(which='minor', axis='both', alpha=0.25, zorder=1)

plt.xlim(df_btc_act_sply['time'].iloc[0], df_btc_act_sply['time'].iloc[-1])
plt.ylim(0, 2.1e7)
plt.legend(title='Bitcoin Supply Activity')
plt.show()