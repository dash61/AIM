#!/usr/bin/python
# -*- coding: utf-8

import tkinter as tk
from tkinter import Tk, ttk, Text, Frame, Button, ACTIVE, WORD
from tkinter.scrolledtext import ScrolledText
import tkSimpleDialog

"""
The help dialog will have multiple tabs; each tab has a name, and the tab body has relevant text.
I came up with a simple file format for help.txt just for fun (see help.txt):
- Each tab section starts with ###TAB= followed by the tab name.
- After the tab name follows all that tab's text, up to the next tab section start (or end of file).
"""

class HelpDialog(tkSimpleDialog.Dialog):

	# override body fn to create one dialog with multiple tabs, each tab having its own text.
	def body(self, master):
		allLines = []       # list of all lines in the file
		allTabNames = []    # list of all the tab names found
		allTextStrings = [] # list of all text w/in a tab (all as one long string per tab)
		oneLongString = ""
		numTabs = 0
		newTabStarted = True
		
		with open(self.filename) as f:  # read the whole file as a list of strings
			allLines = f.readlines()
			
		# Loop to process each line in the file. Tab starter lines are special.
		# All other text w/in a tab section is concatenated into one long string.
		for eachLine in allLines:
			if eachLine[:7] == "###TAB=":  # detect tab starter line
				newTabStarted = True
				eachLine = eachLine.rstrip('\n')
				allTabNames.append(eachLine[7:]) # save the tab name text
				#print ("tab = " + str(allTabNames[numTabs]))
				numTabs += 1
				if (numTabs > 1):
					allTextStrings.insert(numTabs-2, oneLongString)
			else:
				#print ("line = " + eachLine)
				if newTabStarted:
					oneLongString = eachLine
					newTabStarted = False
				else:
					oneLongString += eachLine # concatenate text w/in a tab into one long string
		if (numTabs > 1):
			allTextStrings.insert(numTabs-1, oneLongString)
			
		# Now that we have all the help.txt data, create the notebook widget and fill it up.
		nb = ttk.Notebook(master, padding=0, height=560, width=780) # create notebook
		for tabIndex in range(0, numTabs):
			page = ttk.Frame (nb, borderwidth=1, relief="sunken", width=180, height=180) # create one page in notebook
			scrollbar = tk.Scrollbar(page)
			msg = tk.Text (page, wrap='word', yscrollcommand=scrollbar.set,
							borderwidth=0, highlightthickness=0)
			scrollbar.config(command=msg.yview)
			scrollbar.pack(side="right", fill="y")
			msg.pack(side='left', fill="both", expand=True)
			msg.insert(tk.INSERT, allTextStrings[tabIndex])
			nb.add(page, text=allTabNames[tabIndex])
		nb.pack(expand=1, fill="both")


	# override the default ok/cancel btns to provide one Exit button
	def buttonbox(self):
		box = Frame(self)
		w = Button(box, text="Exit", width=10, command=self.ok, default=ACTIVE)
		w.pack(padx=5, pady=5)
		self.bind("<Return>", self.ok)
		box.pack()
