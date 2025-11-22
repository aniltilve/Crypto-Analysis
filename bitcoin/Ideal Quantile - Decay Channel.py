import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from coinmetrics.api_client import CoinMetricsClient
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from scipy.stats import gaussian_kde
import datetime as dt
from scipy.optimize import curve_fit
from joblib import Parallel, delayed

def exp_decay(x, a, b, c):
    return a * np.exp(x * b) + c

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
df_btc['time'] = pd.to_datetime(df_btc['time'])
df_btc.set_index('time', inplace=True)
df_btc = df_btc.stack().reset_index()
df_btc.columns = ['time', 'type', 'price']

df_btc['date index'] = (df_btc['time'] - dt.datetime(2009, 1, 3)).dt.days
df_btc['log10 price'] = np.log10(df_btc['price'])
df_btc['log10 date index'] = np.log10(df_btc['date index'])


X = sm.add_constant(df_btc['log10 date index'].values.reshape(-1, 1))
y = df_btc['log10 price'].values

#q = GetIdealQuantile(y, X, 0.25, 0.35)
q = 0.2941696

model = sm.QuantReg(y, X).fit(q)
log10_fit = model.predict(X)
df_btc['log10 residuals'] = df_btc['log10 price'] - log10_fit
df_high_resid = df_btc[df_btc['type'] == 'high']

df_peaks = df_high_resid[df_high_resid['time'].isin([
    '2011-06-08',
    '2013-11-29',
    '2017-12-17',
    '2021-04-14'
])]

popt, _ = curve_fit(exp_decay, df_peaks['date index'], df_peaks['log10 residuals'], p0=[1.75, -0.0001, 0], maxfev=1000000)

print(popt)

dr_forecast = pd.date_range(df_high_resid['time'].iloc[0], '2040-01-01')
idx_forecast = np.arange(df_high_resid['date index'].iloc[0], df_high_resid['date index'].iloc[0] + len(dr_forecast))
high_forecast = exp_decay(idx_forecast, *popt)

fig3, ax3 = plt.subplots()
ax3.scatter(df_high_resid['time'], df_high_resid['log10 residuals'], label='Residuals')
ax3.plot(df_high_resid['time'], np.zeros(len(df_high_resid)), color='black')
ax3.plot(dr_forecast, high_forecast)


plt.show()