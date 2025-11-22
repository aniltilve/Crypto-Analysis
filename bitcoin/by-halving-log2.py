import pandas
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime

btc_data = pandas.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_Price.csv', delimiter="\t")

btc_data_early = pandas.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_Price.csv')

btc_data["Date"] = pandas.to_datetime(btc_data["Date"])
btc_data_early["Date"] = pandas.to_datetime(btc_data["Date"])

btc_data = btc_data.merge(btc_data_early, on='Date', how='left')
#btc_data.reset_index()

halving1 = btc_data.loc[(btc_data["Date"] >= "2012-11-28") & (btc_data["Date"] <= "2016-07-09")]
halving2 = btc_data.loc[(btc_data["Date"] >= "2016-07-09") & (btc_data["Date"] <= "2020-05-11")]
halving3 = btc_data.loc[(btc_data["Date"] >= "2020-05-11") & (btc_data["Date"] <= "2024-04-19")]
halving4 = btc_data.loc[(btc_data["Date"] >= "2024-04-19")]


#plotting
figure, axes = pyplot.subplots()
figure.subplots_adjust(left=0.08, right=0.99, top=0.98, bottom=0.04)
axes.grid(axis='both', which='major', color="silver")
axes.grid(axis='both', which='minor', color="gainsboro")

mng = pyplot.get_current_fig_manager()
mng.window.showMaximized()

pyplot.plot(halving1.index.to_list() - halving1.first_valid_index(), halving1["Price"], label="Halving 1")
pyplot.plot(halving2.index.to_list() - halving2.first_valid_index(), halving2["Price"], label="Halving 2")
pyplot.plot(halving3.index.to_list() - halving3.first_valid_index(), halving3["Price"], label="Halving 3")
pyplot.plot(halving4.index.to_list() - halving4.first_valid_index(), halving4["Price"], label="Halving 4")


halving1_top = halving1.loc[(halving1["Date"] == "2013-12-04")]
halving2_top = halving2.loc[(halving2["Date"] == "2017-12-16")]
halving3_top = halving3.loc[(halving3["Date"] == "2021-11-08")]

pyplot.plot(halving1_top.index - halving1.first_valid_index(), halving1_top["Price"], 'go')
pyplot.plot(halving2_top.index - halving2.first_valid_index(), halving2_top["Price"], 'go')
pyplot.plot(halving3_top.index - halving3.first_valid_index(), halving3_top["Price"], 'go')

halving1_bot = halving1.loc[(halving1["Date"] == "2015-01-14")]
halving2_bot = halving2.loc[(halving2["Date"] == "2018-12-15")]
halving3_bot = halving3.loc[(halving3["Date"] == "2022-11-21")]

pyplot.plot(halving1_bot.index - halving1.first_valid_index(), halving1_bot["Price"], 'ro')
pyplot.plot(halving2_bot.index - halving2.first_valid_index(), halving2_bot["Price"], 'ro')
pyplot.plot(halving3_bot.index - halving3.first_valid_index(), halving3_bot["Price"], 'ro')

pyplot.yscale('symlog', basey=2)

axes.xaxis.set_major_locator(ticker.MultipleLocator(250))
axes.xaxis.set_minor_locator(ticker.MultipleLocator(50))
axes.xaxis.set_major_formatter(ticker.ScalarFormatter())
axes.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))

pyplot.ylabel("BTC - Closing Price in USD from Day of Halving")
pyplot.xlim(0, 1450)
pyplot.ylim(8, 131072)
pyplot.legend(title="Legend")
pyplot.show()