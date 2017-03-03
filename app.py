"""
Main entry point for application.
- Creates the root Tk object
- Creates the controller object
- Runs the controller object

MVC template from:
  https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/
"""

import matplotlib       # do this before the next line
matplotlib.use('TkAgg') # and make sure this is done before the next line
from matplotlib import pyplot as plt
from tkinter import Tk  # use Tkinter for python 2, tkinter for python 3
from controller import Controller

if __name__ == '__main__':
    root = Tk()
    matplotlib.interactive(0)   # turn off interaction of TkAgg
    cntlr = Controller(root)
    cntlr.run()
    print("shutting down")
    plt.close("all")
