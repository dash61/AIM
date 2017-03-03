"""
Second algorithm function for application. Intentionally copied from the 1st, and then modified,
just to show how to do multiple algorithms.

This algorithm is based on the book "How to Make $1,000,000 in the Stock Market Automatically",
by Robert Lichello, but has 2 modifications (see comments below in the core_calculate2 function).
"""

def calculate2(self):
    'Calculate ROI and other params given historical stock data using a modified AIM algorithm.'
    try:
        self.quotes = self.get_stock_data_from_internet(self.start_date, self.end_date)
        if self.quotes is None:
            return False
        self.closes = [q[2] for q in self.quotes]

        del self.pv[:]          # portfolio value
        del self.sv[:]          # stock value
        del self.cash[:]        # accumulated cash, cash on hand
        del self.pcntl[:]       # portfolio control, hard to explain
        del self.order[:]       # an order to buy or sell shares, in dollars
        del self.shares_owned[:] # num shares owned
        self.pv    += [0.0] * len(self.closes)
        self.sv    += [0.0] * len(self.closes)
        self.cash  += [0.0] * len(self.closes)
        self.pcntl += [0.0] * len(self.closes)
        self.order += [0.0] * len(self.closes)
        self.shares_owned += [0.0] * len(self.closes)

        # MODIFIED AIM ALGORITHM:
        self.pv[0]    = float(self.str_investment)
        self.sv[0]    = self.pv[0] / 2
        self.cash[0]  = self.sv[0]
        self.pcntl[0] = self.sv[0]
        self.order[0] = 0.0
        self.numTrans = 0
        self.shares_owned[0] = self.sv[0] / self.closes[0]
        self.numDataPoints  = len(self.closes)
        safe_float     = self.opt_param1
        thresh_float   = self.opt_param2

        self.calc_averages()

        if self.bLoop_on_param1:
            max_ROI = 0.0
            best_safe = 0.0
            for outer_index in range(0, 150):
                self.core_calculate2(outer_index / 10.0, thresh_float)
                if self.annual_ROI > max_ROI:
                    max_ROI = self.annual_ROI
                    best_safe = outer_index / 10.0
            self.opt_param1 = best_safe
        elif self.bLoop_on_param2:
            max_ROI = 0.0
            best_thresh = 0.0
            for outer_index in range(0, 500, 5):
                self.core_calculate2(safe_float, float(outer_index))
                if self.annual_ROI > max_ROI:
                    max_ROI = self.annual_ROI
                    best_thresh = float(outer_index)
            self.opt_param2 = best_thresh
        else:
            self.core_calculate2(safe_float, thresh_float)

        return True

    except BaseException as exc:
        print("EXCEPTION OCCURRED IN ALGO2.PY, IN calculate2 FUNCTION - " + str(exc))


# Note that this loops through all stock prices in the self.closes list, then
# rounds the floating point values afterwards.
def core_calculate2(self, safe_float, thresh_float):
    'Core calc broken out so it can be looped upon to optimize certain values.'
    for index in range(1, len(self.closes)):
        val = self.closes[index]
        self.sv[index] = self.shares_owned[index-1] * val
        safe_val = self.sv[index] * safe_float * 0.01
        self.cash[index] = self.cash[index-1] - self.order[index-1]
        self.pv[index] = self.sv[index] + self.cash[index]
        advice = self.pcntl[index-1] - self.sv[index]
        if safe_val > abs(advice):
            self.order[index] = 0.0
        else:
            if advice < 0.0:
                self.order[index] = advice + safe_val
            else:
                self.order[index] = advice - safe_val

        # MODIFICATION #1 - THIS FIRST 'IF' STMT:
        if self.order[index] > self.cash[index]:     # if buying, and the order is more than the cash we have, change order
            self.order[index] = self.cash[index] / 2.0 # use half the cash instead - new algorithm per drl
        if self.order[index] < thresh_float and self.order[index] > (thresh_float * -1.0):
            self.order[index] = 0.0
        bors = self.order[index] / val    # stands for 'buy or sell'
        if bors != 0.0:
            self.numTrans = self.numTrans + 1
        self.shares_owned[index] = self.shares_owned[index-1] + bors
        # MODIFICATION #2 - NEXT STMT:
        self.pcntl[index] = self.pcntl[index-1] + self.order[index] / 2.0 # will alter pcntl on buy OR sell

    self.sv = [round(elem, 2) for elem in self.sv] # round off floating pt values to 2 decimal places
    self.pv = [round(elem, 2) for elem in self.pv]
    self.cash = [round(elem, 2) for elem in self.cash]
    self.order = [round(elem, 2) for elem in self.order]
    self.pcntl = [round(elem, 2) for elem in self.pcntl]
    self.shares_owned = [round(elem, 1) for elem in self.shares_owned]
    self.annual_ROI = self.calc_ROI(self.start_date, self.end_date)
