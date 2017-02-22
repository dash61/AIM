## Overview

This sample Python application was developed to test out certain stock algorithms. It has two implemented algorithms, the first taken from the book "How to Make $1,000,000 in the Stock Market Automatically", by Robert Lichello. The second is just a variation of that.

The application takes in a stock symbol, starting investment amount, and start and end dates, and then downloads the stock data on that stock from Yahoo finance. It then runs the selected algorithm on that block of stock prices and graphs the result.

The idea is to start with an initial investment, say $10000, and split that into 2 pieces: 1) $5000 cash, and 2) $5000 in stock.
After that, for each new stock price fed into the AIM 'machine', it advises whether to hold, buy or sell. Note that the algorithm itself divides the initial investment in half and makes the initial stock purchase; you just have to supply the total initial investment amount.

This program is meant to test out that algorithm (and possibly others) using historical stock data from Yahoo, crunching the numbers to see how much money would be gained or lost. The algorithm works best for volatile stocks.
It splits each algorithm out into it's own file (algo1.py through algo4.py). The GUI is laid out with tk's grid mechanism, which means it is a series of rows and columns (4 columns are used).

There is a help button that brings up a multi-tabbed help dialog with more specific information.


### Basic Usage

To run the program:

- $ python3 app.py

(that is, run with python version 3). Or you can run it inside your favorite Python editor.

To use the program:

- Fill out the stock symbol, start and end dates, and starting investment.
- Select the algorithm.
- Hit the "Run Selected Algorithm" button (or hit RETURN).