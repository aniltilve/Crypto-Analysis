import pandas
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime

btc_data = pandas.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_Price.csv', delimiter='\t')

btc_data["Date"] = pandas.to_datetime(btc_data["Date"])

halving1 = btc_data.loc[(btc_data["Date"] >= "2012-11-28") & (btc_data["Date"] <= "2016-07-08")]
halving2 = btc_data.loc[(btc_data["Date"] >= "2016-07-09") & (btc_data["Date"] <= "2020-05-10")]
halving3 = btc_data.loc[(btc_data["Date"] >= "2020-05-11") & (btc_data["Date"] <= "2024-04-19")]
halving4 = btc_data.loc[(btc_data["Date"] >= "2024-04-19")]


#plotting
figure, axes = pyplot.subplots()
axes.grid(axis='both', which='major', color="silver")
axes.grid(axis='both', which='minor', color="gainsboro")

mng = pyplot.get_current_fig_manager()
mng.window.showMaximized()

pyplot.semilogy(halving1.index.to_list() - halving1.first_valid_index(), halving1["Price"], label="Halving 1")
pyplot.semilogy(halving2.index.to_list() - halving2.first_valid_index(), halving2["Price"], label="Halving 2")
pyplot.semilogy(halving3.index.to_list() - halving3.first_valid_index(), halving3["Price"], label="Halving 3")
pyplot.semilogy(halving4.index.to_list() - halving4.first_valid_index(), halving4["Price"], label="Halving 3")


halving1_top = halving1.loc[(halving1["Date"] == "2013-12-04")]
halving2_top = halving2.loc[(halving2["Date"] == "2017-12-16")]
halving3_top = halving3.loc[(halving3["Date"] == "2021-11-08")]

pyplot.plot(halving1_top.index - halving1.first_valid_index(), halving1_top["Price"], 'go')
pyplot.plot(halving2_top.index - halving2.first_valid_index(), halving2_top["Price"], 'go')
pyplot.plot(halving3_top.index - halving3.first_valid_index(), halving3_top["Price"], 'go')

halving1_bot = halving1.loc[(halving1["Date"] == "2015-01-14")]
halving2_bot = halving2.loc[(halving2["Date"] == "2018-12-15")]
halving3_bot = halving3.loc[(halving3["Date"] == "2022-11-09")]


pyplot.plot(halving1_bot.index - halving1.first_valid_index(), halving1_bot["Price"], 'ro')
pyplot.plot(halving2_bot.index - halving2.first_valid_index(), halving2_bot["Price"], 'ro')
pyplot.plot(halving3_bot.index - halving3.first_valid_index(), halving3_bot["Price"], 'ro')


axes.xaxis.set_major_formatter(ticker.ScalarFormatter())
axes.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))

handles, labels = axes.get_legend_handles_labels()
figure.legend(handles, labels, loc='upper right')

axes.set_xticks(numpy.linspace(0,1500,16))

pyplot.title("BTC - Price from Halving Date")
pyplot.xlabel("Day")
pyplot.ylabel("Price in USD")
pyplot.xlim(0, 1500)
pyplot.ylim(10,100000)
pyplot.show()