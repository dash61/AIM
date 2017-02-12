#!/usr/bin/python
# -*- coding: utf-8

# MVC template from: https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/


from tkinter import ttk, HORIZONTAL, StringVar, IntVar  # use Tkinter for python 2, tkinter for python 3
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import date, timedelta


class View():
	def __init__(self, controller, master):
		# DEFAULT CONSTANTS
		APP_VERSION = 0.2
		self.SAFE_VALUE  = "5.2"  # cheap 'constants'
		self.THRESHOLD   = "80.0"
		
		self.root = master
		self.controller = controller
		self.frame = ttk.Frame(master) # use ttk, not tk, to get 'themed tk' frame
		self.strInvestment = StringVar()
		self.strStartDate = StringVar()
		self.strEndDate = StringVar()
		self.strPV = StringVar()
		self.strSV = StringVar()
		self.strCash = StringVar()
		self.strStockName = StringVar()
		self.strStartSharesOwned = StringVar()
		self.strFinalSharesOwned = StringVar()
		self.strNumTrans = StringVar()
		self.strNumDataPoints = StringVar()
		self.strAnnualROIVal = StringVar()
		self.strParam1 = StringVar()
		self.strParam2 = StringVar()
		self.strParam3 = StringVar()
		self.strParam4 = StringVar()
		self.strComment = StringVar()
		self.algo_choice = IntVar()
		self.plot_choice0 = IntVar()
		self.plot_choice5 = IntVar()
		self.plot_choice11 = IntVar()
		self.plot_choice21 = IntVar()
		self.plot_choice41 = IntVar()
		self.plot_choice81 = IntVar()
		self.plot_choice161 = IntVar()
		self.plot_choice251 = IntVar()
		self.plot_choiceAll = 0
		self.prev_plot_Choice = 0
		self.prev_algo = 0
		self.dates = []
		self.p5 = []  # this is a list of curves (lines) in par5

		
		self.strInvestment.set("4000")
		self.strPV.set("$ 0.00")
		self.strSV.set("$ 0.00")
		self.strCash.set("$ 0.00")
		self.strStartSharesOwned.set("0")
		self.strFinalSharesOwned.set("0")
		self.strNumTrans.set("0")
		self.strNumDataPoints.set("0")
		self.strStockName.set("ZIOP")
		self.strStartDate.set("01-01-2016") # random
		yesterday = date.today() - timedelta(days=1)
		self.strEndDate.set(yesterday.strftime("%m-%d-%Y")) # set end date to yesterday
		self.strAnnualROIVal.set("0.0")
		self.strParam1.set(self.SAFE_VALUE)
		self.strParam2.set(self.THRESHOLD)
		self.strParam3.set("0.0")
		self.strParam4.set("0.0")
		self.strComment.set("Param1 = SAFE and Param2 = Threshold.")
		self.algo_choice.set(1)
		self.plot_choice0.set(1)
		
		self.p1 = None    # plotting variables
		self.p2 = None
		self.p3 = None
		self.par1 = None
		self.par2 = None
		self.par5 = None  # used for the n-day average plots
		
		rowVal = 0
		ttk.Label(self.frame, text="Stock Symbol =").grid(column=0, row=rowVal, sticky="e")
		stockNameEntry = ttk.Entry(self.frame, width=10, textvariable=self.strStockName)
		stockNameEntry.grid(column=1, row=rowVal, sticky="ew")
		ttk.Button(self.frame, text="Help and Instructions...", command=self.controller.help).grid(row=rowVal, column=3, sticky="w")

		rowVal = rowVal + 1
		ttk.Label(self.frame, text="Start Date =").grid(column=0, row=rowVal, sticky="e")
		startDateEntry = ttk.Entry(self.frame, width=10, textvariable=self.strStartDate)
		startDateEntry.grid(column=1, row=rowVal, sticky="we")
		
		ttk.Label(self.frame, text="End Date =").grid(column=2, row=rowVal, sticky="e")
		endDateEntry = ttk.Entry(self.frame, width=10, textvariable=self.strEndDate)
		endDateEntry.grid(column=3, row=rowVal, sticky="we")
		
		rowVal = rowVal + 1
		ttk.Label(self.frame, text="Starting Investment =").grid(column=0, row=rowVal, sticky="e")
		self.invEntry = ttk.Entry(self.frame, width=10, textvariable=self.strInvestment)
		self.invEntry.grid(column=1, row=rowVal, sticky="we")
		ttk.Label(self.frame, text="Num Data Points =").grid(column=2, row=rowVal, sticky="e")
		ttk.Label(self.frame, textvariable=self.strNumDataPoints).grid(column=3, row=rowVal, sticky="we")
		
		rowVal = rowVal + 1
		ttk.Separator(self.frame, orient=HORIZONTAL).grid(row=rowVal, column=0, columnspan=4, sticky="we")
		
		rowVal = rowVal + 1
		ttk.Label(self.frame, text="Ending Portfolio Value =").grid(column=0, row=rowVal, sticky="e")
		ttk.Label(self.frame, textvariable=self.strPV).grid(column=1, row=rowVal, sticky="w")
		ttk.Label(self.frame, text="Ending Stock Value =").grid(column=2, row=rowVal, sticky="e")
		ttk.Label(self.frame, textvariable=self.strSV).grid(column=3, row=rowVal, sticky="w")
		
		rowVal = rowVal + 1
		ttk.Label(self.frame, text="Ending Cash =").grid(column=0, row=rowVal, sticky="e")
		ttk.Label(self.frame, textvariable=self.strCash).grid(column=1, row=rowVal, sticky="w")
		ttk.Label(self.frame, text="Num Transactions =").grid(column=2, row=rowVal, sticky="e")
		ttk.Label(self.frame, textvariable=self.strNumTrans).grid(column=3, row=rowVal, sticky="we")
		
		rowVal = rowVal + 1
		ttk.Label(self.frame, text="Starting Shares =").grid(column=0, row=rowVal, sticky="e")
		ttk.Label(self.frame, textvariable=self.strStartSharesOwned).grid(column=1, row=rowVal, sticky="w")
		ttk.Label(self.frame, text="Ending Shares =").grid(column=2, row=rowVal, sticky="e")
		ttk.Label(self.frame, textvariable=self.strFinalSharesOwned).grid(column=3, row=rowVal, sticky="w")
		
		rowVal = rowVal + 1
		ttk.Label(self.frame, text="Annual ROI =").grid(column=0, row=rowVal, sticky="e")
		ttk.Label(self.frame, textvariable=self.strAnnualROIVal).grid(column=1, row=rowVal, sticky="w")
		ttk.Button(self.frame, text="Run Selected Algorithm", command=self.controller.calculate).grid(row=rowVal, column=2, columnspan=2, sticky="we")
		
		rowVal = rowVal + 1
		ttk.Separator(self.frame, orient=HORIZONTAL).grid(row=rowVal, column=0, columnspan=4, sticky="we")
		
		rowVal = rowVal + 1
		ttk.Radiobutton(self.frame, text='Algo 1 - Original AIM', variable=self.algo_choice, value=1, command=self.clickAlgo1).grid(row=rowVal, column=0, columnspan=4, sticky="w")
		ttk.Radiobutton(self.frame, text='Algo 2 - Modified AIM', variable=self.algo_choice, value=2, command=self.clickAlgo2).grid(row=rowVal, column=1, columnspan=4, sticky="w")
		ttk.Radiobutton(self.frame, text='Algo 3', variable=self.algo_choice, value=3, command=self.clickAlgo3).grid(row=rowVal, column=2, columnspan=4, sticky="w")
		ttk.Radiobutton(self.frame, text='Algo 4', variable=self.algo_choice, value=4, command=self.clickAlgo4).grid(row=rowVal, column=3, columnspan=4, sticky="w")

		rowVal = rowVal + 1
		self.optBtn1 = ttk.Button(self.frame, text="Calc Optimum SAFE Value", command=self.controller.calcOptParam1)
		self.optBtn1.grid(column=0, row=rowVal, sticky="we")
		self.optBtn2 = ttk.Button(self.frame, text="Calc Optimum Threshold Value", command=self.controller.calcOptParam2)
		self.optBtn2.grid(column=1, row=rowVal, sticky="we")
		self.optBtn3 = ttk.Button(self.frame, text="      -- Not Used --      ", command=self.controller.calcOptParam3)
		self.optBtn3.grid(column=2, row=rowVal, sticky="we")
		self.optBtn4 = ttk.Button(self.frame, text="      -- Not Used --      ", command=self.controller.calcOptParam4)
		self.optBtn4.grid(column=3, row=rowVal, sticky="we")
		
		rowVal = rowVal + 1
		s = ttk.Style()
		s.configure('Grey.TEntry', background='grey')
		s.configure('Green.TEntry', background='green')
		self.param1Entry = ttk.Entry(self.frame, width=10, textvariable=self.strParam1)
		self.param1Entry.grid(column=0, row=rowVal, sticky="we")
		self.param2Entry = ttk.Entry(self.frame, width=10, textvariable=self.strParam2)
		self.param2Entry.grid(column=1, row=rowVal, sticky="we")
		self.param3Entry = ttk.Entry(self.frame, width=10, textvariable=self.strParam3)
		self.param3Entry.grid(column=2, row=rowVal, sticky="we")
		self.param4Entry = ttk.Entry(self.frame, width=10, textvariable=self.strParam4)
		self.param4Entry.grid(column=3, row=rowVal, sticky="we")
		self.param1Entry["style"] = "Green.TEntry"
		self.param2Entry["style"] = "Green.TEntry"
		self.param3Entry["style"] = "Grey.TEntry"
		self.param4Entry["style"] = "Grey.TEntry"

		rowVal = rowVal + 1
		self.cb0 = ttk.Checkbutton(self.frame, text='Plot - No Average', variable=self.plot_choice0, command=self.clickPlotNone).grid(row=rowVal, column=0, columnspan=4, sticky="w")
		self.cb1 = ttk.Checkbutton(self.frame, text='Plot - 5 day Average', variable=self.plot_choice5, command=self.clickPlot).grid(row=rowVal, column=1, columnspan=4, sticky="w")
		self.cb2 = ttk.Checkbutton(self.frame, text='Plot - 10 day Average', variable=self.plot_choice11, command=self.clickPlot).grid(row=rowVal, column=2, columnspan=4, sticky="w")
		self.cb3 = ttk.Checkbutton(self.frame, text='Plot - 20 day Average', variable=self.plot_choice21, command=self.clickPlot).grid(row=rowVal, column=3, columnspan=4, sticky="w")

		rowVal = rowVal + 1
		self.cb4 = ttk.Checkbutton(self.frame, text='Plot - 40 day Average', variable=self.plot_choice41, command=self.clickPlot).grid(row=rowVal, column=0, columnspan=4, sticky="w")
		self.cb5 = ttk.Checkbutton(self.frame, text='Plot - 80 day Average', variable=self.plot_choice81, command=self.clickPlot).grid(row=rowVal, column=1, columnspan=4, sticky="w")
		self.cb6 = ttk.Checkbutton(self.frame, text='Plot - 160 day Average', variable=self.plot_choice161, command=self.clickPlot).grid(row=rowVal, column=2, columnspan=4, sticky="w")
		self.cb7 = ttk.Checkbutton(self.frame, text='Plot - 250 day Average', variable=self.plot_choice251, command=self.clickPlot).grid(row=rowVal, column=3, columnspan=4, sticky="w")
		
		rowVal = rowVal + 1
		ttk.Label(self.frame, textvariable=self.strComment, text="Param1 = SAFE and Param2 = Threshold.").grid(column=0, row=rowVal, columnspan=4, sticky="we")
