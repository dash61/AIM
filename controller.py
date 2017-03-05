"""
Controller class for application.

MVC template from:
  https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/
"""


import re
import tkinter as tk
from tkinter import messagebox
import datetime
#from datetime import timedelta
from view import View
from model import Model
from help import HelpDialog


class Controller(tk.Frame):
    'Controller class of the MVC architecture.'
    def __init__(self, master=None, *args, **kwargs):
        'Constructor'
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.root = master
        self.view = View(self, self.root)
        self.model = Model()
        self.view.inv_entry.focus()
        self.root.bind('<Return>', self.calculate_1_enter_key)
        self.root.bind("<Configure>", self.view.resize_func)
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.calc_btn_hit = 0

    def __del__(self):
        'Destructor, just to see if/when it gets called'
        print(id(self), 'died')

    def close_app(self):
        'Function called when the close button is hit'
        print("Got WM_DELETE_WINDOW msg")
        self.root.quit()

    def convert_start_end_dates(self):
        'Helper function to convert start/end dates to real date objects'
        list_start_date = re.split('[- /]', self.view.str_start_date.get()) # split date into fields
        listend_date = re.split('[- /]', self.view.str_end_date.get()) # split date into fields
        if list_start_date[0] == "MM" or listend_date[0] == "MM":
            messagebox.showerror("ERROR", "Make sure *both* start and end dates are filled in!")
            return (None, None)

        datestart_date = datetime.date(int(list_start_date[2]), int(list_start_date[0]), int(list_start_date[1]))
        dateend_date = datetime.date(int(listend_date[2]), int(listend_date[0]), int(listend_date[1]))
        return (datestart_date, dateend_date)

    def pre_calculate(self):
        'Code to run before one of the four algorithms gets run'
        self.model.set_stock_symbol(self.view.str_stock_name.get())
        (start_date, end_date) = self.convert_start_end_dates() # convert strings to real Date objects
        self.model.set_start_date(start_date)
        self.model.set_end_date(end_date)
        self.model.set_investment(self.view.str_investment.get())
        self.model.set_opt_params(self.view.str_param1.get(), self.view.str_param2.get(), self.view.str_param3.get(), self.view.str_param4.get())

    def calculate_1_enter_key(self, event):
        'Function called if the RETURN key is hit.'
        self.calculate()

    def calc_opt_param1(self):
        'Calc optimum value for parameter #1 for the selected algorithm'
        algo = self.view.algo_choice.get()
        if algo == 1 or algo == 2:
            self.model.set_opt_param1_mode(True)
            self.calculate()  # loop to calc best param1
            self.model.set_opt_param1_mode(False)
            self.calculate()  # redo calc and graphs w/ best param1 chosen

    def calc_opt_param2(self):
        'Calc optimum value for parameter #2 for the selected algorithm'
        algo = self.view.algo_choice.get()
        if algo == 1 or algo == 2:
            self.model.set_opt_param2_mode(True)
            self.calculate()
            self.model.set_opt_param2_mode(False)
            self.calculate()  # redo calc and graphs w/ best param2 chosen

    def calc_opt_param3(self):
        'Calc optimum value for parameter #3 for the selected algorithm'
        pass
        #algo = self.view.algo_choice.get()

    def calc_opt_param4(self):
        'Calc optimum value for parameter #4 for the selected algorithm'
        pass
        #algo = self.view.algo_choice.get()

    def calculate(self):
        'Run one of the four algorithms.'
        self.pre_calculate()
        algo = self.view.algo_choice.get()
        if algo == 1:
            success = self.model.calculate1()
        elif algo == 2:
            success = self.model.calculate2()
        elif algo == 3:
            success = self.model.calculate3()
        else:
            success = self.model.calculate4()
        if success:
            self.post_calculate()

    def post_calculate(self):
        'Code to run after one of the four algorithms gets run'
        self.calc_btn_hit = 1
        self.view.str_PV.set("$ " + str(self.model.get_ending_PV())) # strPV.set ("$ " + str(pv[len(pv)-1]))
        self.view.str_SV.set("$ " + str(self.model.get_ending_SV()))
        self.view.str_cash.set("$ " + str(self.model.get_ending_cash()))
        self.view.str_num_trans.set(str(self.model.get_num_trans()))
        self.view.str_num_data_points.set(str(self.model.get_num_data_points()))
        self.view.str_start_shares_owned.set(str(self.model.get_starting_shares()))
        self.view.str_final_shares_owned.set(str(self.model.get_ending_shares()))
        self.view.str_annual_ROI_val.set(str(self.model.get_ROI()))
        algo = self.view.algo_choice.get()
        if algo == 1:
            self.view.str_param1.set(str(self.model.get_opt_param1()))
            self.view.str_param2.set(str(self.model.get_opt_param2()))
        elif algo == 2:
            self.view.str_param1.set(str(self.model.get_opt_param1()))
            self.view.str_param2.set(str(self.model.get_opt_param2()))
        elif algo == 3:
            self.view.str_param1.set(str(self.model.get_opt_param1()))
            self.view.str_param2.set(str(self.model.get_opt_param2()))
        else:
            self.view.str_param1.set(str(self.model.get_opt_param1()))
            self.view.str_param2.set(str(self.model.get_opt_param2()))
            self.view.str_param3.set(str(self.model.get_opt_param3()))
        self.view.plot_it()

    def help(self):
        'Function called when the help button is hit.'
        #helpDlg = HelpDialog(self.root, filename="help.txt")
        HelpDialog(self.root, filename="help.txt")
        #self.root.wait_window(helpDlg.top)


    def run(self):
        'Main loop of the app; called from app.py'
        self.root.title("AIM")
        self.root.deiconify()
        self.root.mainloop()
