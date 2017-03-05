"""
A class for a generic dialog.

Taken from:  http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
"""

from tkinter import Toplevel, Frame, Button, ACTIVE, LEFT


class Dialog(Toplevel):
    'Generic dialog class'

    def __init__(self, parent, title=None, filename=None):
        'Constructor'
        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.filename = ""

        if title:
            self.title(title)

        if filename:
            self.filename = filename

        self.parent = parent
        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        self.button_box()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))

        self.initial_focus.focus_set()
        self.wait_window(self)

    #
    # 
    def body(self, master):
        """construction hooks.
        
        Create dialog body.  Return widget that should have
        initial focus.  This method should be overridden."""
        pass

    def button_box(self):
        """add standard button box.
        
        override if you don't want the standard buttons."""
        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics
    def ok(self, event=None):
        'Handle the OK button press'
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        'Handle the Cancel button press'
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks
    def validate(self):
        'Hook to validate the commands. Override as needed.'
        return 1 # override

    def apply(self):
        'Optional override to do stuff when OK button is hit.'
        pass # override
