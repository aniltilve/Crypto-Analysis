import pandas
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime

btcData = pandas.read_csv(r'C:\Users\user\Desktop\Python\bitcoin\BTC_Price.csv', delimiter="\t")
btcData["Date"] = pandas.to_datetime(btcData["Date"])


#plotting
figure, axes = pyplot.subplots()
axes.grid(axis='y', which='major', color="silver")
pyplot.yscale('log', subsy=[1])
pyplot.tick_params(axis='y',which='minor')

mng = pyplot.get_current_fig_manager()
mng.window.showMaximized()


alpha_factor = 0.8

axes.semilogy(btcData["Date"], btcData["Price"], color="black")

genesis_trough = datetime.datetime(2011,11,18)

halving1 = datetime.datetime(2012,11,28)
halving1_peak = datetime.datetime(2013,12,4)
halving1_trough = datetime.datetime(2015,1,14)

halving2 = datetime.datetime(2016,7,9)
halving2_peak = datetime.datetime(2017,12,16)
halving2_trough = datetime.datetime(2018,12,15)

halving3 = datetime.datetime(2020,5,11)
halving3_peak = datetime.datetime(2021,11,8)
halving3_trough = datetime.datetime(2022,11,9)

halving4 = datetime.datetime(2024,4,18)

pyplot.axvline(halving1, color="black")
pyplot.axvline(halving2, color="black")
pyplot.axvline(halving3, color="black")
pyplot.axvline(halving4, color="black")


# Genesis Trough - Halving 1
axes.fill_betweenx(
    y=numpy.arange(0.01,1000000,5),
    x1=genesis_trough,
    x2=halving1,
    color="lightgreen",
    alpha=alpha_factor
)

axes.text(
    genesis_trough + (halving1 - genesis_trough) / 2, 
    500000, 
    "{0} days\n{1:.2f}x".format(
        (halving1 - genesis_trough).days,
        btcData.loc[btcData["Date"] == halving1,"Price"].values[0] / btcData.loc[btcData["Date"] == genesis_trough,"Price"].values[0]
    ), 
    color="white",
    horizontalalignment="center",
    verticalalignment="center"
)

# Halving 1 - Halving 1 Peak
axes.fill_betweenx(
    y=numpy.arange(0.01,1000000,5),
    x1=halving1,
    x2=halving1_peak,
    color="limegreen",
    alpha=alpha_factor
)

axes.text(
    halving1 + (halving1_peak - halving1) / 2, 
    500000, 
    "{0} days\n{1:.2f}x".format(
        (halving1_peak - halving1).days,
        btcData.loc[btcData["Date"] == halving1_peak,"Price"].values[0] / btcData.loc[btcData["Date"] == halving1,"Price"].values[0]
    ), 
    color="white",
    horizontalalignment="center",
    verticalalignment="center"
)

# Halving 1 Peak - Halving 1 Trough
axes.fill_betweenx(
    y=numpy.arange(0.01,1000000,5),
    x1=halving1_peak,
    x2=halving1_trough,
    color="red",
    alpha=alpha_factor
)

axes.text(
    halving1_peak + (halving1_trough - halving1_peak) / 2, 
    500000, 
    "{0} days\n{1:.2f}x".format(
        (halving1_trough - halving1_peak).days,
        btcData.loc[btcData["Date"] == halving1_trough,"Price"].values[0] / btcData.loc[btcData["Date"] == halving1_peak,"Price"].values[0]
    ), 
    color="white",
    horizontalalignment="center",
    verticalalignment="center"
)

# Halving 1 Trough - Halving 2
axes.fill_betweenx(
    y=numpy.arange(0.01,1000000,5),
    x1=halving1_trough,
    x2=halving2,
    color="lightgreen",
    alpha=alpha_factor
)

axes.text(
    halving1_trough + (halving2 - halving1_trough) / 2, 
    500000, 
    "{0} days\n{1:.2f}x".format(
        (halving2 - halving1_trough).days,
        btcData.loc[btcData["Date"] == halving2,"Price"].values[0] / btcData.loc[btcData["Date"] == halving1_trough,"Price"].values[0]
    ), 
    color="white",
    horizontalalignment="center",
    verticalalignment="center"
)

# Halving 2 - Halving 2 Peak
axes.fill_betweenx(
    y=numpy.arange(0.01,1000000,5),
    x1=halving2,
    x2=halving2_peak,
    color="limegreen",
    alpha=alpha_factor
)

axes.text(
    halving2 + (halving2_peak - halving2) / 2, 
    500000, 
    "{0} days\n{1:.2f}x".format(
        (halving2_peak - halving2).days,
        btcData.loc[btcData["Date"] == halving2_peak,"Price"].values[0] / btcData.loc[btcData["Date"] == halving2,"Price"].values[0]
    ), 
    color="white",
    horizontalalignment="center",
    verticalalignment="center"
)

