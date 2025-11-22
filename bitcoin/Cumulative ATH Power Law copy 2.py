import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.lines as mlines
import matplotlib.dates as mdates
import datetime as dt
from coinmetrics.api_client import CoinMetricsClient
import scipy.stats as stats
import statsmodels.api as sm
from scipy.stats import gaussian_kde
from joblib import Parallel, delayed

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
    else:
        return '{:,.2f}¢'.format(x * 100)

def FitAndScore(model, X, y, q, kde_points=200):
    # Fit model at quantile q
    fit = model.fit(q=q).predict(X)
    resid = y - fit

    # KDE with limited evaluation points
    kde = gaussian_kde(resid)
    kde_xvals = np.linspace(resid.min(), resid.max(), kde_points)
    mode_est = np.abs(kde_xvals[np.argmax(kde(kde_xvals))])

    return q, mode_est


def GetIdealQuantile(y, X, q_start=0.01, q_end=0.99):
    step=0.01
    model = sm.QuantReg(y, X)
    q_ideal = q_start
    lowest_abs_mode = np.inf

    for iteration in range(17):
        q_values = np.arange(q_start, q_end + step, step)

        # Run fits in parallel
        results = Parallel(n_jobs=-1)(
            delayed(FitAndScore)(model, X, y, q, len(y)) for q in q_values
        )

        for q, mode_est in results:
            if mode_est < lowest_abs_mode:
                lowest_abs_mode = mode_est
                q_ideal = q
                print(f'The ideal quantile so far is Q{q*100:.{iteration}f} with an absolute mode of {mode_est}')
        
        if -int(np.floor(np.log10(step*100))) >= 17:
                return q_ideal

        # Narrow the search range
        q_start = q_ideal - step
        q_end = q_ideal + step
        step /= 10

    return q_ideal

df_btc = pd.read_csv('./Bitcoin/BTCUSD.csv')
df_btc['time'] = pd.to_datetime(df_btc['time']).dt.tz_localize(None)
df_btc['high'] = df_btc['high'].astype(float)
df_btc['Date Index'] = (df_btc['time'] - df_btc['time'].min()).dt.days + 1
df_btc['CumMax'] = df_btc['high'].cummax()
df_btc = df_btc[(df_btc['CumMax'] == df_btc['high'])]
df_btc['Log_Index'] = np.log10(df_btc['Date Index'])
df_btc['Log_CumMax'] = np.log10(df_btc['CumMax'])

X = sm.add_constant(df_btc['Log_Index'].values.reshape(-1, 1))
y = df_btc['Log_CumMax'].values


model = sm.QuantReg(y, X).fit(0.99)
log10_fit = model.predict(X)
resid = df_btc['Log_CumMax'] - log10_fit

p0 = np.percentile(resid, 0)
p1 = np.percentile(resid, 1)
p5 = np.percentile(resid, 5)
p10 = np.percentile(resid, 10)

p75 = np.percentile(resid, 75)
p90 = np.percentile(resid, 90)
p95 = np.percentile(resid, 95)
p99 = np.percentile(resid, 99)
p100 = np.percentile(resid, 100)

#days_gen = (df_btc['time'].iloc[0] - df).days
dr_forecast= pd.date_range(df_btc['time'].iloc[0], '2035-01-01')
idx_forecast = np.arange(1, 1 + len(dr_forecast))
log10_idx_forecast = sm.add_constant(np.log10(idx_forecast))
log10_forecast = model.predict(log10_idx_forecast)


fig, ax = plt.subplots()
fig.subplots_adjust(left=0.04, right=0.98, top=0.98, bottom=0.04)

fig_manager = plt.get_current_fig_manager()
fig_manager.resize(3024, 1624)

ax.scatter(df_btc['time'], df_btc['CumMax'], zorder=4, label='BTC - Cumulative All Time High in USD')
ax.semilogy(dr_forecast, np.power(10, log10_forecast), zorder=3, label=f'Quantile Q99 Fit')
#ax.semilogy(dr_forecast, np.power(10, log10_forecast + p5), color='tab:green', zorder=3, linestyle='dashed', label='5% chance of going lower')
#ax.semilogy(dr_forecast, np.power(10, log10_forecast + p95), color='tab:red', zorder=3, linestyle='dashed', label='5% chance of going higher')


ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator([4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.LogLocator(numticks=500))
ax.yaxis.set_minor_locator(ticker.LogLocator(numticks=500))
ax.yaxis.set_major_formatter(CurrencyFormatter)

ax.grid(which='major', alpha=0.5)
ax.grid(which='minor', alpha=0.25)
ax.legend()

plt.ylim(1e-4, 1e7)
plt.show()