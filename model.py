"""
Model class for application.

MVC template from:
  https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/
"""


import math
import datetime
from datetime import datetime as dt
from tkinter import messagebox  # use Tkinter for python 2, tkinter for python 3
import numpy as np
import algorithms.algo1
import algorithms.algo2
import algorithms.algo3
import algorithms.algo4
import urllib.request
from enum import Enum


class StockSite(Enum):
    unknown = 0
    yahoo = 1
    google1 = 2  # https://www.google.com/finance/getprices
    google2 = 3  # http://www.google.com/finance/historical


class Model():
    'Model class of the MVC architecture.'
    def __init__(self):
        'Constructor'
        self.str_stock_symbol = "ZIOP"                   # example stock symbol
        self.start_date = datetime.date(2016, 1, 1)     # example date just to start app with
        self.end_date = datetime.date(2016, 12, 31)     # will be overridden later in the view class
        self.str_investment = "4000"                    # example starting investment, in dollars
        self.pcntl = []        # portfolio control (see book for explanation)
        self.cash = []         # cash on hand
        self.pv = []           # portfolio value
        self.sv = []           # stock value
        self.shares_owned = []  # number of stock shares owned
        self.order = []        # amount of a buy or sell order, in dollars
        self.num_trans = 0      # number of transactions (buy or sell orders) made
        self.num_data_points = 0 # number of data points in our list of stock prices (a convenience, it is used a lot)
        self.quotes = []       # a large list to hold all stock data retrieved from the Internet, not just the closing prices
        self.closes = []       # the stock prices we save are the 'closing' prices for each trading day
        self.ave_5_days = []     # the 'aveNdays' lists are used for graphing moving averages of the stock prices
        self.ave_11_days = []
        self.ave_21_days = []
        self.ave_41_days = []
        self.ave_81_days = []
        self.ave_161_days = []
        self.ave_251_days = []
        self.annual_ROI = 0.0   # annualized return on investment
        self.bLoop_on_param1 = False
        self.bLoop_on_param2 = False
        self.bLoop_on_param3 = False
        self.bLoop_on_param4 = False
        self.num_days = 0
        self.stockURLSite = StockSite.google2

        self.opt_param1 = 0.052
        self.opt_param2 = 0.80
        self.opt_param3 = 0.0
        self.opt_param4 = 0.0
        self.horz_size = 9.0  # in inches; dpi = 80

    def __del__(self):
        'Destructor, just to see if/when it gets called'
        print(id(self), 'died')


    def calc_ROI(self, start_date, end_date):
        'Calculate the annualized return on investment'
        delta = end_date - start_date   # get delta between start and stop dates
        years = delta.days / 365.25   # calc number of years that passed over time range
        x = self.pv[len(self.pv)-1] / self.pv[0]  # ratio of ending pv to starting pv
        y = 1.0 / years               # get inverse of years
        z = (math.pow(x, y)) - 1      # x to the y power, then minus 1
        z = z * 100.0                 # convert to percent
        z = round(z, 2)               # round off
        return z

    def convertStringDateToOrdinal(self, strDate):
        'Convert date in string format to a date ordinal'
        list1 = strDate.split("-")
        intYear = int(list1[2])
        if intYear < 80:
            intYear += 2000
        else:
            intYear += 1900
        list1[2] = str(intYear)
        newStrDate = list1[0] + "-" + list1[1] + "-" + list1[2]
        dateObj = dt.strptime(newStrDate, "%d-%b-%Y")
        ordinal = dateObj.toordinal()
        return ordinal

    def get_stock_data_from_internet(self, start_date, end_date):
        'Get stock data from Yahoo finance or Google'
        try:
            if self.stockURLSite == StockSite.google1: # THIS URL HAS ISSUES, SO IT IS NOT VERY USEFUL
                delta = endDate - start_date
                DAY = 24*60*60 # POSIX day in seconds (exact value)
                timestamp1 = calendar.timegm(start_date.timetuple())
                urlString = "https://www.google.com/finance/getprices?q={}&p={}d&ts={}&f=d,c&df=cpct&ei=Ef6XUYDfCqSTiAKEMg".format(
                    self.str_stock_symbol, delta.days, timestamp1)
                with urllib.request.urlopen(urlString) as response:
                    data = response.read()
                strResponse = data.decode("utf-8")
                lines = strResponse.split("\n")
                del lines[0:7] # zap header lines
                del lines[-1]  # zap last line
                list1 = [x.split(",") for x in lines] # split each line into a list
                list1[0][0] = list1[0][0][1:]         # get rid of leading 'a' character
                list2 = [[float(x[0]), float(x[1])] for x in list1] # create list w/ just date, closing price values for each date
                list3 = [[int(list2[0][0] + DAY*x[0]), x[1]] for x in list2] # convert date offset to timestamp
                list3[0][0] = int(list2[0][0])        # replace 1st timestamp entry (munged above) to correct original value
                self.quotes = [[dt.fromtimestamp(x[0]).toordinal(), x[1]] for x in list2] # convert timestamps to ordinals
                return [q[1] for q in self.quotes]
            elif self.stockURLSite == StockSite.google2: # THIS URL WORKS
                urlString = "http://www.google.com/finance/historical?q={}&startdate={:02d}-{:02d}-{:4d}&enddate={:02d}-{:02d}-{:4d}&output=csv".format(
                    self.str_stock_symbol, start_date.month, start_date.day, start_date.year, end_date.month, end_date.day, end_date.year)
                with urllib.request.urlopen(urlString) as response:
                    data = response.read()
                strResponse = data.decode("utf-8")
                lines = strResponse.split("\n")
                # The output (after the first header line) will be:  Date,Open,High,Low,Close,Volume,
                # starting from the 'startdate' and ending on the 'enddate', or as near as those 2 dates
                # can be hit (might not be market days).
                del lines[0]  # zap the header line
                del lines[-1] # zap empty line at end
                list1 = [x.split(",") for x in lines] # split each line into a list
                list1.reverse()
                self.quotes = [[self.convertStringDateToOrdinal(x[0]), float(x[4])] for x in list1] # grab and convert date; grab closing price
                return [q[1] for q in self.quotes]
        except Exception as e:
            messagebox.showerror("ERROR", "Could not get data from the Internet; bad stock symbol?\n\n" + str(e) + ".")
            return


    # Pre-Calculate functions
    def set_stock_symbol(self, stock_symbol):
        'Helper function to set the stock symbol'
        self.str_stock_symbol = stock_symbol

    def set_start_date(self, start_date):
        'Helper function to set the start date'
        self.start_date = start_date

    def set_end_date(self, end_date):
        'Helper function to set the end date'
        self.end_date = end_date

    def set_investment(self, investment):
        'Helper function to set the initial investment'
        self.str_investment = investment

    def set_opt_param1_mode(self, value):
        'Helper function to set the optional parameter #1'
        self.bLoop_on_param1 = value

    def set_opt_param2_mode(self, value):
        'Helper function to set the optional parameter #2'
        self.bLoop_on_param2 = value

    def set_opt_param3_mode(self, value):
        'Helper function to set the optional parameter #3'
        self.bLoop_on_param3 = value

    def set_opt_param4_mode(self, value):
        'Helper function to set the optional parameter #4'
        self.bLoop_on_param4 = value

    def loop_on_thres(self):
        'Helper function to set the loop flag'
        self.bLoop_on_param2 = True

    def set_opt_params(self, param1, param2, param3, param4):
        'Helper function to set all optional parameters'
        self.opt_param1 = float(param1)
        self.opt_param2 = float(param2)
        self.opt_param3 = float(param3)
        self.opt_param4 = float(param4)

    # Post-Calculate functions
    def get_ending_PV(self):
        'Helper function to get the ending portfolio value'
        return self.pv[len(self.pv)-1]

    def get_ending_SV(self):
        'Helper function to get the ending stock value'
        return self.sv[len(self.sv)-1]

    def get_ending_cash(self):
        'Helper function to get the ending cash amount'
        return self.cash[len(self.cash)-1]

    def get_num_trans(self):
        'Helper function to get the number of transactions'
        return self.num_trans

    def get_num_data_points(self):
        'Helper function to get the number of data points in the stock data'
        return self.num_data_points

    def get_starting_shares(self):
        'Helper function to get the number of shares originally bought'
        return self.shares_owned[0]

    def get_ending_shares(self):
        'Helper function to get the ending number of shares'
        return self.shares_owned[len(self.shares_owned)-1]

    def get_ROI(self):
        'Helper function to get the ROI'
        return self.annual_ROI

    def get_opt_param1(self):
        'Helper function to get the optional parameter #1'
        return self.opt_param1

    def get_opt_param2(self):
        'Helper function to get the optional parameter #2'
        return self.opt_param2

    def get_opt_param3(self):
        'Helper function to get the optional parameter #3'
        return self.opt_param3

    def get_opt_param4(self):
        'Helper function to get the optional parameter #4'
        return self.opt_param4

    def set_horz_size(self, horz_size):
        'Helper function to set the horizontal size of the window'
        self.horz_size = horz_size
        #print ("Model - horz_size is now {:.3f} inches (dpi = 80)".format(horz_size))


    # Inputs:
    # days_to_ave - number of days to average inside array
    # in_array - array of numbers to average
    # num_days - total size of the array
    def calc_average_array(self, days_to_ave, in_array, num_days):
        'Helper function for calc_averages (below).'
        midpt = int((days_to_ave - 1) / 2) # find midpoint of x value
        del in_array[:]      # clear out old data
        in_array = [sum(self.closes[i:i+days_to_ave]) / float(days_to_ave) for i in range(0, num_days)] # do the averaging
        temp = np.roll(in_array, midpt) # right rotate 'midpt' positions to align average curve to real curve
        for i in range(0, midpt):
            temp[i] = sum(self.closes[0:midpt+i+1]) / float(midpt+i+1)
        for i in range(num_days-midpt, num_days):
            temp[i] = sum(self.closes[i-midpt:num_days]) / float(num_days-(i-midpt))
        in_array = temp.tolist()
        return in_array


    def calc_averages(self):
        """ Calc moving averages for various lengths of time: 5 days, 10 days, etc.
        
        Data is in the self.closes[] array.
        Algorithm:  1) clear out old data in the array.
        2) Alloc space in each array for the averages.
        Space needed is length of quotes array minus (ave length - 1).
        For example, if quotes array is 15 long, we'll need: 15 - (5 - 1) = 11
        for the ave_5_days array.  This is because for the last 5 days, we do 1 average,
        then don't do an average for the 4 days, 3 days, 2 days, 1 day remaining
        as we loop. 3) Calc average using list comprehension."""
        num_days = len(self.closes)

        if num_days > 5:
            self.ave_5_days = self.calc_average_array(5, self.ave_5_days, num_days)
            #len_5days = len(self.ave_5_days)

        if num_days > 11:
            self.ave_11_days = self.calc_average_array(11, self.ave_11_days, num_days)
            #len_11days = len(self.ave_11_days)
            #print ("Ave 11 day length = " + str(len_11days) + ", closes length = " + str(num_days))

        if num_days > 21:
            self.ave_21_days = self.calc_average_array(21, self.ave_21_days, num_days)
            #len_21days = len(self.ave_21_days)
            #print ("Ave 21 day length = " + str(len_21days) + ", closes length = " + str(num_days))

        if num_days > 41:
            self.ave_41_days = self.calc_average_array(41, self.ave_41_days, num_days)
            #len_41days = len(self.ave_41_days)
            #print ("Ave 41 day length = " + str(len_41days) + ", closes length = " + str(num_days))

        if num_days > 81:
            self.ave_81_days = self.calc_average_array(81, self.ave_81_days, num_days)
            #len_81days = len(self.ave_81_days)
            #print ("Ave 81 day length = " + str(len_81days) + ", closes length = " + str(num_days))

        if num_days > 161:
            self.ave_161_days = self.calc_average_array(161, self.ave_161_days, num_days)
            #len_161days = len(self.ave_161_days)
            #print ("Ave 161 day length = " + str(len_161days) + ", closes length = " + str(num_days))

        if num_days > 251:
            self.ave_251_days = self.calc_average_array(251, self.ave_251_days, num_days)
            #len_251days = len(self.ave_251_days)
            #print ("Ave 251 day length = " + str(len_251days) + ", closes length = " + str(num_days))


# Direct injection of these functions into this class, so it can be in another file
# (since it could be large)
Model.calculate1 = algorithms.algo1.calculate1
Model.calculate2 = algorithms.algo2.calculate2
Model.calculate3 = algorithms.algo3.calculate3
Model.calculate4 = algorithms.algo4.calculate4
Model.core_calculate1 = algorithms.algo1.core_calculate1
Model.core_calculate2 = algorithms.algo2.core_calculate2
