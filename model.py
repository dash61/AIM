#!/usr/bin/python
# -*- coding: utf-8

# MVC template from: https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/


import math
import datetime
import re
from tkinter import messagebox  # use Tkinter for python 2, tkinter for python 3
from matplotlib.finance import quotes_historical_yahoo_ochl
import numpy as np
import algorithms.algo1
import algorithms.algo2
import algorithms.algo3
import algorithms.algo4


class Model():
	def __init__(self):
		self.strStockSymbol = "ZIOP"
		self.startDate = datetime.date(2016,1,1)     #"02-23-2016"
		self.endDate = datetime.date(2016,12,31)     #"05-17-2016"
		self.strInvestment = "4000"
		self.pcntl = []
		self.cash = []
		self.pv = []
		self.sv = []
		self.sharesOwned = []
		self.order = []
		self.numTrans = 0
		self.numDataPoints = 0
		self.quotes = []
		self.closes = []
		self.ave5days = []
		self.ave11days = []
		self.ave21days = []
		self.ave41days = []
		self.ave81days = []
		self.ave161days = []
		self.ave251days = []
		self.annualROI = 0.0
		self.bLoopOnParam1 = False
		self.bLoopOnParam2 = False
		self.bLoopOnParam3 = False
		self.bLoopOnParam4 = False

		self.optParam1 = 0.052
		self.optParam2 = 0.80
		self.optParam3 = 0.0
		self.optParam4 = 0.0
		self.horzSize = 9.0  # in inches; dpi = 80
		
	def __del__(self):
		print (id(self), 'died')
		

	def calcROI(self, startDate, endDate):
		delta = endDate - startDate   # get delta between start and stop dates
		years = delta.days / 365.25   # calc number of years that passed over time range
		x = self.pv[len(self.pv)-1] / self.pv[0]  # ratio of ending pv to starting pv
		y = 1.0 / years			      # get inverse of years
		z = (math.pow(x, y)) - 1	  # x to the y power, then minus 1
		z = z * 100.0				  # convert to percent
		z = round(z, 2)			      # round off
		return z
			
	def getStockDataFromInternet(self, startDate, endDate):
		try:
			return quotes_historical_yahoo_ochl(self.strStockSymbol, startDate, endDate) # get stock data!
		except:
			messagebox.showerror("ERROR", "Could not get data from the Internet; bad stock symbol?")
			return
			
		
	# Pre-Calculate functions
	def setStockSymbol(self, stockSymbol):
		self.strStockSymbol = stockSymbol
		
	def setStartDate(self, startDate):
		self.startDate = startDate
		
	def setEndDate(self, endDate):
		self.endDate = endDate
		
	def setInvestment(self, investment):
		self.strInvestment = investment

	def setOptParam1Mode(self, value):
		self.bLoopOnParam1 = value
		
	def setOptParam2Mode(self, value):
		self.bLoopOnParam2 = value
		
	def setOptParam3Mode(self, value):
		self.bLoopOnParam3 = value
		
	def setOptParam4Mode(self, value):
		self.bLoopOnParam4 = value
		
	def loopOnThres(self):
		self.bLoopOnParam2 = True
		
	def setOptParams(self, param1, param2, param3, param4):
		self.optParam1 = float(param1)
		self.optParam2 = float(param2)
		self.optParam3 = float(param3)
		self.optParam4 = float(param4)
		
	# Post-Calculate functions
	def getEndingPV(self):
		return self.pv[len(self.pv)-1]
	
	def getEndingSV(self):
		return self.sv[len(self.sv)-1]

	def getEndingCash(self):
		return self.cash[len(self.cash)-1]

	def getNumTrans(self):
		return self.numTrans
	
	def getNumDataPoints(self):
		return self.numDataPoints
	
	def getStartingShares(self):
		return self.sharesOwned[0]
	
	def getEndingShares(self):
		return self.sharesOwned[len(self.sharesOwned)-1]

	def getROI(self):
		return self.annualROI
	
	def getOptParam1(self):
		return self.optParam1
	
	def getOptParam2(self):
		return self.optParam2
	
	def getOptParam3(self):
		return self.optParam3
	
	def getOptParam4(self):
		return self.optParam4
	
	def setHorzSize(self, horzSize):
		self.horzSize = horzSize
		#print ("Model - horzSize is now {:.3f} inches (dpi = 80)".format(horzSize))
	

	# Inputs:
	# x - number of days to average inside array
	# in_array - array of numbers to average
	# numDays - total size of the array
	def calcAverageArray(self, x, in_array, numDays):
		y = int((x - 1) / 2) # find midpoint of x value
		del in_array[:]      # clear out old data
		in_array = [sum(self.closes[i:i+x]) / float(x) for i in range(0, numDays)] # do the averaging
		temp = np.roll(in_array, y) # right rotate 'y' positions to align average curve to real curve
		for i in range(0,y):
			temp[i] = sum(self.closes[0:y+i+1]) / float(y+i+1)
		for i in range(numDays-y,numDays):
			temp[i] = sum(self.closes[i-y:numDays]) / float(numDays-(i-y))
		in_array = temp.tolist()
		return in_array


	# Calc moving averages for various lengths of time: 5 days, 10 days, etc.
	# Data is in the self.closes[] array.
	# Algorithm:  1) clear out old data in the array.
	# 2) Alloc space in each array for the averages.
	# Space needed is length of quotes array minus (ave length - 1).
	# For example, if quotes array is 15 long, we'll need: 15 - (5 - 1) = 11
	# for the ave5days array.  This is because for the last 5 days, we do 1 average,
	# then don't do an average for the 4 days, 3 days, 2 days, 1 day remaining 
	# as we loop. 3) Calc average using list comprehension.
	
	def calcAverages(self):
		numDays = len(self.closes)
	
		if numDays > 5:
			self.ave5days = self.calcAverageArray(5, self.ave5days, numDays)
			len_5days = len(self.ave5days)
	
		if numDays > 11:
			self.ave11days = self.calcAverageArray(11, self.ave11days, numDays)
			len_11days = len(self.ave11days)
			#print ("Ave 11 day length = " + str(len_11days) + ", closes length = " + str(numDays))
	
		if numDays > 21:
			self.ave21days = self.calcAverageArray(21, self.ave21days, numDays)
			len_21days = len(self.ave21days)
			#print ("Ave 21 day length = " + str(len_21days) + ", closes length = " + str(numDays))
		
		if numDays > 41:
			self.ave41days = self.calcAverageArray(41, self.ave41days, numDays)
			len_41days = len(self.ave41days)
			#print ("Ave 41 day length = " + str(len_41days) + ", closes length = " + str(numDays))
		
		if numDays > 81:
			self.ave81days = self.calcAverageArray(81, self.ave81days, numDays)
			len_81days = len(self.ave81days)
			#print ("Ave 81 day length = " + str(len_81days) + ", closes length = " + str(numDays))
	
		if numDays > 161:
			self.ave161days = self.calcAverageArray(161, self.ave161days, numDays)
			len_161days = len(self.ave161days)
			#print ("Ave 161 day length = " + str(len_161days) + ", closes length = " + str(numDays))
	
		if numDays > 251:
			self.ave251days = self.calcAverageArray(251, self.ave251days, numDays)
			len_251days = len(self.ave251days)
			#print ("Ave 251 day length = " + str(len_251days) + ", closes length = " + str(numDays))
	

# Direct injection of these functions into this class, so it can be in another file
# (since it could be large)
Model.calculate1 = algorithms.algo1.calculate1
Model.calculate2 = algorithms.algo2.calculate2
Model.calculate3 = algorithms.algo3.calculate3
Model.calculate4 = algorithms.algo4.calculate4
Model.coreCalculate1 = algorithms.algo1.coreCalculate1
Model.coreCalculate2 = algorithms.algo2.coreCalculate2