# 		rowVal = rowVal + 1
# 		ttk.Label(self.frame, text="Algorithms 3&4 have Param1 = 'blah blah' and Param2 = 'blah blah'.").grid(column=0, row=rowVal, columnspan=4, sticky="we")
		

		# We'll need these lines so the basic plot can draw before we call Calculate and fill in the plots themselves.
		rowVal = rowVal + 1
		self.fig, self.host = plt.subplots()
		params = plt.gcf()  # do this line and next 2 just so we can resize the plot taller
		mysize = params.get_size_inches()
		params.set_size_inches(mysize[0]*1, mysize[1]*1.2, forward=True)
		self.dataPlot = FigureCanvasTkAgg(self.fig, master=self.frame)
		self.dataPlot.get_tk_widget().grid(row=rowVal, column=0, columnspan=4, sticky="nsew")
		mpl.interactive(0) # turn off interaction of TkAgg
		
		# This next block is to get the app to resize everything correctly:
		self.root.columnconfigure(3, weight=1)  # need to do this for this column only to get resize to work right
		self.frame.columnconfigure(0, weight=1) # yes, this is different from the last line
		self.frame.columnconfigure(1, weight=1)
		self.frame.columnconfigure(2, weight=1)
		self.frame.columnconfigure(3, weight=1)
		self.frame.grid(column=0, row=rowVal, sticky="nsew")
		self.frame.grid(column=1, row=rowVal, sticky="nsew")
		self.frame.grid(column=2, row=rowVal, sticky="nsew")
		self.frame.grid(column=3, row=rowVal, sticky="nsew")
		
		for child in self.frame.winfo_children(): child.grid_configure(padx=3, pady=3)
		
		self.saved_windowWidth = self.root.winfo_width()
		self.root.update()
		self.root.minsize(300, 300) #self.root.winfo_height()) # trying to set a min width for app
		fig_size = plt.rcParams["figure.figsize"]
		print ("(view-init) plot size is {:.3f} x {:.3f} inches (wxh); dpi=80".format(fig_size[0], fig_size[1]))
		print ("(view-init) matplotlib version is {}".format(mpl.__version__))
		
	def __del__(self):
		print (id(self), 'died')
		
	# Set the text for the 4 buttons based on this 1st radio button being hit
	def clickAlgo1(self):
		self.optBtn1["text"] = "Calc Optimum SAFE Value"
		self.optBtn2["text"] = "Calc Optimum Threshold Value"
		self.optBtn3["text"] = "      -- Not Used --      "
		self.optBtn4["text"] = "      -- Not Used --      "
		self.strParam1.set(self.SAFE_VALUE)
		self.strParam2.set(self.THRESHOLD)
		self.param1Entry["style"] = "Green.TEntry"
		self.param2Entry["style"] = "Green.TEntry"
		self.param3Entry["style"] = "Grey.TEntry"
		self.param4Entry["style"] = "Grey.TEntry"
		self.strComment.set("Param1 = SAFE and Param2 = Threshold.")
		# If you switch algorithms, this will stop the plot from redrawing (may
		# not have the data yet to do so).
		if (self.controller.calc_btn_hit == 1 and self.algo_choice != self.prev_algo):
			self.controller.calc_btn_hit = 0
		self.prev_algo = 1

	# Set the text for the 4 buttons based on this 2nd radio button being hit
	def clickAlgo2(self):
		self.optBtn1["text"] = "Calc Optimum SAFE Value"
		self.optBtn2["text"] = "Calc Optimum Threshold Value"
		self.optBtn3["text"] = "      -- Not Used --      "
		self.optBtn4["text"] = "      -- Not Used --      "
		self.strParam1.set(self.SAFE_VALUE)
		self.strParam2.set(self.THRESHOLD)
		self.param1Entry["style"] = "Green.TEntry"
		self.param2Entry["style"] = "Green.TEntry"
		self.param3Entry["style"] = "Grey.TEntry"
		self.param4Entry["style"] = "Grey.TEntry"
		self.strComment.set("Param1 = SAFE and Param2 = Threshold.")
		# If you switch algorithms, this will stop the plot from redrawing (may
		# not have the data yet to do so).
		if (self.controller.calc_btn_hit == 1 and self.algo_choice != self.prev_algo):
			self.controller.calc_btn_hit = 0
		self.prev_algo = 2

	# Set the text for the 4 buttons based on this 3rd radio button being hit
	def clickAlgo3(self):
		self.optBtn1["text"] = "      -- Not Used --      "
		self.optBtn2["text"] = "      -- Not Used --      "
		self.optBtn3["text"] = "      -- Not Used --      "
		self.optBtn4["text"] = "      -- Not Used --      "
		self.strParam1.set(self.SAFE_VALUE)
		self.strParam2.set(self.THRESHOLD)
		self.param1Entry["style"] = "Grey.TEntry"
		self.param2Entry["style"] = "Grey.TEntry"
		self.param3Entry["style"] = "Grey.TEntry"
		self.param4Entry["style"] = "Grey.TEntry"
		self.strComment.set("Param1 = ? and Param2 = ?.")
		# If you switch algorithms, this will stop the plot from redrawing (may
		# not have the data yet to do so).
		if (self.controller.calc_btn_hit == 1 and self.algo_choice != self.prev_algo):
			self.controller.calc_btn_hit = 0
		self.prev_algo = 3

	# Set the text for the 4 buttons based on this 4th radio button being hit
	def clickAlgo4(self):
		self.optBtn1["text"] = "      -- Not Used --      "
		self.optBtn2["text"] = "      -- Not Used --      "
		self.optBtn3["text"] = "      -- Not Used --      "
		self.optBtn4["text"] = "      -- Not Used --      "
		self.strParam1.set(self.SAFE_VALUE)
		self.strParam2.set(self.THRESHOLD)
		self.param1Entry["style"] = "Grey.TEntry"
		self.param2Entry["style"] = "Grey.TEntry"
		self.param3Entry["style"] = "Grey.TEntry"
		self.param4Entry["style"] = "Grey.TEntry"
		self.strComment.set("Param1 = ? and Param2 = ?.")
		# If you switch algorithms, this will stop the plot from redrawing (may
		# not have the data yet to do so).
		if (self.controller.calc_btn_hit == 1 and self.algo_choice != self.prev_algo):
			self.controller.calc_btn_hit = 0
		self.prev_algo = 4

	# Call if the 'no plots' option is checked.
	def clickPlotNone(self):
		self.prev_plot_Choice = 0
		if (self.plot_choice0.get() == 1):  # then "none" plot is selected, so deselect all other checkboxes
			self.plot_choice5.set(0)
			self.plot_choice11.set(0)
			self.plot_choice21.set(0)
			self.plot_choice41.set(0)
			self.plot_choice81.set(0)
			self.plot_choice161.set(0)
			self.plot_choice251.set(0)
			self.plot_choiceAll = 0
			if (self.par5 != None):
				for item in self.p5:
					#print ("1 - Removing curve = " + str(id(item[0])))
					item[0].remove()
				del self.p5[:]
				self.dataPlot.draw()

		# if all other plots are deselected, select the "none" checkbox, even if the user just turned it off
		if (self.plot_choice5.get() == 0  and
				self.plot_choice11.get() == 0 and
				self.plot_choice21.get() == 0 and
				self.plot_choice41.get() == 0 and
				self.plot_choice81.get() == 0 and
				self.plot_choice161.get() == 0 and
				self.plot_choice251.get() == 0):
			self.plot_choice0.set(1)

	# Called when one of the plot checkboxes is clicked, also at the end of plotting
	# (to redraw the plots).
	def clickPlot(self):
		self.plot_choice0.set(0)  # clear None button
		self.plot_choiceAll = 0
		if (self.plot_choice5.get() == 1):
			self.plot_choiceAll = self.plot_choiceAll | 1
		elif ((self.prev_plot_Choice & 1) == 1):  # then this guy was deselected just now
			self.removeFromListByBitFlag (1)
		if (self.plot_choice11.get() == 1):
			self.plot_choiceAll = self.plot_choiceAll | 2
		elif ((self.prev_plot_Choice & 2) == 2):
			self.removeFromListByBitFlag (2)
		if (self.plot_choice21.get() == 1):
			self.plot_choiceAll = self.plot_choiceAll | 4
		elif ((self.prev_plot_Choice & 4) == 4):
			self.removeFromListByBitFlag (4)
		if (self.plot_choice41.get() == 1):
			self.plot_choiceAll = self.plot_choiceAll | 8
		elif ((self.prev_plot_Choice & 8) == 8):
			self.removeFromListByBitFlag (8)
		if (self.plot_choice81.get() == 1):
			self.plot_choiceAll = self.plot_choiceAll | 16
		elif ((self.prev_plot_Choice & 16) == 16):
			self.removeFromListByBitFlag (16)
		if (self.plot_choice161.get() == 1):
			self.plot_choiceAll = self.plot_choiceAll | 32
		elif ((self.prev_plot_Choice & 32) == 32):
			self.removeFromListByBitFlag (32)
		if (self.plot_choice251.get() == 1):
			self.plot_choiceAll = self.plot_choiceAll | 64
		elif ((self.prev_plot_Choice & 64) == 64):
			self.removeFromListByBitFlag (64)
		
		# if all other plots are deselected, select the "none" checkbox
		if (self.plot_choiceAll == 0):
			self.plot_choice0.set(1)
			
		elif (self.prev_plot_Choice <= self.plot_choiceAll):
			if (self.par5 == None):
				self.par5 = self.host.twinx()
			elif (self.par5 != None): # temp change to fix zorder issues
				self.par5.remove()
				self.par5 = self.host.twinx()
	
			if (self.plot_choiceAll > 0):
				lenCloses = len(self.controller.model.closes)
				just_ints = np.arange(lenCloses)
				
				# For color names, see:
				# http://stackoverflow.com/questions/22408237/named-colors-in-matplotlib
				
				optParam3 = self.controller.model.getOptParam3()
				thisChoice = self.plot_choiceAll
				if ((thisChoice & 0x1) != 0 and lenCloses > 5):
					temp, = self.par5.plot(just_ints, self.controller.model.ave5days, "r-", zorder=11)
					self.p5.insert(0, (temp, 0x1))
				if ((thisChoice & 0x2) != 0 and lenCloses > 11):
					temp, = self.par5.plot(just_ints, self.controller.model.ave11days, "r-", zorder=11)
					self.p5.insert(0, (temp, 0x2))
				if ((thisChoice & 0x4) != 0 and lenCloses > 21):
					temp, = self.par5.plot(just_ints, self.controller.model.ave21days, "r-")
					self.p5.insert(0, (temp, 0x4))
				if ((thisChoice & 0x8) != 0 and lenCloses > 41):
					temp, = self.par5.plot(just_ints, self.controller.model.ave41days, "r-")
					self.p5.insert(0, (temp, 0x8))
				if ((thisChoice & 0x10) != 0 and lenCloses > 81):
					temp, = self.par5.plot(just_ints, self.controller.model.ave81days, "r-")
					self.p5.insert(0, (temp, 0x10))
				if ((thisChoice & 0x20) != 0 and lenCloses > 161):
					temp, = self.par5.plot(just_ints, self.controller.model.ave161days, "r-")
					self.p5.insert(0, (temp, 0x20))
				if ((thisChoice & 0x40) != 0 and lenCloses > 251):
					temp, = self.par5.plot(just_ints, self.controller.model.ave251days, "r-")
					self.p5.insert(0, (temp, 0x40))
				self.make_patch_spines_invisible(self.par5)
				self.par5.spines["right"].set_visible(False)
				self.par5.get_yaxis().set_visible(False)
				self.par5.set_ylim(self.host.get_ylim())
				self.host.set_xlim(0, lenCloses-1)

		self.dataPlot.draw()				
		self.prev_plot_Choice = self.plot_choiceAll


	def removeFromListByBitFlag(self, bitflag):
		for item in self.p5:
			if (bitflag == item[1]):
				#print ("2 - Removing curve = " + str(id(item[0])))
				item[0].remove()
				self.p5.remove(item)
				
	# code from site that had plot examples
	def make_patch_spines_invisible(self, ax):
		ax.set_frame_on(True)
		ax.patch.set_visible(False)
		for sp in ax.spines.values():
			sp.set_visible(False)
	
	def resize_func(self, event):
		#w, h, t = event.width, event.height, event.type
		w_real = self.root.winfo_width()
		if (self.controller.calc_btn_hit == 1 and self.saved_windowWidth != w_real):
			self.saved_windowWidth = w_real
			#safeEntry.width = w_real / 4.0
			#mainframe.itemconfigure("safeEntry", width=(w_real / 4.0))
			dpi = 120.0  # TODO - get real value
			self.plotIt()

	# inputs - tick value = x and position = pos
	def format_date(self, x, pos=None):
			thisind = np.clip(int(x + 0.5), 0, len(self.controller.model.closes) - 1)
			the_date = date.fromordinal(int(self.dates[thisind]))
			return the_date.strftime('%b-%e-%Y') # m d Y in gui date boxes
			
	def plotIt(self):
