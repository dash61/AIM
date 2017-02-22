"""
Second algorithm function for application. Intentionally copied from the 1st, and then modified,
just to show how to do multiple algorithms.

This algorithm is based on the book "How to Make $1,000,000 in the Stock Market Automatically",
by Robert Lichello, but has 2 modifications (see comments below in the coreCalculate2 function).
"""

def calculate2(self):
    try:
        self.quotes = self.getStockDataFromInternet(self.startDate, self.endDate)
        if self.quotes is None:
            return False
        self.closes = [q[2] for q in self.quotes]

        del self.pv[:]          # portfolio value
        del self.sv[:]          # stock value
        del self.cash[:]        # accumulated cash, cash on hand
        del self.pcntl[:]       # portfolio control, hard to explain
        del self.order[:]       # an order to buy or sell shares, in dollars
        del self.sharesOwned[:] # num shares owned
        self.pv    += [0.0] * len(self.closes)
        self.sv    += [0.0] * len(self.closes)
        self.cash  += [0.0] * len(self.closes)
        self.pcntl += [0.0] * len(self.closes)
        self.order += [0.0] * len(self.closes)
        self.sharesOwned += [0.0] * len(self.closes)

        # MODIFIED AIM ALGORITHM:
        self.pv[0]    = float(self.strInvestment)
        self.sv[0]    = self.pv[0] / 2
        self.cash[0]  = self.sv[0]
        self.pcntl[0] = self.sv[0]
        self.order[0] = 0.0
        self.numTrans = 0
        self.sharesOwned[0] = self.sv[0] / self.closes[0]
        self.numDataPoints  = len(self.closes)
        safeFloat     = self.optParam1
        threshFloat   = self.optParam2

        self.calcAverages()

        if self.bLoopOnParam1:
            maxROI = 0.0
            bestSafe = 0.0
            for outerIndex in range(0, 150):
                self.coreCalculate2(outerIndex / 10.0, threshFloat)
                if self.annualROI > maxROI:
                    maxROI = self.annualROI
                    bestSafe = outerIndex / 10.0
            self.optParam1 = bestSafe
        elif self.bLoopOnParam2:
            maxROI = 0.0
            bestThresh = 0.0
            for outerIndex in range(0, 500, 5):
                self.coreCalculate2(safeFloat, float(outerIndex))
                if self.annualROI > maxROI:
                    maxROI = self.annualROI
                    bestThresh = float(outerIndex)
            self.optParam2 = bestThresh
        else:
            self.coreCalculate2(safeFloat, threshFloat)

        return True

    except BaseException as e:
        print("EXCEPTION OCCURRED IN ALGO2.PY, IN calculate2 FUNCTION - " + str(e))


# Note that this loops through all stock prices in the self.closes list, then
# rounds the floating point values afterwards.
def coreCalculate2(self, safeFloat, threshFloat):
    for index in range(1, len(self.closes)):
        val = self.closes[index]
        self.sv[index] = self.sharesOwned[index-1] * val
        safeVal = self.sv[index] * safeFloat * 0.01
        self.cash[index] = self.cash[index-1] - self.order[index-1]
        self.pv[index] = self.sv[index] + self.cash[index]
        advice = self.pcntl[index-1] - self.sv[index]
        if safeVal > abs(advice):
            self.order[index] = 0.0
        else:
            if advice < 0.0:
                self.order[index] = advice + safeVal
            else:
                self.order[index] = advice - safeVal

        # MODIFICATION #1 - THIS FIRST 'IF' STMT:        
        if self.order[index] > self.cash[index]:     # if buying, and the order is more than the cash we have, change order
            self.order[index] = self.cash[index] / 2.0 # use half the cash instead - new algorithm per drl
        if self.order[index] < threshFloat and self.order[index] > (threshFloat * -1.0):
            self.order[index] = 0.0
        bors = self.order[index] / val    # stands for 'buy or sell'
        if bors != 0.0:
            self.numTrans = self.numTrans + 1
        self.sharesOwned[index] = self.sharesOwned[index-1] + bors
        # MODIFICATION #2 - NEXT STMT:
        self.pcntl[index] = self.pcntl[index-1] + self.order[index] / 2.0 # will alter pcntl on buy OR sell

    self.sv = [round(elem, 2) for elem in self.sv] # round off floating pt values to 2 decimal places
    self.pv = [round(elem, 2) for elem in self.pv]
    self.cash = [round(elem, 2) for elem in self.cash]
    self.order = [round(elem, 2) for elem in self.order]
    self.pcntl = [round(elem, 2) for elem in self.pcntl]
    self.sharesOwned = [round(elem, 1) for elem in self.sharesOwned]
    self.annualROI = self.calcROI(self.startDate, self.endDate)
