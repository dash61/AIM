"""
View class for application.

MVC template from:
  https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/
"""


from datetime import date, timedelta
from tkinter import ttk, HORIZONTAL, StringVar, IntVar  # use Tkinter for python 2, tkinter for python 3
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np



class View():
    'View class of the MVC architecture.'
    def __init__(self, controller, master):
        'Constructor'
        # DEFAULT CONSTANTS
        #APP_VERSION = 0.2
        self.SAFE_VALUE = "5.2"  # cheap 'constants'
        self.THRESHOLD = "80.0"

        self.root = master
        self.controller = controller
        self.frame = ttk.Frame(master) # use ttk, not tk, to get 'themed tk' frame
        self.str_investment = StringVar()
        self.str_start_date = StringVar()
        self.str_end_date = StringVar()
        self.str_PV = StringVar()
        self.str_SV = StringVar()
        self.str_cash = StringVar()
        self.str_stock_name = StringVar()
        self.str_start_shares_owned = StringVar()
        self.str_final_shares_owned = StringVar()
        self.str_num_trans = StringVar()
        self.str_num_data_points = StringVar()
        self.str_annual_ROI_val = StringVar()
        self.str_param1 = StringVar()
        self.str_param2 = StringVar()
        self.str_param3 = StringVar()
        self.str_param4 = StringVar()
        self.str_comment = StringVar()
        self.algo_choice = IntVar()
        self.plot_choice0 = IntVar()
        self.plot_choice5 = IntVar()
        self.plot_choice11 = IntVar()
        self.plot_choice21 = IntVar()
        self.plot_choice41 = IntVar()
        self.plot_choice81 = IntVar()
        self.plot_choice161 = IntVar()
        self.plot_choice251 = IntVar()
        self.plot_choice_all = 0
        self.prev_plot_choice = 0
        self.prev_algo = 0
        self.dates = []
        self.p5 = []  # this is a list of curves (lines) in par5


        self.str_investment.set("4000")
        self.str_PV.set("$ 0.00")
        self.str_SV.set("$ 0.00")
        self.str_cash.set("$ 0.00")
        self.str_start_shares_owned.set("0")
        self.str_final_shares_owned.set("0")
        self.str_num_trans.set("0")
        self.str_num_data_points.set("0")
        self.str_stock_name.set("ZIOP")
        self.str_start_date.set("01-01-2016") # random
        yesterday = date.today() - timedelta(days=1)
        self.str_end_date.set(yesterday.strftime("%m-%d-%Y")) # set end date to yesterday
        self.str_annual_ROI_val.set("0.0")
        self.str_param1.set(self.SAFE_VALUE)
        self.str_param2.set(self.THRESHOLD)
        self.str_param3.set("0.0")
        self.str_param4.set("0.0")
        self.str_comment.set("Param1 = SAFE and Param2 = Threshold.")
        self.algo_choice.set(1)
        self.plot_choice0.set(1)

        self.p1 = None    # plotting variables
        self.p2 = None
        self.p3 = None
        self.par1 = None
        self.par2 = None
        self.par5 = None  # used for the n-day average plots

        row_val = 0
        ttk.Label(self.frame, text="Stock Symbol =").grid(column=0, row=row_val, sticky="e")
        stock_name_entry = ttk.Entry(self.frame, width=10, textvariable=self.str_stock_name)
        stock_name_entry.grid(column=1, row=row_val, sticky="ew")
        ttk.Button(self.frame, text="Help and Instructions...", command=self.controller.help).grid(row=row_val, column=3, sticky="w")

        row_val = row_val + 1
        ttk.Label(self.frame, text="Start Date =").grid(column=0, row=row_val, sticky="e")
        start_date_entry = ttk.Entry(self.frame, width=10, textvariable=self.str_start_date)
        start_date_entry.grid(column=1, row=row_val, sticky="we")

        ttk.Label(self.frame, text="End Date =").grid(column=2, row=row_val, sticky="e")
        end_date_entry = ttk.Entry(self.frame, width=10, textvariable=self.str_end_date)
        end_date_entry.grid(column=3, row=row_val, sticky="we")

        row_val = row_val + 1
        ttk.Label(self.frame, text="Starting Investment =").grid(column=0, row=row_val, sticky="e")
        self.inv_entry = ttk.Entry(self.frame, width=10, textvariable=self.str_investment)
        self.inv_entry.grid(column=1, row=row_val, sticky="we")
        ttk.Label(self.frame, text="Num Data Points =").grid(column=2, row=row_val, sticky="e")
        ttk.Label(self.frame, textvariable=self.str_num_data_points).grid(column=3, row=row_val, sticky="we")

        row_val = row_val + 1
        ttk.Separator(self.frame, orient=HORIZONTAL).grid(row=row_val, column=0, columnspan=4, sticky="we")

        row_val = row_val + 1
        ttk.Label(self.frame, text="Ending Portfolio Value =").grid(column=0, row=row_val, sticky="e")
        ttk.Label(self.frame, textvariable=self.str_PV).grid(column=1, row=row_val, sticky="w")
        ttk.Label(self.frame, text="Ending Stock Value =").grid(column=2, row=row_val, sticky="e")
        ttk.Label(self.frame, textvariable=self.str_SV).grid(column=3, row=row_val, sticky="w")

        row_val = row_val + 1
        ttk.Label(self.frame, text="Ending Cash =").grid(column=0, row=row_val, sticky="e")
        ttk.Label(self.frame, textvariable=self.str_cash).grid(column=1, row=row_val, sticky="w")
        ttk.Label(self.frame, text="Num Transactions =").grid(column=2, row=row_val, sticky="e")
        ttk.Label(self.frame, textvariable=self.str_num_trans).grid(column=3, row=row_val, sticky="we")

        row_val = row_val + 1
        ttk.Label(self.frame, text="Starting Shares =").grid(column=0, row=row_val, sticky="e")
        ttk.Label(self.frame, textvariable=self.str_start_shares_owned).grid(column=1, row=row_val, sticky="w")
        ttk.Label(self.frame, text="Ending Shares =").grid(column=2, row=row_val, sticky="e")
        ttk.Label(self.frame, textvariable=self.str_final_shares_owned).grid(column=3, row=row_val, sticky="w")

        row_val = row_val + 1
        ttk.Label(self.frame, text="Annual ROI =").grid(column=0, row=row_val, sticky="e")
        ttk.Label(self.frame, textvariable=self.str_annual_ROI_val).grid(column=1, row=row_val, sticky="w")
        ttk.Button(self.frame, text="Run Selected Algorithm", command=self.controller.calculate).grid(row=row_val, column=2, columnspan=2, sticky="we")

        row_val = row_val + 1
        ttk.Separator(self.frame, orient=HORIZONTAL).grid(row=row_val, column=0, columnspan=4, sticky="we")

        row_val = row_val + 1
        ttk.Radiobutton(self.frame, text='Algo 1 - Original AIM', variable=self.algo_choice, value=1, command=self.click_algo1).grid(row=row_val, column=0, columnspan=4, sticky="w")
        ttk.Radiobutton(self.frame, text='Algo 2 - Modified AIM', variable=self.algo_choice, value=2, command=self.click_algo2).grid(row=row_val, column=1, columnspan=4, sticky="w")
        ttk.Radiobutton(self.frame, text='Algo 3', variable=self.algo_choice, value=3, command=self.click_algo3).grid(row=row_val, column=2, columnspan=4, sticky="w")
        ttk.Radiobutton(self.frame, text='Algo 4', variable=self.algo_choice, value=4, command=self.click_algo4).grid(row=row_val, column=3, columnspan=4, sticky="w")

        row_val = row_val + 1
        self.opt_btn1 = ttk.Button(self.frame, text="Calc Optimum SAFE Value", command=self.controller.calc_opt_param1)
        self.opt_btn1.grid(column=0, row=row_val, sticky="we")
        self.opt_btn2 = ttk.Button(self.frame, text="Calc Optimum Threshold Value", command=self.controller.calc_opt_param2)
        self.opt_btn2.grid(column=1, row=row_val, sticky="we")
        self.opt_btn3 = ttk.Button(self.frame, text="      -- Not Used --      ", command=self.controller.calc_opt_param3)
        self.opt_btn3.grid(column=2, row=row_val, sticky="we")
        self.opt_btn4 = ttk.Button(self.frame, text="      -- Not Used --      ", command=self.controller.calc_opt_param4)
        self.opt_btn4.grid(column=3, row=row_val, sticky="we")

        row_val = row_val + 1
        style = ttk.Style()
        style.configure('Grey.TEntry', background='grey')
        style.configure('Green.TEntry', background='green')
        self._param1_entry = ttk.Entry(self.frame, width=10, textvariable=self.str_param1)
        self._param1_entry.grid(column=0, row=row_val, sticky="we")
        self._param2_entry = ttk.Entry(self.frame, width=10, textvariable=self.str_param2)
        self._param2_entry.grid(column=1, row=row_val, sticky="we")
        self._param3_entry = ttk.Entry(self.frame, width=10, textvariable=self.str_param3)
        self._param3_entry.grid(column=2, row=row_val, sticky="we")
        self._param4_entry = ttk.Entry(self.frame, width=10, textvariable=self.str_param4)
        self._param4_entry.grid(column=3, row=row_val, sticky="we")
        self._param1_entry["style"] = "Green.TEntry"
        self._param2_entry["style"] = "Green.TEntry"
        self._param3_entry["style"] = "Grey.TEntry"
        self._param4_entry["style"] = "Grey.TEntry"

        row_val = row_val + 1
        self.cb0 = ttk.Checkbutton(self.frame, text='Plot - No Average', variable=self.plot_choice0, command=self.click_plot_none).grid(row=row_val, column=0, columnspan=4, sticky="w")
        self.cb1 = ttk.Checkbutton(self.frame, text='Plot - 5 day Average', variable=self.plot_choice5, command=self.click_plot).grid(row=row_val, column=1, columnspan=4, sticky="w")
        self.cb2 = ttk.Checkbutton(self.frame, text='Plot - 10 day Average', variable=self.plot_choice11, command=self.click_plot).grid(row=row_val, column=2, columnspan=4, sticky="w")
        self.cb3 = ttk.Checkbutton(self.frame, text='Plot - 20 day Average', variable=self.plot_choice21, command=self.click_plot).grid(row=row_val, column=3, columnspan=4, sticky="w")

        row_val = row_val + 1
        self.cb4 = ttk.Checkbutton(self.frame, text='Plot - 40 day Average', variable=self.plot_choice41, command=self.click_plot).grid(row=row_val, column=0, columnspan=4, sticky="w")
        self.cb5 = ttk.Checkbutton(self.frame, text='Plot - 80 day Average', variable=self.plot_choice81, command=self.click_plot).grid(row=row_val, column=1, columnspan=4, sticky="w")
        self.cb6 = ttk.Checkbutton(self.frame, text='Plot - 160 day Average', variable=self.plot_choice161, command=self.click_plot).grid(row=row_val, column=2, columnspan=4, sticky="w")
        self.cb7 = ttk.Checkbutton(self.frame, text='Plot - 250 day Average', variable=self.plot_choice251, command=self.click_plot).grid(row=row_val, column=3, columnspan=4, sticky="w")

        row_val = row_val + 1
        ttk.Label(self.frame, textvariable=self.str_comment, text="Param1 = SAFE and Param2 = Threshold.").grid(column=0, row=row_val, columnspan=4, sticky="we")
