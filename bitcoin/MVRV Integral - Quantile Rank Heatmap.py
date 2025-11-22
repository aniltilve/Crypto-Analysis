import sys
from matplotlib import cm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from coinmetrics.api_client import CoinMetricsClient
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime as dt
from joblib import Parallel, delayed

# Helper functions

def CurrencyFormatter(x, pos):
    if x >= 1e6:
        return '${:,.0f}M'.format(x / 1e6)
    elif x >= 1e3:
        return '${:,.0f}k'.format(x / 1e3)
    elif x >= 1:
        return '${:,.0f}'.format(x)
    elif x >= 1e-2:
        return '{:,.0f}¢'.format(x * 100)
    elif x >= 1e-3:
        return '{:,.1f}¢'.format(x * 100)
    elif x >= 1e-4:
        return '{:,.2f}¢'.format(x * 100)
    else:
        return '{:,.3f}¢'.format(x * 100)
    
def fit_quantile(q, y, X):
    model = sm.QuantReg(y, X).fit(q=q)
    return q, model.predict(X)

def get_quantile_rank(row):
    log_p = row['Log10_MVRV']
    quantile_values = df_preds.loc[row.name]
    return np.mean(log_p > quantile_values)

df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['CapRealUSD', 'CapMrktCurUSD'], page_size=10000).to_dataframe()
df_btc.dropna(inplace=True)
df_btc['time'] = df_btc['time'].dt.tz_localize(None)
df_btc['Index'] = (df_btc['time'] - df_btc['time'].iloc[0]).dt.days + 1
df_btc['Log10_Index'] = np.log10(df_btc['Index'])
df_btc['MVRV'] = df_btc['CapMrktCurUSD'] / df_btc['CapRealUSD']
df_btc['Log10_MVRV'] = df_btc['MVRV'].cumsum()
print(df_btc)

X = sm.add_constant(df_btc['Log10_Index'].astype(float).values.reshape(-1, 1))
y = df_btc['Log10_MVRV'].astype(float).values

quantiles = np.arange(0.0001, 1, 0.0001)


results = Parallel(n_jobs=-1, backend="loky", verbose=5)(
    delayed(fit_quantile)(q, y, X) for q in quantiles
)

df_preds = pd.DataFrame({q: preds for q, preds in results}, index=df_btc.index)

df_btc['Quantile Rank'] = (df_btc['Log10_MVRV'].to_numpy()[:, None] > df_preds.to_numpy()).mean(axis=1)


plt.style.use('dark_background')
fig, ax = plt.subplots(2, 1)
fig.subplots_adjust(left=0.005, right=0.97, top=0.98, bottom=0.04, hspace=0.07)


# Plot MVRV

ax[0].scatter(df_btc['time'], df_btc['MVRV'], c=df_btc['Quantile Rank'], s=3, cmap='RdYlGn_r', zorder=3)

ax[0].scatter(
    df_btc['time'].iloc[-1], 
    df_btc['MVRV'].iloc[-1],
    c=df_btc['Quantile Rank'].iloc[-1],
    norm=plt.Normalize(df_btc['Quantile Rank'].min(), df_btc['Quantile Rank'].max()),
    s=100,
    cmap='RdYlGn_r',
    zorder=4,
    linewidths=4,
    edgecolors=[
        (1, 1, 1, 0.6),
        (1, 1, 1, 0.9)
    ]
)


ax[0].set_yscale('log')


ax[0].yaxis.set_major_locator(ticker.LogLocator(numticks=12))
ax[0].yaxis.set_minor_locator(ticker.LogLocator(subs='all'))
#ax[0].yaxis.set_major_formatter(CurrencyFormatter)

ax[0].format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y=${y:,.5f}')
ax[0].set_ylim(3e-1, 1e1)
ax[0].legend(title='MVRV')


# Plot Quantile Rank

ax[1].scatter(df_btc['time'], df_btc['Quantile Rank'], c=df_btc['Quantile Rank'], s=4, cmap='RdYlGn_r')

ax[1].scatter(
    df_btc['time'].iloc[-1], 
    df_btc['Quantile Rank'].iloc[-1],
    c=df_btc['Quantile Rank'].iloc[-1],
    norm=plt.Normalize(df_btc['Quantile Rank'].min(), df_btc['Quantile Rank'].max()),
    s=100,
    cmap='RdYlGn_r',
    zorder=4,
    linewidths=4,
    edgecolors=[
        (1, 1, 1, 0.6),
        (1, 1, 1, 0.9)
    ]
)

ax[1].yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax[1].set_ylim(0, 1)
ax[1].legend(title='Quantile Rank')

#cbar = fig.colorbar(sc, ax=ax, pad=0.02, fraction=0.08)
#cbar.set_label('Quantile Rank (0 = undervalued, 1 = overvalued)')

dt_start_offset = pd.tseries.offsets.DateOffset(weeks=1)
dt_end_offset = pd.tseries.offsets.DateOffset(months=1)


for axis in ax:
    axis.xaxis.set_major_locator(mdates.YearLocator())
    axis.xaxis.set_minor_locator(mdates.MonthLocator([4, 7, 10]))
    axis.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    axis.grid(which='major', alpha=0.5)
    axis.grid(which='minor', alpha=0.25)
    axis.set_xlim(df_btc['time'].iloc[0] - dt_start_offset, df_btc['time'].iloc[-1] + dt_end_offset)
    axis.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:g}'))
    axis.yaxis.tick_right()
    axis.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y=${y:g}')

ax[0].tick_params(axis='x', labelcolor='none')

plt.show()