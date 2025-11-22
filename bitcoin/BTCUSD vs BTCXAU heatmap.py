import pandas as pd
from joblib import Parallel, delayed
import numpy as np
import statsmodels.api as sm
import datetime as dt
from matplotlib import (
    dates as mdates,
    pyplot as plt,
    ticker as ticker
)

def fit_quantile(q, y, X):
    model = sm.QuantReg(y, X).fit(q=q)
    return q, model.predict(X)


df_btcusd = pd.read_csv('./Bitcoin/BTCUSD.csv')
df_btcxau = pd.read_csv('./Bitcoin/BTCXAU.csv')

df_btcusd = df_btcusd.rename(columns={'close':'BTCUSD'})
df_btcxau = df_btcxau.rename(columns={'close':'BTCXAU'})

df_btcusd = df_btcusd.drop(columns=['open', 'low', 'high'])
df_btcxau = df_btcxau.drop(columns=['open', 'low', 'high'])

df_merge = df_btcusd.merge(df_btcxau, 'inner', 'time')
df_merge['time'] = pd.to_datetime(df_merge['time'])
df_merge['Index'] = (df_merge['time'] - dt.datetime(2009, 1, 3)).dt.days
df_merge['Log10 Index'] = np.log10(df_merge['Index'])
df_merge['Log10 BTCUSD'] = np.log10(df_merge['BTCUSD'])
df_merge['Log10 BTCXAU'] = np.log10(df_merge['BTCXAU'])

X_BTCUSD = sm.add_constant(df_merge['Log10 Index'].values.reshape(-1, 1))
X_BTCXAU = sm.add_constant(df_merge['Log10 Index'].values.reshape(-1, 1))

y_BTCUSD = df_merge['Log10 BTCUSD']
y_BTCXAU = df_merge['Log10 BTCXAU']

quantiles = np.arange(0.0001, 1, 0.0001)

results_usd = Parallel(n_jobs=-1, backend="loky", verbose=5)(
    delayed(fit_quantile)(q, y_BTCUSD, X_BTCUSD) for q in quantiles
)

df_preds_usd = pd.DataFrame({q: preds for q, preds in results_usd}, index=df_merge.index)

df_merge['Quantile Rank USD'] = (df_merge['Log10 BTCUSD'].to_numpy()[:, None] > df_preds_usd.to_numpy()).mean(axis=1)


results_xau = Parallel(n_jobs=-1, backend="loky", verbose=5)(
    delayed(fit_quantile)(q, y_BTCXAU, X_BTCXAU) for q in quantiles
)

df_preds_xau = pd.DataFrame({q: preds for q, preds in results_xau}, index=df_merge.index)

df_merge['Quantile Rank XAU'] = (df_merge['Log10 BTCXAU'].to_numpy()[:, None] > df_preds_xau.to_numpy()).mean(axis=1)


plt.style.use('dark_background')
fig, ax = plt.subplots(2, 1)
fig.subplots_adjust(left=0.005, right=0.97, top=0.98, bottom=0.04, hspace=0.07)


ax[0].scatter(df_merge['time'], df_merge['Quantile Rank USD'], c=df_merge['Quantile Rank USD'], s=3, cmap='RdYlGn_r', zorder=3)

ax[0].scatter(
    df_merge['time'].iloc[-1], 
    df_merge['Quantile Rank USD'].iloc[-1],
    c=df_merge['Quantile Rank USD'].iloc[-1],
    norm=plt.Normalize(df_merge['Quantile Rank USD'].min(), df_merge['Quantile Rank USD'].max()),
    s=100,
    cmap='RdYlGn_r',
    zorder=4,
    linewidths=4,
    edgecolors=[
        (1, 1, 1, 0.6),
        (1, 1, 1, 0.9)
    ]
)

ax[1].scatter(df_merge['time'], df_merge['Quantile Rank XAU'], c=df_merge['Quantile Rank XAU'], s=3, cmap='RdYlGn_r', zorder=3)

ax[1].scatter(
    df_merge['time'].iloc[-1], 
    df_merge['Quantile Rank XAU'].iloc[-1],
    c=df_merge['Quantile Rank XAU'].iloc[-1],
    norm=plt.Normalize(df_merge['Quantile Rank XAU'].min(), df_merge['Quantile Rank XAU'].max()),
    s=100,
    cmap='RdYlGn_r',
    zorder=4,
    linewidths=4,
    edgecolors=[
        (1, 1, 1, 0.6),
        (1, 1, 1, 0.9)
    ]
)

dt_start_offset = pd.tseries.offsets.DateOffset(weeks=1)
dt_end_offset = pd.tseries.offsets.DateOffset(months=1)


for axis in ax:
    axis.xaxis.set_major_locator(mdates.YearLocator())
    axis.xaxis.set_minor_locator(mdates.MonthLocator([4, 7, 10]))
    axis.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    axis.grid(which='major', alpha=0.5)
    axis.grid(which='minor', alpha=0.25)
    axis.set_xlim(df_merge['time'].iloc[0] - dt_start_offset, df_merge['time'].iloc[-1] + dt_end_offset)
    axis.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:g}'))
    axis.yaxis.tick_right()
    axis.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y=${y:g}')

plt.show()