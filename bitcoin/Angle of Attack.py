import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

df_btc = pd.read_csv('/Users/user/Desktop/Python/Bitcoin/BTCUSD.csv')
df_btc['time'] = pd.to_datetime(df_btc['time'])
df_btc['time ordinal'] = (df_btc['time'] - dt.datetime(2009, 1, 3)).dt.days
df_btc['log10 low'] = np.log10(df_btc['low'])
df_btc['log10 high'] = np.log10(df_btc['high'])


fig, ax = plt.subplots()
fig.subplots_adjust(left=0.04, right=0.98, top=0.98, bottom=0.04)

fig_manager = plt.get_current_fig_manager()
fig_manager.resize(3024, 1624)

ax.semilogy(df_btc['time'], df_btc.loc[:, 'open':'close'], color='tab:blue')


'''
2009 - 2011 ANGLE OF ATTACK
'''

trough_2009 = df_btc[df_btc['time'] == '2009-12-17']
peak_2011 = df_btc[df_btc['time'] == '2011-06-08']

opp_g = peak_2011['log10 high'].iloc[0] - trough_2009['log10 low'].iloc[0]
adj_g = peak_2011['time ordinal'].iloc[0] - trough_2009['time ordinal'].iloc[0]
angle_g = math.degrees(np.arctan(opp_g / adj_g * 365))

plt.plot(
    [trough_2009['time'].iloc[0], peak_2011['time'].iloc[0]],
    [trough_2009['low'].iloc[0], trough_2009['low'].iloc[0]], 
    color='black'
)
plt.plot(
    [trough_2009['time'].iloc[0], peak_2011['time'].iloc[0]],
    [trough_2009['low'].iloc[0], peak_2011['high'].iloc[0]], 
    color='black'
)
plt.annotate(
    f'{angle_g:.2f}°', 
    (mdates.date2num(trough_2009['time'].iloc[0]), trough_2009['low'].iloc[0]),
    (mdates.date2num(trough_2009['time'].iloc[0]) + 40, trough_2009['low'].iloc[0] + 0.0001),
    color='red'
)


'''
2011 - 2013 ANGLE OF ATTACK
'''

trough_2011 = df_btc[df_btc['time'] == '2011-11-17']
peak_2013 = df_btc[df_btc['time'] == '2013-11-29']

opp_h1 = peak_2013['log10 high'].iloc[0] - trough_2011['log10 low'].iloc[0]
adj_h1 = peak_2013['time ordinal'].iloc[0] - trough_2011['time ordinal'].iloc[0]
angle_h1 = math.degrees(np.arctan(opp_h1 / adj_h1 * 365))

plt.plot(
    [trough_2011['time'].iloc[0], peak_2013['time'].iloc[0]],
    [trough_2011['low'].iloc[0], trough_2011['low'].iloc[0]], 
    color='black'
)
plt.plot(
    [trough_2011['time'].iloc[0], peak_2013['time'].iloc[0]],
    [trough_2011['low'].iloc[0], peak_2013['high'].iloc[0]], 
    color='black'
)
plt.annotate(
    f'{angle_h1:.2f}°', 
    (mdates.date2num(trough_2011['time'].iloc[0]), trough_2011['low'].iloc[0]),
    (mdates.date2num(trough_2011['time'].iloc[0]) + 50, trough_2011['low'].iloc[0] + 0.2),
    color='red'
)


'''
2015 - 2017 ANGLE OF ATTACK
'''

trough_2015 = df_btc[df_btc['time'] == '2015-08-18']
peak_2017 = df_btc[df_btc['time'] == '2017-12-17']

opp_h2 = peak_2017['log10 high'].iloc[0] - trough_2015['log10 low'].iloc[0]
adj_h2 = peak_2017['time ordinal'].iloc[0] - trough_2015['time ordinal'].iloc[0]
angle_h2 = math.degrees(np.arctan(opp_h2 / adj_h2 * 365))

plt.plot(
    [trough_2015['time'].iloc[0], peak_2017['time'].iloc[0]],
    [trough_2015['low'].iloc[0], trough_2015['low'].iloc[0]], 
    color='black'
)
plt.plot(
    [trough_2015['time'].iloc[0], peak_2017['time'].iloc[0]],
    [trough_2015['low'].iloc[0], peak_2017['high'].iloc[0]], 
    color='black'
)
plt.annotate(
    f'{angle_h2:.2f}°', 
    (mdates.date2num(trough_2015['time'].iloc[0]), trough_2015['low'].iloc[0]),
    (mdates.date2num(trough_2015['time'].iloc[0]) + 70, trough_2015['low'].iloc[0] + 20),
    color='red'
)


'''
2018 - 2021 ANGLE OF ATTACK
'''

trough_2018 = df_btc[df_btc['time'] == '2018-12-15']
peak_2021 = df_btc[df_btc['time'] == '2021-11-10']

opp_h3 = peak_2021['log10 high'].iloc[0] - trough_2018['log10 low'].iloc[0]
adj_h3 = peak_2021['time ordinal'].iloc[0] - trough_2018['time ordinal'].iloc[0]
angle_h3 = math.degrees(np.arctan(opp_h3 / adj_h3 * 365))

plt.plot(
    [trough_2018['time'].iloc[0], peak_2021['time'].iloc[0]],
    [trough_2018['low'].iloc[0], trough_2018['low'].iloc[0]], 
    color='black'
)
plt.plot(
    [trough_2018['time'].iloc[0], peak_2021['time'].iloc[0]],
    [trough_2018['low'].iloc[0], peak_2021['high'].iloc[0]], 
    color='black'
)
plt.annotate(
    f'{angle_h3:.2f}°', 
    (mdates.date2num(trough_2018['time'].iloc[0]), trough_2018['low'].iloc[0]),
    (mdates.date2num(trough_2018['time'].iloc[0]) + 130, trough_2018['low'].iloc[0] + 260),
    color='red'
)


'''
2022 - 2025 ANGLE OF ATTACK
'''

trough_2022 = df_btc[df_btc['time'] == '2022-11-21']
peak_2025 = df_btc[df_btc['time'] == '2025-10-06']

opp_h4 = peak_2025['log10 high'].iloc[0] - trough_2022['log10 low'].iloc[0]
adj_h4 = peak_2025['time ordinal'].iloc[0] - trough_2022['time ordinal'].iloc[0]
angle_h4 = math.degrees(np.arctan(opp_h4 / adj_h4 * 365))

plt.plot(
    [trough_2022['time'].iloc[0], peak_2025['time'].iloc[0]],
    [trough_2022['low'].iloc[0], trough_2022['low'].iloc[0]], 
    color='black'
)
plt.plot(
    [trough_2022['time'].iloc[0], peak_2025['time'].iloc[0]],
    [trough_2022['low'].iloc[0], peak_2025['high'].iloc[0]], 
    color='black'
)
plt.annotate(
    f'{angle_h4:.2f}°', 
    (mdates.date2num(trough_2022['time'].iloc[0]), trough_2022['low'].iloc[0]),
    (mdates.date2num(trough_2022['time'].iloc[0]) + 180, trough_2022['low'].iloc[0] + 1300),
    color='red'
)

print(f'{angle_g}\n{angle_h1}\n{angle_h2}\n{angle_h3}\n{angle_h4}')

plt.xlim(df_btc['time'].iloc[0], df_btc['time'].iloc[-1])
plt.show()