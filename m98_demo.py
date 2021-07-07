#!/usr/bin/env python
__author__ = "Aryaman Sharma"

# P98 demo
import numpy as np

nInst=100
currentPos = np.zeros(nInst)

# m2, b2 imported from m98_strat.ipynb
m2 = 8.84381895074547e-05
b2 = 9.47


sl_flag_hit = False
position = False
qty = 0
pprice = 0
sl = 0
sl_active = False
sl_trig_price = 0
normal_run = True

# Dummy algorithm to demonstrate function format.
def getMyPosition (prcSoFar):
    # Stock index 
    STOCK_NO = 55
    global currentPos
    global sl_flag_hit
    global position
    global qty
    global pprice
    global sl
    global m2
    global b2

    (nins,nt) = prcSoFar.shape
    rpos = np.zeros(100)
    # Get p98 stuff
    new_price = prcSoFar[STOCK_NO][-1]
    p = m2*(nt) + b2

    # Buy
    if new_price < 0.995*p:
        if position == False:
            # buy
            qty = ((10000 - (10000%new_price))/new_price)
            print(f"\n===> buy {qty} @ {new_price}\n")
            rpos[STOCK_NO] = qty
            position = True
            pprice = new_price
            sl = (0.9*new_price)
            
    # Sell
    if new_price > p:
        if position:
            rpos[STOCK_NO] = -qty
            print(f"\n===> sell {qty} @ {new_price}\n")
            position = False
            pprice = 0
            qty = 0

    currentPos += rpos

    return currentPos