# 		print ("About to clear plots, thread={}, threadID={}, MPL ver={}".format(
# 			current_thread().name, current_thread().ident, mpl.__version__))
		self.clearPlots()

		optParam3 = self.controller.model.getOptParam3()
		optParam4 = self.controller.model.getOptParam4()
		lenCloses = len(self.controller.model.closes)
		algo = self.algo_choice.get()

		self.dates = [q[0] for q in self.controller.model.quotes]
		self.host.grid(True)  # this works, turns on minor grids
		self.saved_windowWidth = self.root.winfo_width()
		just_ints = np.arange(lenCloses)

		# Using twinx - Having been created by twinx, par1 or par2 will have its frame off,
		# so the line of its detached spine is invisible.  You will have to fix that later.
		# The ticks and label will be placed on the right in this twinx call.
		self.par1 = self.host.twinx()
		self.par2 = self.host.twinx()
		
		self.p1, = self.host.plot(just_ints, self.controller.model.closes, "b-")
		host_ylim = self.host.get_ylim() # need this value for certain plots		
		self.host.set_xlabel("Time")
		self.host.set_ylabel("Stock Price ($)")
		tkw = dict(size=4, width=1.5)
		
		order2 = [x * -1 for x in self.controller.model.order] # flip sign of each array element using list comprehension
		self.p2, = self.par1.plot(just_ints, self.controller.model.pv, "r--")
		self.p3, = self.par2.plot(just_ints, order2, "go")
		self.par2.set_ylabel("Orders ($)")          # you'll have to customize this for other algorithms
		self.par1.set_ylabel("Portfolio Value ($)") # ditto
		self.par2.spines["right"].set_position(("axes", 1.16)) # offset the right spine of par2
		self.make_patch_spines_invisible(self.par2) # activate the frame but make the patch and spines invisible
		self.par2.spines["right"].set_visible(True) # show the right spine
			
		self.host.yaxis.label.set_color(self.p1.get_color())
		self.par1.yaxis.label.set_color(self.p2.get_color())
		self.par2.yaxis.label.set_color(self.p3.get_color())
		
		self.host.tick_params(axis='y', colors=self.p1.get_color(), **tkw)
		self.par1.tick_params(axis='y', colors=self.p2.get_color(), **tkw)
		self.par2.tick_params(axis='y', colors=self.p3.get_color(), **tkw)
		self.host.tick_params(axis='x', **tkw)
		
		#xtick_locator = mpl.dates.AutoDateLocator()
		#xtick_formatter = mpl.dates.AutoDateFormatter(xtick_locator)
		#self.host.xaxis.set_major_locator(xtick_locator)
		#self.host.xaxis.set_major_formatter(xtick_formatter)
		self.host.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(self.format_date))
		self.host.set_xlim(0, lenCloses-1)
		self.host.autoscale_view()

		# rotates and right aligns the x labels, and moves the bottom of the
		# axes up to make room for them
		self.fig.autofmt_xdate(rotation=60)#, bottom=0.2) # change bottom so "Time" label is visible
		
		# draw the legend
		#lines = [self.p1, self.p2, self.p3]
		#self.host.legend(lines, [l.get_label() for l in lines])
			
		self.prev_plot_Choice = 0
		self.fig.tight_layout()
		self.clickPlot()
		
		window_size = self.fig.get_size_inches()   # gives window size (grey area, not the plot area)
		#fig_size = plt.rcParams["figure.figsize"] # always gives 8x6 even if window is resized
		#print ("(view-plot) plot size is {:.3f} x {:.3f} inches (wxh); dpi=80".format(window_size[0], window_size[1]))
		self.controller.model.setHorzSize(window_size[0])


	def clearPlots(self):
		#print ("CLEARING PLOTS.....................")
		if (self.p1 != None):
			try:
				self.p1.remove()  # these calls work good to remove the old plot and axes
			except BaseException as e:
				print ("EXCEPTION OCCURRED IN view.PY, trying to remove p1, IN clearPlots FUNCTION - " + str(e))
				pass
			try:
				self.p2.remove()
			except BaseException as e:
				print ("EXCEPTION OCCURRED IN view.PY, trying to remove p2, IN clearPlots FUNCTION - " + str(e))
				pass
			try:
				self.p3.remove()
			except BaseException as e:
				print ("EXCEPTION OCCURRED IN view.PY, trying to remove p3, IN clearPlots FUNCTION - " + str(e))
				pass
			if (self.p5 != None):
				counter = 1
				while counter <= 64:
					if ((self.prev_plot_Choice & counter) == counter):
						self.removeFromListByBitFlag (counter)
					counter *= 2
			self.host.cla()   # this is very important so the axes get reset each time
			try:
				self.par1.cla()
				self.par1.clear()
				self.par1.remove()
			except BaseException as e:
				print ("EXCEPTION OCCURRED IN view.PY, trying to remove par1, IN clearPlots FUNCTION - " + str(e))
				pass
			try:
				if (self.par2 != None):
					self.par2.cla()
					self.par2.clear()
					self.par2.remove()
			except BaseException as e:
				print ("EXCEPTION OCCURRED IN view.PY, trying to remove par2, IN clearPlots FUNCTION - " + str(e))
				pass
			try:
				if (self.par5 != None):
					self.par5.remove()
					self.par5 = self.host.twinx()
					self.par5.spines["right"].set_visible(False)
					self.par5.get_yaxis().set_visible(False)
					self.par5.set_ylim(self.host.get_ylim())
			except BaseException as e:
				print ("EXCEPTION OCCURRED IN view.PY, trying to remove par5, IN clearPlots FUNCTION - " + str(e))
				pass
		plt.close("all") # see if this works

	#	 plt.clf()  # these 3 calls clear the entire graph, but the host graph and axes never come back
	#	 plt.cla()
	#	 plt.close()
		#plt.close() # don't do this or the app will close (mainloop will exit); not sure why
