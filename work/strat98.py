#!/usr/bin/env python
__author__ = "aryaman"

import numpy as np
from numpy.polynomial.polynomial import polyfit
import math

nInst=100
currentPos = np.zeros(nInst)
stop_loss_value = np.zeros(nInst) # for normal buy-sell
trailing_profit = np.zeros(nInst) # can be substituted by trailing sl

def getMyPosition (prcSoFar):
    global currentPos
    global stop_loss_values
    global trailing_profit
    (nins,nt) = prcSoFar.shape #(100, prices
    rpos = np.zeros(100)

    # Get convergence values
    convergence_values = get_convergence_values(prcSoFar)   
    #print(f"\n {convergence_values} \n")
    for i in range(0, nins):
        #if i != 98:
        #    continue
        cnvg = convergence_values[i]
        new_price = prcSoFar[i][-1]
        if new_price < 0.995*cnvg:
            if currentPos[i] == 0: # no current pos in stock
                qty = ((10000 - (10000 % new_price)) / new_price)
                qty = math.floor(qty)
                #print(f"==> Simple buy {i} :: {qty}@{new_price} :: transaction value: {qty*new_price}")
                rpos[i] = qty
            if currentPos[i] < 0:
                # buy all short sells
                qty = currentPos[i]
                qty = math.floor(qty)
                #print(f"==> Settle short position {i} :: {qty}@{new_price} :: transaction value: {qty*new_price}")
                rpos[i] = rpos[i] - qty # qty is negative
        
        if new_price > cnvg:
            if currentPos[i] > 0:
                qty = currentPos[i]
                qty = math.floor(qty)
                #print(f"==> Simple sell {i} :: {qty}@{new_price} :: transaction value: {qty*new_price}")
                # short sell here
                qty_sll = ((10000 - (10000 % new_price)) / new_price)
                qty_sll = math.floor(qty_sll)
                #print(f"==> short sell {i} :: {qty_sll}@{new_price} :: transaction value: {qty_sll*new_price}")
                rpos[i] = -qty_sll - qty
        '''
        # Why does trailing profit perform worse ????? WTF?
        # Trailing profit implementation cant really figure out why it performs worse than simple sell
        if new_price > cnvg:
            if trailing_profit[i] < new_price:
                trailing_profit[i] = new_price
            elif trailing_profit[i] >= new_price:
                if currentPos[i] > 0:
                    qty = currentPos[i]
                    qty = math.floor(qty)
                    print(f"==> Simple sell {i} :: {qty}@{new_price} :: transaction value: {qty*new_price}")
                    #rpos[i] = -qty
                    # short sell here
                    qty_sll = ((10000 - (10000 % new_price)) / new_price)
                    qty_sll = math.floor(qty_sll)
                    print(f"==> short sell {i} :: {qty_sll}@{new_price} :: transaction value: {qty_sll*new_price}")
                    rpos[i] = -qty_sll - qty
                    trailing_profit[i] = 0
        '''
    currentPos += rpos
    
    return currentPos

"""
TODO: Find best number of sequences and sequence length

Get convergence values for all stocks

Returns: List of 100 convergence values
"""
def get_convergence_values(prcSoFar):
    SEQUENCE_LENGTH = 30
    SEQUENCES = 50
    convergence_values = []
    (nins, nt) = prcSoFar.shape
    for stock in prcSoFar:
        values = stock[-50:]
        tmp_convergence_values = []
        sequences = []
        for i in range(0, SEQUENCES):
            seq_tmp = []
            for j in range(0, SEQUENCE_LENGTH):
                seq_tmp.append(values[np.random.randint(0, len(values))])
            sequences.append(seq_tmp) 
        x_values = []
        for k in range(1, SEQUENCE_LENGTH+1):
            x_values.append(k)
        for seq in sequences:
            x = np.array(x_values)
            y = np.array(seq)
            
            m, b = polyfit(x, y, 1)
            pred = 69 * b + m
            ''' Why does second degree polynomial perform worse ??????
            a, b, c = polyfit(x, y, 2) # try second degree regression
            pred = a + b * 69 + c * 69 * 69
            '''
            tmp_convergence_values.append(pred)
        cnvg = 0
        for val in tmp_convergence_values:
            cnvg += val
        cnvg = cnvg/len(tmp_convergence_values)
        convergence_values.append(cnvg)
    return convergence_values   