#         row_val = row_val + 1
#         ttk.Label(self.frame, text="Algorithms 3&4 have Param1 = 'blah blah' and Param2 = 'blah blah'.").grid(column=0, row=row_val, columnspan=4, sticky="we")


        # We'll need these lines so the basic plot can draw before we call Calculate and fill in the plots themselves.
        row_val = row_val + 1
        self.fig, self.host = plt.subplots()
        params = plt.gcf()  # do this line and next 2 just so we can resize the plot taller
        mysize = params.get_size_inches()
        params.set_size_inches(mysize[0]*1, mysize[1]*1.2, forward=True)
        self.data_plot = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.data_plot.get_tk_widget().grid(row=row_val, column=0, columnspan=4, sticky="nsew")
        mpl.interactive(0) # turn off interaction of TkAgg

        # This next block is to get the app to resize everything correctly:
        self.root.columnconfigure(3, weight=1)  # need to do this for this column only to get resize to work right
        self.frame.columnconfigure(0, weight=1) # yes, this is different from the last line
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.grid(column=0, row=row_val, sticky="nsew")
        self.frame.grid(column=1, row=row_val, sticky="nsew")
        self.frame.grid(column=2, row=row_val, sticky="nsew")
        self.frame.grid(column=3, row=row_val, sticky="nsew")

        for child in self.frame.winfo_children():
            child.grid_configure(padx=3, pady=3)

        self.saved_window_width = self.root.winfo_width()
        self.root.update()
        self.root.minsize(300, 300) #self.root.winfo_height()) # trying to set a min width for app
        fig_size = plt.rcParams["figure.figsize"]
        print("(view-init) plot size is {:.3f} x {:.3f} inches (wxh); dpi=80".format(fig_size[0], fig_size[1]))
        print("(view-init) matplotlib version is {}".format(mpl.__version__))

    def __del__(self):
        'Destructor, just to see if/when it gets called'
        print(id(self), 'died')

    def click_algo1(self):
        'Set the text for the 4 buttons based on this 1st radio button being hit'
        self.opt_btn1["text"] = "Calc Optimum SAFE Value"
        self.opt_btn2["text"] = "Calc Optimum Threshold Value"
        self.opt_btn3["text"] = "      -- Not Used --      "
        self.opt_btn4["text"] = "      -- Not Used --      "
        self.str_param1.set(self.SAFE_VALUE)
        self.str_param2.set(self.THRESHOLD)
        self._param1_entry["style"] = "Green.TEntry"
        self._param2_entry["style"] = "Green.TEntry"
        self._param3_entry["style"] = "Grey.TEntry"
        self._param4_entry["style"] = "Grey.TEntry"
        self.str_comment.set("Param1 = SAFE and Param2 = Threshold.")
        # If you switch algorithms, this will stop the plot from redrawing (may
        # not have the data yet to do so).
        if self.controller.calc_btn_hit == 1 and self.algo_choice != self.prev_algo:
            self.controller.calc_btn_hit = 0
        self.prev_algo = 1

    def click_algo2(self):
        'Set the text for the 4 buttons based on this 2nd radio button being hit'
        self.opt_btn1["text"] = "Calc Optimum SAFE Value"
        self.opt_btn2["text"] = "Calc Optimum Threshold Value"
        self.opt_btn3["text"] = "      -- Not Used --      "
        self.opt_btn4["text"] = "      -- Not Used --      "
        self.str_param1.set(self.SAFE_VALUE)
        self.str_param2.set(self.THRESHOLD)
        self._param1_entry["style"] = "Green.TEntry"
        self._param2_entry["style"] = "Green.TEntry"
        self._param3_entry["style"] = "Grey.TEntry"
        self._param4_entry["style"] = "Grey.TEntry"
        self.str_comment.set("Param1 = SAFE and Param2 = Threshold.")
        # If you switch algorithms, this will stop the plot from redrawing (may
        # not have the data yet to do so).
        if self.controller.calc_btn_hit == 1 and self.algo_choice != self.prev_algo:
            self.controller.calc_btn_hit = 0
        self.prev_algo = 2

    def click_algo3(self):
        'Set the text for the 4 buttons based on this 3rd radio button being hit'
        self.opt_btn1["text"] = "      -- Not Used --      "
        self.opt_btn2["text"] = "      -- Not Used --      "
        self.opt_btn3["text"] = "      -- Not Used --      "
        self.opt_btn4["text"] = "      -- Not Used --      "
        self.str_param1.set(self.SAFE_VALUE)
        self.str_param2.set(self.THRESHOLD)
        self._param1_entry["style"] = "Grey.TEntry"
        self._param2_entry["style"] = "Grey.TEntry"
        self._param3_entry["style"] = "Grey.TEntry"
        self._param4_entry["style"] = "Grey.TEntry"
        self.str_comment.set("Param1 = ? and Param2 = ?.")
        # If you switch algorithms, this will stop the plot from redrawing (may
        # not have the data yet to do so).
        if self.controller.calc_btn_hit == 1 and self.algo_choice != self.prev_algo:
            self.controller.calc_btn_hit = 0
        self.prev_algo = 3

    def click_algo4(self):
        'Set the text for the 4 buttons based on this 4th radio button being hit'
        self.opt_btn1["text"] = "      -- Not Used --      "
        self.opt_btn2["text"] = "      -- Not Used --      "
        self.opt_btn3["text"] = "      -- Not Used --      "
        self.opt_btn4["text"] = "      -- Not Used --      "
        self.str_param1.set(self.SAFE_VALUE)
        self.str_param2.set(self.THRESHOLD)
        self._param1_entry["style"] = "Grey.TEntry"
        self._param2_entry["style"] = "Grey.TEntry"
        self._param3_entry["style"] = "Grey.TEntry"
        self._param4_entry["style"] = "Grey.TEntry"
        self.str_comment.set("Param1 = ? and Param2 = ?.")
        # If you switch algorithms, this will stop the plot from redrawing (may
        # not have the data yet to do so).
        if self.controller.calc_btn_hit == 1 and self.algo_choice != self.prev_algo:
            self.controller.calc_btn_hit = 0
        self.prev_algo = 4

    def click_plot_none(self):
        'Call if the "no plots" option is checked.'
        self.prev_plot_choice = 0
        if self.plot_choice0.get() == 1:  # then "none" plot is selected, so deselect all other checkboxes
            self.plot_choice5.set(0)
            self.plot_choice11.set(0)
            self.plot_choice21.set(0)
            self.plot_choice41.set(0)
            self.plot_choice81.set(0)
            self.plot_choice161.set(0)
            self.plot_choice251.set(0)
            self.plot_choice_all = 0
            if self.par5 != None:
                for item in self.p5:
                    #print ("1 - Removing curve = " + str(id(item[0])))
                    item[0].remove()
                del self.p5[:]
                self.data_plot.draw()

        # if all other plots are deselected, select the "none" checkbox, even if the user just turned it off
        if (self.plot_choice5.get() == 0 and
                self.plot_choice11.get() == 0 and
                self.plot_choice21.get() == 0 and
                self.plot_choice41.get() == 0 and
                self.plot_choice81.get() == 0 and
                self.plot_choice161.get() == 0 and
                self.plot_choice251.get() == 0):
            self.plot_choice0.set(1)

    def click_plot(self):
        """Called when one of the plot checkboxes is clicked, also at the end 
        of plotting (to redraw the plots)."""
        self.plot_choice0.set(0)  # clear None button
        self.plot_choice_all = 0
        if self.plot_choice5.get() == 1:
            self.plot_choice_all = self.plot_choice_all | 1
        elif (self.prev_plot_choice & 1) == 1:  # then this guy was deselected just now
            self.remove_from_list_by_bit_flag(1)
        if self.plot_choice11.get() == 1:
            self.plot_choice_all = self.plot_choice_all | 2
        elif (self.prev_plot_choice & 2) == 2:
            self.remove_from_list_by_bit_flag(2)
        if self.plot_choice21.get() == 1:
            self.plot_choice_all = self.plot_choice_all | 4
        elif (self.prev_plot_choice & 4) == 4:
            self.remove_from_list_by_bit_flag(4)
        if self.plot_choice41.get() == 1:
            self.plot_choice_all = self.plot_choice_all | 8
        elif (self.prev_plot_choice & 8) == 8:
            self.remove_from_list_by_bit_flag(8)
        if self.plot_choice81.get() == 1:
            self.plot_choice_all = self.plot_choice_all | 16
        elif (self.prev_plot_choice & 16) == 16:
            self.remove_from_list_by_bit_flag(16)
        if self.plot_choice161.get() == 1:
            self.plot_choice_all = self.plot_choice_all | 32
        elif (self.prev_plot_choice & 32) == 32:
            self.remove_from_list_by_bit_flag(32)
        if self.plot_choice251.get() == 1:
            self.plot_choice_all = self.plot_choice_all | 64
        elif (self.prev_plot_choice & 64) == 64:
            self.remove_from_list_by_bit_flag(64)

        # if all other plots are deselected, select the "none" checkbox
        if self.plot_choice_all == 0:
            self.plot_choice0.set(1)

        elif self.prev_plot_choice <= self.plot_choice_all:
            if self.par5 is None:
                self.par5 = self.host.twinx()
            elif self.par5 is not None: # temp change to fix zorder issues
                self.par5.remove()
                self.par5 = self.host.twinx()

            if self.plot_choice_all > 0:
                len_closes = len(self.controller.model.closes)
                just_ints = np.arange(len_closes)

                # For color names, see:
                # http://stackoverflow.com/questions/22408237/named-colors-in-matplotlib

                #optParam3 = self.controller.model.getOptParam3()
                this_choice = self.plot_choice_all
                if (this_choice & 0x1) != 0 and len_closes > 5:
                    temp, = self.par5.plot(just_ints, self.controller.model.ave_5_days, "r-", zorder=11)
                    self.p5.insert(0, (temp, 0x1))
                if (this_choice & 0x2) != 0 and len_closes > 11:
                    temp, = self.par5.plot(just_ints, self.controller.model.ave_11_days, "r-", zorder=11)
                    self.p5.insert(0, (temp, 0x2))
                if (this_choice & 0x4) != 0 and len_closes > 21:
                    temp, = self.par5.plot(just_ints, self.controller.model.ave_21_days, "r-")
                    self.p5.insert(0, (temp, 0x4))
                if (this_choice & 0x8) != 0 and len_closes > 41:
                    temp, = self.par5.plot(just_ints, self.controller.model.ave_41_days, "r-")
                    self.p5.insert(0, (temp, 0x8))
                if (this_choice & 0x10) != 0 and len_closes > 81:
                    temp, = self.par5.plot(just_ints, self.controller.model.ave_81_days, "r-")
                    self.p5.insert(0, (temp, 0x10))
                if (this_choice & 0x20) != 0 and len_closes > 161:
                    temp, = self.par5.plot(just_ints, self.controller.model.ave_161_days, "r-")
                    self.p5.insert(0, (temp, 0x20))
                if (this_choice & 0x40) != 0 and len_closes > 251:
                    temp, = self.par5.plot(just_ints, self.controller.model.ave_251_days, "r-")
                    self.p5.insert(0, (temp, 0x40))
                View.make_patch_spines_invisible(self.par5)
                self.par5.spines["right"].set_visible(False)
                self.par5.get_yaxis().set_visible(False)
                self.par5.set_ylim(self.host.get_ylim())
                self.host.set_xlim(0, len_closes-1)

        self.data_plot.draw()
        self.prev_plot_choice = self.plot_choice_all


    def remove_from_list_by_bit_flag(self, bitflag):
        'helper function to remove one of the average plots'
        for item in self.p5:
            if bitflag == item[1]:
                #print ("2 - Removing curve = " + str(id(item[0])))
                item[0].remove()
                self.p5.remove(item)

    @staticmethod
    def make_patch_spines_invisible(axis):
        'code from a site that had plot examples'
        axis.set_frame_on(True)
        axis.patch.set_visible(False)
        for spine in axis.spines.values():
            spine.set_visible(False)

    def resize_func(self, event):
        'function triggered when the window is resized; we need to redraw the plot'
        #w, h, t = event.width, event.height, event.type
        w_real = self.root.winfo_width()
        if self.controller.calc_btn_hit == 1 and self.saved_window_width != w_real:
            self.saved_window_width = w_real
            #safeEntry.width = w_real / 4.0
            #mainframe.itemconfigure("safeEntry", width=(w_real / 4.0))
            #dpi = 120.0  # at some point - get real value here
            self.plot_it()

    # inputs - tick value = x and position = pos
    def format_date(self, tick_val, pos=None):
        'helper function to format the date string along the x-axis'
        thisind = np.clip(int(tick_val + 0.5), 0, len(self.controller.model.closes) - 1)
        the_date = date.fromordinal(int(self.dates[thisind]))
        return the_date.strftime('%b-%e-%Y') # m d Y in gui date boxes

    def plot_it(self):
        'Main plot routine to draw the big graph w/ all the plots in it'
