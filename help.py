"""
The HelpDialog class, which derives from tkSimpleDialog.Dialog.
"""

import tkinter as tk
from tkinter import ttk, Frame, Button, ACTIVE
#from tkinter.scrolledtext import ScrolledText
import tkSimpleDialog

# This code based on ideas at - http://effbot.org/tkinterbook/tkinter-dialog-windows.htm


class HelpDialog(tkSimpleDialog.Dialog):
    """
    Simple help dialog class.

    The help dialog will have multiple tabs; each tab has a name, and the tab body has relevant text.
    I came up with a simple file format for help.txt just for fun (see help.txt):
    - Each tab section starts with ###TAB= followed by the tab name.
    - After the tab name follows all that tab's text, up to the next tab section start (or end of file).
    """

    def body(self, master):
        'override body fn to create one dialog with multiple tabs, each tab having its own text.'
        all_lines = []       # list of all lines in the file
        all_tab_names = []    # list of all the tab names found
        all_text_strings = [] # list of all text w/in a tab (all as one long string per tab)
        one_long_string = ""
        num_tabs = 0
        new_tab_started = True

        with open(self.filename) as file_obj:  # read the whole file as a list of strings
            all_lines = file_obj.readlines()

        # Loop to process each line in the file. Tab starter lines are special.
        # All other text w/in a tab section is concatenated into one long string.
        for each_line in all_lines:
            if each_line[:7] == "###TAB=":  # detect tab starter line
                new_tab_started = True
                each_line = each_line.rstrip('\n')
                all_tab_names.append(each_line[7:]) # save the tab name text
                #print ("tab = " + str(all_tab_names[num_tabs]))
                num_tabs += 1
                if num_tabs > 1:
                    all_text_strings.insert(num_tabs-2, one_long_string)
            else:
                #print ("line = " + each_line)
                if new_tab_started:
                    one_long_string = each_line
                    new_tab_started = False
                else:
                    one_long_string += each_line # concatenate text w/in a tab into one long string
        if num_tabs > 1:
            all_text_strings.insert(num_tabs-1, one_long_string)

        # Now that we have all the help.txt data, create the notebook widget and fill it up.
        nt_book = ttk.Notebook(master, padding=0, height=560, width=780) # create notebook
        for tab_index in range(0, num_tabs):
            page = ttk.Frame(nt_book, borderwidth=1, relief="sunken", width=180, height=180) # create one page in notebook
            scroll_bar = tk.Scrollbar(page)
            msg = tk.Text(page, wrap='word', yscrollcommand=scroll_bar.set,
                          borderwidth=0, highlightthickness=0)
            scroll_bar.config(command=msg.yview)
            scroll_bar.pack(side="right", fill="y")
            msg.pack(side='left', fill="both", expand=True)
            msg.insert(tk.INSERT, all_text_strings[tab_index])
            nt_book.add(page, text=all_tab_names[tab_index])
        nt_book.pack(expand=1, fill="both")


    def button_box(self):
        'override the default ok/cancel btns to provide one Exit button'
        box = Frame(self)
        widget = Button(box, text="Exit", width=10, command=self.ok, default=ACTIVE)
        widget.pack(padx=5, pady=5)
        self.bind("<Return>", self.ok)
        box.pack()
