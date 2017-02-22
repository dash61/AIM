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
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.root = master
        self.view = View(self, self.root)
        self.model = Model()
        self.view.invEntry.focus()
        self.root.bind('<Return>', self.calculate1EnterKey)
        self.root.bind("<Configure>", self.view.resize_func)
        self.root.protocol("WM_DELETE_WINDOW", self.closeApp)
        self.calc_btn_hit = 0

    def __del__(self):
        print(id(self), 'died')

    def closeApp(self):
        print("Got WM_DELETE_WINDOW msg")
        self.root.quit()

    def convertStartEndDates(self):
        listStartDate = re.split('[- /]', self.view.strStartDate.get()) # split date into fields
        listEndDate = re.split('[- /]', self.view.strEndDate.get()) # split date into fields
        if listStartDate[0] == "MM" or listEndDate[0] == "MM":
            messagebox.showerror("ERROR", "Make sure *both* start and end dates are filled in!")
            return (None, None)

        dateStartDate = datetime.date(int(listStartDate[2]), int(listStartDate[0]), int(listStartDate[1]))
        dateEndDate = datetime.date(int(listEndDate[2]), int(listEndDate[0]), int(listEndDate[1]))
        return (dateStartDate, dateEndDate)

    def preCalculate(self):
        self.model.setStockSymbol(self.view.strStockName.get())
        (startDate, endDate) = self.convertStartEndDates() # convert strings to real Date objects
        self.model.setStartDate(startDate)
        self.model.setEndDate(endDate)
        self.model.setInvestment(self.view.strInvestment.get())
        self.model.setOptParams(self.view.strParam1.get(), self.view.strParam2.get(), self.view.strParam3.get(), self.view.strParam4.get())

    def calculate1EnterKey(self, event):
        self.calculate()

    # Calc optimum value for parameter #1 for the selected algorithm
    def calcOptParam1(self):
        algo = self.view.algo_choice.get()
        if algo == 1 or algo == 2:
            self.model.setOptParam1Mode(True)
            self.calculate()  # loop to calc best param1
            self.model.setOptParam1Mode(False)
            self.calculate()  # redo calc and graphs w/ best param1 chosen

    # Calc optimum value for parameter #2 for the selected algorithm
    def calcOptParam2(self):
        algo = self.view.algo_choice.get()
        if algo == 1 or algo == 2:
            self.model.setOptParam2Mode(True)
            self.calculate()
            self.model.setOptParam2Mode(False)
            self.calculate()  # redo calc and graphs w/ best param2 chosen

    # Calc optimum value for parameter #3 for the selected algorithm
    def calcOptParam3(self):
        pass
        #algo = self.view.algo_choice.get()

    # Calc optimum value for parameter #4 for the selected algorithm
    def calcOptParam4(self):
        pass
        #algo = self.view.algo_choice.get()

    def calculate(self):
        self.preCalculate()
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
            self.postCalculate()

    def postCalculate(self):
        self.calc_btn_hit = 1
        self.view.strPV.set("$ " + str(self.model.getEndingPV())) # strPV.set ("$ " + str(pv[len(pv)-1]))
        self.view.strSV.set("$ " + str(self.model.getEndingSV()))
        self.view.strCash.set("$ " + str(self.model.getEndingCash()))
        self.view.strNumTrans.set(str(self.model.getNumTrans()))
        self.view.strNumDataPoints.set(str(self.model.getNumDataPoints()))
        self.view.strStartSharesOwned.set(str(self.model.getStartingShares()))
        self.view.strFinalSharesOwned.set(str(self.model.getEndingShares()))
        self.view.strAnnualROIVal.set(str(self.model.getROI()))
        algo = self.view.algo_choice.get()
        if algo == 1:
            self.view.strParam1.set(str(self.model.getOptParam1()))
            self.view.strParam2.set(str(self.model.getOptParam2()))
        elif algo == 2:
            self.view.strParam1.set(str(self.model.getOptParam1()))
            self.view.strParam2.set(str(self.model.getOptParam2()))
        elif algo == 3:
            self.view.strParam1.set(str(self.model.getOptParam1()))
            self.view.strParam2.set(str(self.model.getOptParam2()))
        else:
            self.view.strParam1.set(str(self.model.getOptParam1()))
            self.view.strParam2.set(str(self.model.getOptParam2()))
            self.view.strParam3.set(str(self.model.getOptParam3()))
        self.view.plotIt()

    def help(self):
        #helpDlg = HelpDialog(self.root, filename="help.txt")
        HelpDialog(self.root, filename="help.txt")
        #self.root.wait_window(helpDlg.top)


    def run(self):
        self.root.title("AIM")
        self.root.deiconify()
        self.root.mainloop()
