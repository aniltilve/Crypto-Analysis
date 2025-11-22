import pandas
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime

btc_data = pandas.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_Price_BlockHeight.csv')

btc_data["Date_Price"] = pandas.to_datetime(btc_data["Date_Price"])
btc_data["Date_BlockHeight"] = pandas.to_datetime(btc_data["Date_BlockHeight"])

halving1 = btc_data.loc[(btc_data["BlockHeight"] >= 210000) & (btc_data["BlockHeight"] < 420000)]
halving2 = btc_data.loc[(btc_data["BlockHeight"] >= 420000) & (btc_data["BlockHeight"] < 630000)]
halving3 = btc_data.loc[(btc_data["BlockHeight"] >= 630000)]

#plotting
figure, axes = pyplot.subplots()
axes.grid(axis='both', which='major', color="silver")
axes.grid(axis='both', which='minor', color="gainsboro")

mng = pyplot.get_current_fig_manager()
mng.window.showMaximized()

pyplot.semilogy(halving1["BlockHeight"] - 210000, halving1["Price"], label="Halving 1")
pyplot.semilogy(halving2["BlockHeight"] - 420000, halving2["Price"], label="Halving 2")
pyplot.semilogy(halving3["BlockHeight"] - 630000, halving3["Price"], label="Halving 3")

halving1_top = halving1.loc[(halving1["Date_Price"] == "2013-12-04")]
halving2_top = halving2.loc[(halving2["Date_Price"] == "2017-12-16")]
halving3_top = halving3.loc[(halving3["Date_Price"] == "2021-11-08")]

pyplot.plot(halving1_top["BlockHeight"] - 210000, halving1_top["Price"], 'go')
pyplot.plot(halving2_top["BlockHeight"] - 420000, halving2_top["Price"], 'go')
pyplot.plot(halving3_top["BlockHeight"] - 630000, halving3_top["Price"], 'go')

halving1_bot = halving1.loc[(halving1["Date_Price"] == "2015-01-14")]
halving2_bot = halving2.loc[(halving2["Date_Price"] == "2018-12-15")]

pyplot.plot(halving1_bot["BlockHeight"] - 210000, halving1_bot["Price"], 'ro')
pyplot.plot(halving2_bot["BlockHeight"] - 420000, halving2_bot["Price"], 'ro')


axes.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.2f}'))

handles, labels = axes.get_legend_handles_labels()
figure.legend(handles, labels, loc='upper right')

axes.set_xticks(numpy.linspace(0,210000,11))

pyplot.title("BTC - Price from Halving Date (in Blocks)")
pyplot.xlabel("Block # (relative to halving)")
pyplot.ylabel("Price in USD")
pyplot.xlim(0, 210000)
pyplot.ylim(10,100000)
pyplot.show()