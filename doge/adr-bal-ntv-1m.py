import pandas
import numpy
from scipy import stats
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import matplotlib.dates as dates
import datetime


doge_address_data = pandas.read_csv(r'C:\Users\user\Desktop\Python\doge\DOGE_AdrBalNtv1M.csv', delimiter="\t")
doge_address_data["Date"] = pandas.to_datetime(doge_address_data["Date"])

#regression
ub_data = doge_address_data[(doge_address_data["Date"].isin([
    "2018-07-09",
    "2020-06-30",
    "2020-11-15"
]))]

lb_data = doge_address_data[(doge_address_data["Date"].isin([
    "2017-01-12",
    "2018-09-24",
    "2018-10-15",
    "2021-06-22"
]))]

def modelling_func(x, a, b):
    return a * x + b

startDate = doge_address_data["Date"].loc[doge_address_data["Date"] >= "2015-01-01"]
extendedDates = pandas.date_range(startDate.iloc[0], "2033-01-01")

slope, intercept, r, p, std_err = stats.linregress(ub_data.index.to_list(), ub_data["AddressCount"])
ub_extendedFittedYdata = modelling_func(numpy.array([x+1+startDate.index[0] for x in range(len(extendedDates))]), slope, intercept)

slope, intercept, r, p, std_err = stats.linregress(lb_data.index.to_list(), lb_data["AddressCount"])
lb_extendedFittedYdata = modelling_func(numpy.array([x+1+startDate.index[0] for x in range(len(extendedDates))]), slope, intercept)


#plotting
fig, ax = pyplot.subplots()
ax.grid(axis='both', which='major', color="silver")
ax.grid(axis='both', which='minor', color="gainsboro")
ax.plot(doge_address_data["Date"], doge_address_data["AddressCount"])
pyplot.tick_params(axis='y',which='minor')

fig_manager = pyplot.get_current_fig_manager()
fig_manager.window.showMaximized()

ax.xaxis.set_major_locator(dates.YearLocator(1,month=1,day=1))
ax.xaxis.set_minor_locator(dates.MonthLocator(7))
ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))

ax.yaxis.set_minor_locator(ticker.MultipleLocator(1000))

pyplot.axvline(datetime.datetime(2016,7,9), color="black", label="Bitcoin halving")
pyplot.axvline(datetime.datetime(2020,5,11), color="black")
pyplot.axvline(datetime.datetime(2024,4,22), color="black")

pyplot.plot(extendedDates, ub_extendedFittedYdata, color="lime", label="Upper bound")
pyplot.plot(extendedDates, lb_extendedFittedYdata, color="red", label="Lower bound")

h, l = ax.get_legend_handles_labels()
fig.legend(h, l, loc='upper right')

pyplot.title("Count of addresses with 1 million or more DOGE")
pyplot.xlabel("Date")
pyplot.ylabel("Count of Addresses")
pyplot.ylim(0,10000)
pyplot.xlim(datetime.datetime(2013, 12, 8), datetime.datetime(2033,1,1))
pyplot.show()
