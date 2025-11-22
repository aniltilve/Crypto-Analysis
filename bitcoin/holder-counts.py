from coinmetrics.api_client import CoinMetricsClient
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

def fmt_func(x, pos):
    if x >= 1e6:
        return '{:,.0f}M'.format(x / 1e6)
    elif x >= 1e3:
        return '{:,.0f}k'.format(x / 1e3)
    else:
        return '{:,.0f}'.format(x)

client = CoinMetricsClient()

df_btc_holder_counts = client.get_asset_metrics(
    assets="BTC",
    metrics=[
        "AdrBalCnt",
        "AdrBalNtv0.001Cnt",
        "AdrBalNtv0.01Cnt",
        "AdrBalNtv0.1Cnt",
        "AdrBalNtv1Cnt",
        "AdrBalNtv10Cnt",
        "AdrBalNtv100Cnt",
        "AdrBalNtv1KCnt",
        "AdrBalNtv10KCnt"
    ],
).parallel().to_dataframe()

df_btc_holder_counts = df_btc_holder_counts.rename(columns={
    "AdrBalCnt" : "Any BTC",
    "AdrBalNtv0.001Cnt" : ">= 0.001 BTC",
    "AdrBalNtv0.01Cnt" : ">= 0.01 BTC",
    "AdrBalNtv0.1Cnt" : ">= 0.1 BTC",
    "AdrBalNtv1Cnt" : ">= 1 BTC",
    "AdrBalNtv10Cnt" : ">= 10 BTC",
    "AdrBalNtv100Cnt" : ">= 100 BTC",
    "AdrBalNtv1KCnt" : ">= 1K BTC",
    "AdrBalNtv10KCnt" : ">= 10K BTC",
})

figure, ax = plt.subplots()
figure.subplots_adjust(left=0.055, right=0.99, top=0.985, bottom=0.07)
ax.grid(axis='both', which='major', color="silver")
ax.grid(axis='both', which='minor', color="gainsboro")
plt.tick_params(axis='y', which='minor')

plt.semilogy(df_btc_holder_counts["time"], df_btc_holder_counts.loc[:,"Any BTC":], label=df_btc_holder_counts.columns[2:].values)
#plt.stackplot(df_btc_holder_counts["time"], df_btc_holder_counts.loc[:,"Any BTC":].astype(float).T, labels=df_btc_holder_counts.columns[2:].values)
#plt.yscale('log')

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

ax.yaxis.set_major_locator(ticker.LogLocator(numticks=18))
ax.yaxis.set_minor_locator(ticker.LogLocator(subs="all"))
ax.yaxis.set_major_formatter(fmt_func)

plt.xlabel("Date")
plt.ylabel("Address Count")
plt.ylim(1, 1e8)
plt.xlim(dt.datetime(2009, 1, 1), dt.date.today())
plt.legend(title="Balance")
plt.show()