# Halving 2 Peak - Halving 2 Trough
axes.fill_betweenx(
    y=numpy.arange(0.01,1000000,5),
    x1=halving2_peak,
    x2=halving2_trough,
    color="red",
    alpha=alpha_factor
)

axes.text(
    halving2_peak + (halving2_trough - halving2_peak) / 2, 
    500000, 
    "{0} days\n{1:.2f}x".format(
        (halving2_trough - halving2_peak).days,
        btcData.loc[btcData["Date"] == halving2_trough,"Price"].values[0] / btcData.loc[btcData["Date"] == halving2_peak,"Price"].values[0]
    ), 
    color="white",
    horizontalalignment="center",
    verticalalignment="center"
)

# Halving 2 Trough - Halving 3
axes.fill_betweenx(
    y=numpy.arange(0.01,1000000,5),
    x1=halving2_trough,
    x2=halving3,
    color="lightgreen",
    alpha=alpha_factor
)

axes.text(
    halving2_trough + (halving3 - halving2_trough) / 2, 
    500000, 
    "{0} days\n{1:.2f}x".format(
        (halving3 - halving2_trough).days,
        btcData.loc[btcData["Date"] == halving3,"Price"].values[0] / btcData.loc[btcData["Date"] == halving2_trough,"Price"].values[0]
    ), 
    color="white",
    horizontalalignment="center",
    verticalalignment="center"
)

# Halving 3 - Halving 3 Peak
axes.fill_betweenx(
    y=numpy.arange(0.01,1000000,5),
    x1=halving3,
    x2=halving3_peak,
    color="limegreen",
    alpha=alpha_factor
)

axes.text(
    halving3 + (halving3_peak - halving3) / 2, 
    500000, 
    "{0} days\n{1:.2f}x".format(
        (halving3_peak - halving3).days,
        btcData.loc[btcData["Date"] == halving3_peak,"Price"].values[0] / btcData.loc[btcData["Date"] == halving3,"Price"].values[0]
    ), 
    color="white",
    horizontalalignment="center",
    verticalalignment="center"
)

# Halving 3 Peak - Halving 3 Trough
axes.fill_betweenx(
    y=numpy.arange(0.01,1000000,5),
    x1=halving3_peak,
    x2=halving3_trough,
    color="red",
    alpha=alpha_factor
)

axes.text(
    halving3_peak + (halving3_trough - halving3_peak) / 2, 
    500000, 
    "{0} days\n{1:.2f}x".format(
        (halving3_trough - halving3_peak).days,
        btcData.loc[btcData["Date"] == halving3_trough,"Price"].values[0] / btcData.loc[btcData["Date"] == halving3_peak,"Price"].values[0]
    ), 
    color="white",
    horizontalalignment="center",
    verticalalignment="center"
)


# Halving 3 Trough - Halving 4
axes.fill_betweenx(
    y=numpy.arange(0.01,1000000,5),
    x1=halving3_trough,
    x2=halving4,
    color="lightgreen",
    alpha=alpha_factor
)

axes.text(
    halving3_trough + (halving4 - halving3_trough) / 2, 
    500000, 
    "{0} days\n{1:.2f}x".format(
        (halving4 - halving3_trough).days,
        btcData.loc[btcData["Date"] == halving4,"Price"].values[0] / btcData.loc[btcData["Date"] == halving3_trough,"Price"].values[0]
    ), 
    color="white",
    horizontalalignment="center",
    verticalalignment="center"
)

'''
axes.text(
    halving3_trough + (halving4 - halving3_trough) / 2, 
    500000, 
    "{0} days\n{1:.2f}x".format(
        (halving4 - halving3_trough).days,
        btcData.loc[btcData["Date"] == halving4,"Price"].values[0] / btcData.loc[btcData["Date"] == halving3_trough,"Price"].values[0]
    ), 
    color="white",
    horizontalalignment="center",
    verticalalignment="center"
)
'''

axes.xaxis.set_major_locator(dates.YearLocator(1,month=1,day=1))
axes.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
axes.xaxis.set_minor_locator(dates.MonthLocator(7))
axes.xaxis.set_major_formatter(dates.DateFormatter('%Y'))

axes.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.2f}'))

pyplot.title("BTC price - bull ratio")
pyplot.ylabel("Price in USD")
pyplot.ylim(0.01,1000000)
pyplot.xlim(datetime.datetime(2010, 7, 1), datetime.datetime(2026,1,1))
pyplot.show()