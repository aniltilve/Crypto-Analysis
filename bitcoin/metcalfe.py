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

# Helper functions
def CurrencyFormatter(x, pos):
    if x >= 1e18:
        return '${:.0f}Qt'.format(x / 1e18)
    elif x >= 1e15:
        return '${:.0f}Q'.format(x / 1e15)
    elif x >= 1e12:
        return '${:.0f}T'.format(x / 1e12)
    elif x >= 1e9:
        return '${:.0f}B'.format(x / 1e9)
    elif x >= 1e6:
        return '${:.0f}M'.format(x / 1e6)
    elif  x >= 1e3:
        return '${:.0f}k'.format(x / 1e3)
    elif x >= 1:
        return '${:,.0f}'.format(x)
    elif x >= 0.1:
        return '${:,.1f}'.format(x)
    else:
        return '${:,.2f}'.format(x)
    
# Data ETL

df_btc = (
    CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['CapMrktCurUSD', 'AdrActCnt'], page_size=10000)
        .to_dataframe()
)
print(df_btc)

df_btc['time'] = pd.to_datetime(df_btc['time']).dt.tz_localize(None)
df_btc[['CapMrktCurUSD', 'AdrActCnt']] = df_btc[['CapMrktCurUSD', 'AdrActCnt']].astype(float)
#df_btc_price['AdrActCnt'] = df_btc_price['AdrActCnt'].rolling(window=300).mean()

df_btc.dropna(inplace=True)

df_btc['Sqrd_AdrActCnt'] = np.square(df_btc['AdrActCnt'])
df_btc['Log_SqrdAdrActCnt'] = np.log(df_btc['Sqrd_AdrActCnt'])
df_btc['Log_CapMrktCurUSD'] = np.log(df_btc['CapMrktCurUSD'])

# Regression
a, b, r, p, stderr = stats.linregress(df_btc['Log_SqrdAdrActCnt'], df_btc['Log_CapMrktCurUSD'])
fit = a * df_btc['Log_SqrdAdrActCnt'] + b
resid = df_btc['Log_CapMrktCurUSD'] - fit
std = np.std(resid)


forecast_adr_act_cnt = np.arange(1e2, 1e10, 1000)
forecast_adr_act_cnt_log_sqrd = np.log(np.square(forecast_adr_act_cnt))
forecast_cap_mrkt = a * forecast_adr_act_cnt_log_sqrd + b

print(r**2)

# Plotting

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.06, right=0.98, top=0.98, bottom=0.06)


ax.scatter(df_btc['AdrActCnt'], df_btc['CapMrktCurUSD'])
ax.plot(forecast_adr_act_cnt, np.exp(forecast_cap_mrkt), color='gray')

ax.plot(forecast_adr_act_cnt, np.exp(forecast_cap_mrkt - 3 * std), color='green')
ax.plot(forecast_adr_act_cnt, np.exp(forecast_cap_mrkt + 3 * std), color='red')


ax.set_xscale('log')
ax.set_yscale('log')

ax.xaxis.set_major_formatter(ticker.EngFormatter())

ax.yaxis.set_major_locator(ticker.LogLocator(numticks=100))
ax.yaxis.set_major_formatter(CurrencyFormatter)


plt.xlabel('Number of Active Addresses')
plt.ylabel('BTC - Market Cap')
plt.grid(which='major', axis='both', alpha=0.5)
plt.show()