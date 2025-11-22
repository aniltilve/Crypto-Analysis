import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from coinmetrics.api_client import CoinMetricsClient
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from scipy.stats import gaussian_kde
import datetime as dt

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
    
def GetIdealQuantile(y, X, q_start=0.2, q_end=0.6, step=0.01):
    q_ideal = q_start
    lowest_abs_mode = 100
    len_y = len(y) * 10

    for q in np.arange(q_start, q_end + step, step):
        fit = sm.QuantReg(y, X).fit(q).predict(X)
        resid = y - fit
        kde = gaussian_kde(resid)
        kde_xvals = np.linspace(resid.min(), resid.max(), len_y)
        mode_est = np.abs(kde_xvals[np.argmax(kde(kde_xvals))])
        
        if (mode_est < lowest_abs_mode):
            lowest_abs_mode = mode_est
            q_ideal = q
            print(f'The ideal quantile so far is Q{q*100:.7f} with an absolute mode of {mode_est}')

    return q_ideal


df_btc = CoinMetricsClient().get_asset_metrics(assets='BTC', metrics=['PriceUSD'], page_size=10000).to_dataframe()
df_btc = df_btc.drop(columns=['asset'])
df_btc['time'] = df_btc['time'].dt.tz_localize(None)
df_btc['PriceUSD'] = df_btc['PriceUSD'].astype(float)

days_gen = (df_btc['time'].iloc[0] - dt.datetime(2009, 1, 3)).days
df_btc['Index'] = df_btc.index + days_gen
df_btc['Log10_Price'] = np.log10(df_btc['PriceUSD'])
df_btc['Log10_Index'] = np.log10(df_btc['Index'])


X = sm.add_constant(df_btc['Log10_Index'].values.reshape(-1, 1))
y = df_btc['Log10_Price'].values

#q = GetIdealQuantile(y, X, 0.1, 0.4, 0.01)
q = 0.25

model = sm.QuantReg(y, X).fit(q)
log10_fit = model.predict(X)
df_btc['Resid'] = df_btc['Log10_Price'] - log10_fit
df_btc['Resid Rank'] = df_btc['Resid'].rank(pct=True)



dr_forecast= pd.date_range(df_btc['time'].iloc[0], '2030-01-01')
idx_forecast = np.arange(days_gen, days_gen + len(dr_forecast))
log10_idx_forecast = sm.add_constant(np.log10(idx_forecast))
log10_forecast = model.predict(log10_idx_forecast)

norm = plt.Normalize(df_btc['Resid Rank'].min(), df_btc['Resid Rank'].max())
colors = plt.cm.RdYlGn_r(norm(df_btc['Resid Rank']))


fig, ax = plt.subplots()
fig.subplots_adjust(left=0.045, right=0.98, top=0.98, bottom=0.04)
#plt.semilogy(df_doge_price['time'], df_doge_price['PriceUSD'], label="Actual DOGE Price", color='black', zorder=4)

ax.scatter(df_btc['time'], df_btc['PriceUSD'], c=colors, zorder=3)
ax.plot(dr_forecast, np.power(10, log10_forecast), label=f'Q{q*100:.0f} Fit', color='dimgray', linestyle='dashed')

ax.set_yscale('log')

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator([4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.yaxis.set_major_locator(ticker.LogLocator(numticks=12))
ax.yaxis.set_minor_locator(ticker.LogLocator(subs='all'))
ax.yaxis.set_major_formatter(CurrencyFormatter)

ax.format_coord = (lambda x, y: f'x={mdates.num2date(x):%Y-%m-%d}, y=${y:,.5f}')

# Formatting the plot
plt.xlim(df_btc['time'].iloc[0], dr_forecast[-1])
plt.ylim(1e-2, 1e6)
plt.grid(which='major', alpha=0.5)
plt.grid(which='minor', alpha=0.25)
plt.legend()
plt.show()