#         print ("About to clear plots, thread={}, threadID={}, MPL ver={}".format(
#             current_thread().name, current_thread().ident, mpl.__version__))
        self.clear_plots()

#         optParam3 = self.controller.model.getOptParam3()
#         optParam4 = self.controller.model.getOptParam4()
        len_closes = len(self.controller.model.closes)
        #algo = self.algo_choice.get()

        self.dates = [q[0] for q in self.controller.model.quotes]
        self.host.grid(True)  # this works, turns on minor grids
        self.saved_window_width = self.root.winfo_width()
        just_ints = np.arange(len_closes)

        # Using twinx - Having been created by twinx, par1 or par2 will have its frame off,
        # so the line of its detached spine is invisible.  You will have to fix that later.
        # The ticks and label will be placed on the right in this twinx call.
        self.par1 = self.host.twinx()
        self.par2 = self.host.twinx()

        self.p1, = self.host.plot(just_ints, self.controller.model.closes, "b-", linewidth=1.0)
        #host_ylim = self.host.get_ylim() # may need this value for certain plots
        self.host.set_xlabel("Time")
        self.host.set_ylabel("Stock Price ($)")
        tkw = dict(size=4, width=1.5)

        order2 = [x * -1 for x in self.controller.model.order] # flip sign of each array element using list comprehension
        self.p2, = self.par1.plot(just_ints, self.controller.model.pv, "r--", linewidth=1.0)
        self.p3, = self.par2.plot(just_ints, order2, "go", markersize=3.0)
        self.par2.set_ylabel("Orders ($)")          # you'll have to customize this for other algorithms
        self.par1.set_ylabel("Portfolio Value ($)") # ditto
        self.par2.spines["right"].set_position(("axes", 1.16)) # offset the right spine of par2
        View.make_patch_spines_invisible(self.par2) # activate the frame but make the patch and spines invisible
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
        self.host.set_xlim(0, len_closes-1)
        self.host.autoscale_view()

        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        self.fig.autofmt_xdate(rotation=60)#, bottom=0.2) # change bottom so "Time" label is visible

        # draw the legend
        #lines = [self.p1, self.p2, self.p3]
        #self.host.legend(lines, [l.get_label() for l in lines])

        self.prev_plot_choice = 0
        self.fig.tight_layout()
        self.click_plot()

        window_size = self.fig.get_size_inches()   # gives window size (grey area, not the plot area)
        #fig_size = plt.rcParams["figure.figsize"] # always gives 8x6 even if window is resized
        #print ("(view-plot) plot size is {:.3f} x {:.3f} inches (wxh); dpi=80".format(window_size[0], window_size[1]))
        self.controller.model.set_horz_size(window_size[0])


    def clear_plots(self):
        'Clear all plots from the graph'
        #print ("CLEARING PLOTS.....................")
        if self.p1 != None:
            try:
                self.p1.remove()  # these calls work good to remove the old plot and axes
            except BaseException as exc:
                print("EXCEPTION OCCURRED IN view.PY, trying to remove p1, IN clear_plots FUNCTION - " + str(exc))
            try:
                self.p2.remove()
            except BaseException as exc:
                print("EXCEPTION OCCURRED IN view.PY, trying to remove p2, IN clear_plots FUNCTION - " + str(exc))
            try:
                self.p3.remove()
            except BaseException as exc:
                print("EXCEPTION OCCURRED IN view.PY, trying to remove p3, IN clear_plots FUNCTION - " + str(exc))
            if self.p5 != None:
                counter = 1
                while counter <= 64:
                    if (self.prev_plot_choice & counter) == counter:
                        self.remove_from_list_by_bit_flag(counter)
                    counter *= 2
            self.host.cla()   # this is very important so the axes get reset each time
            try:
                self.par1.cla()
                self.par1.clear()
                self.par1.remove()
            except BaseException as exc:
                print("EXCEPTION OCCURRED IN view.PY, trying to remove par1, IN clear_plots FUNCTION - " + str(exc))
            try:
                if self.par2 != None:
                    self.par2.cla()
                    self.par2.clear()
                    self.par2.remove()
            except BaseException as exc:
                print("EXCEPTION OCCURRED IN view.PY, trying to remove par2, IN clear_plots FUNCTION - " + str(exc))
            try:
                if self.par5 != None:
                    self.par5.remove()
                    self.par5 = self.host.twinx()
                    self.par5.spines["right"].set_visible(False)
                    self.par5.get_yaxis().set_visible(False)
                    self.par5.set_ylim(self.host.get_ylim())
            except BaseException as exc:
                print("EXCEPTION OCCURRED IN view.PY, trying to remove par5, IN clear_plots FUNCTION - " + str(exc))
        plt.close("all") # see if this works

    #     plt.clf()  # these 3 calls clear the entire graph, but the host graph and axes never come back
    #     plt.cla()
    #     plt.close()
        #plt.close() # don't do this or the app will close (mainloop will exit); not sure why
