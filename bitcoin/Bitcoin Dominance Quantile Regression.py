import sys
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime
import os
from scipy.stats import gaussian_kde
import statsmodels.api as sm
from joblib import Parallel, delayed



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


df_btc_d = pd.read_csv('/Users/user/Desktop/Python/Bitcoin/BTC_Dominance.csv')
df_btc_d['time'] = pd.to_datetime(df_btc_d['time'])
df_btc_d.set_index('time', inplace=True)
df_btc_d = df_btc_d.stack().reset_index()
df_btc_d.columns = ['time', 'type', 'dominance']
df_btc_d['date index'] = (df_btc_d['time'] - df_btc_d['time'].iloc[0]).dt.days


X = sm.add_constant(df_btc_d['date index'].values.reshape(-1, 1))
y = df_btc_d['dominance'].values

q_ideal = GetIdealQuantile(y, X)
#q_ideal = 0.55

model = sm.QuantReg(y, X).fit(q_ideal)
fit = model.predict(X)
resid = df_btc_d['dominance'] - fit

dr_forecast = pd.date_range(df_btc_d['time'].iloc[0], '2030-01-01')
idx_forecast = sm.add_constant(np.arange(len(dr_forecast)))
forecast = model.predict(idx_forecast)

p0 = np.percentile(resid, 0)
p10 = np.percentile(resid, 10)

p90 = np.percentile(resid, 90)
p100 = np.percentile(resid, 100)

#plotting
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.055, right=0.98, top=0.98, bottom=0.04)
ax.grid(axis='both', which='major', color='silver')
ax.grid(axis='both', which='minor', color='gainsboro')
plt.tick_params(axis='y',which='minor')


ax.plot(df_btc_d['time'], df_btc_d['dominance'], zorder=4)
ax.plot(dr_forecast, forecast)

ax.plot(dr_forecast, forecast + p0, color='tab:green', label='No chance of going lower')
ax.plot(dr_forecast, forecast + p10, color='tab:green', linestyle='dashed', label='10% chance of going lower')

ax.plot(dr_forecast, forecast + p90, color='tab:red', linestyle='dashed', label='10% chance of going higher')
ax.plot(dr_forecast, forecast + p100, color='tab:red', label='No chance of going higher')

ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))

ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y={y:,.2f}%')

plt.ylabel('Bitcoin Dominance')
plt.xlim(df_btc_d['time'].iloc[0], datetime.datetime(2030,1,1))
plt.ylim(0,100)
plt.show()