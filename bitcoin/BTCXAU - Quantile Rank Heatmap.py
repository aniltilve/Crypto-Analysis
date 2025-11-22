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
    
def fit_quantile(q):
    model = sm.QuantReg(y, X).fit(q=q)
    return q, model.predict(X)

def get_quantile_rank(row):
    log_p = row['Log10_Price']
    quantile_values = df_preds.loc[row.name]
    return np.mean(log_p > quantile_values)

df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_btc = df_btc.drop(columns=['asset'])
df_btc['time'] = df_btc['time'].dt.tz_localize(None)
df_btc['PriceUSD'] = df_btc['PriceUSD'].astype(float)

#days_gen = (df_btc['time'].iloc[0] - dt.datetime(2009, 1, 3)).days
df_btc['Index'] = df_btc.index + 400
df_btc['Log10_Price'] = np.log10(df_btc['PriceUSD'])
df_btc['Log10_Index'] = np.log10(df_btc['Index'])


X = sm.add_constant(df_btc['Log10_Index'].values.reshape(-1, 1))
y = df_btc['Log10_Price'].values

quantiles = np.arange(0.0001, 1, 0.0001)


results = Parallel(n_jobs=-1, backend="loky", verbose=5)(
    delayed(fit_quantile)(q) for q in quantiles
)

df_preds = pd.DataFrame({q: preds for q, preds in results}, index=df_btc.index)

df_btc['Quantile Rank'] = (df_btc['Log10_Price'].values[:, None] > df_preds.values).mean(axis=1)


fig, ax = plt.subplots(2, 1)
fig.subplots_adjust(left=0.045, right=1.0, top=0.98, bottom=0.04, hspace=0.115)

sc = ax[0].scatter(df_btc['time'], df_btc['PriceUSD'], c=df_btc['Quantile Rank'], s=5, cmap='RdYlGn_r', zorder=3)

low_q = quantiles[0]
high_q = quantiles[-1]

# corresponding predictions
low_line = df_preds[low_q]
high_line = df_preds[high_q]

# get the colormap you used for the scatter
cmap = cm.get_cmap('RdYlGn_r')

# lowest and highest colors (0.0 = bottom of colormap, 1.0 = top)
low_color = cmap(0.0)
high_color = cmap(1.0)


# plot them back on the scatter
ax[0].semilogy(df_btc['time'], 10**low_line, color=low_color, lw=1.5, label=f'{low_q:.4f} quantile')
ax[0].semilogy(df_btc['time'], 10**high_line, color=high_color, lw=1.5, label=f'{high_q:.4f} quantile')


#ax[0].set_yscale('log')


ax[0].yaxis.set_major_locator(ticker.LogLocator(numticks=12))
ax[0].yaxis.set_minor_locator(ticker.LogLocator(subs='all'))
ax[0].yaxis.set_major_formatter(CurrencyFormatter)

ax[0].format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y=${y:,.5f}')
ax[0].set_ylim(1e-2, 1e6)

ax[1].plot(df_btc['time'], df_btc['Quantile Rank'])
ax[1].yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax[1].set_ylim(0, 1)

cbar = fig.colorbar(sc, ax=ax, pad=0.02, fraction=0.08)
cbar.set_label('Quantile Rank (0 = undervalued, 1 = overvalued)')

for axis in ax:
    axis.xaxis.set_major_locator(mdates.YearLocator())
    axis.xaxis.set_minor_locator(mdates.MonthLocator([4, 7, 10]))
    axis.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    axis.grid(which='major', alpha=0.5)
    axis.grid(which='minor', alpha=0.25)
    axis.set_xlim(df_btc['time'].iloc[0], df_btc['time'].iloc[-1])

ax[0].tick_params(axis='x', labelcolor='none')

plt.show()