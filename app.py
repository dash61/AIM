#!/usr/bin/python
# -*- coding: utf-8

# MVC template from: https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/


from tkinter import Tk  # use Tkinter for python 2, tkinter for python 3
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from controller import Controller

if __name__ == '__main__':
	root = Tk()
	matplotlib.interactive(0)   # turn off interaction of TkAgg
	c = Controller(root)
	c.run()
	print ("shutting down")
	plt.close("all")
