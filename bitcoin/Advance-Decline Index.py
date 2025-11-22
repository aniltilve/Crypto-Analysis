from coinmetrics.api_client import CoinMetricsClient
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.dates as mdates
from joblib import Parallel, delayed
import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.special import inv_boxcox
from scipy.stats import gaussian_kde
import statsmodels.api as sm


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


# Data ETL
df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_btc['time'] = pd.to_datetime(df_btc['time']).dt.tz_localize(None)
df_btc['Price Direction'] = np.sign(df_btc['PriceUSD'].diff())
df_btc['Price Direction'].iloc[0] = 0
df_btc['ADI'] = df_btc['Price Direction'].cumsum()


X = sm.add_constant(df_btc.index.values.reshape(-1, 1))
y = df_btc['ADI']

q_ideal = GetIdealQuantile(y, X)
#q_ideal = 0.55

model = sm.QuantReg(y, X).fit(q_ideal)
fit = model.predict(X)

# Plotting 
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.043, right=0.98, top=0.98, bottom=0.04)
ax.grid(axis='both', which='major', color='silver', zorder=1)
ax.grid(axis='both', which='minor', color='gainsboro', zorder=1)



ax.plot(df_btc['time'], df_btc['ADI'], zorder=4, label='ADI')
ax.plot(df_btc['time'], fit, zorder=4, label='fit')


ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.xlim(df_btc['time'].iloc[0], df_btc['time'].iloc[-1])
#plt.ylim(0)
plt.show()