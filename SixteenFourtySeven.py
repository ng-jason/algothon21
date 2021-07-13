#!/usr/bin/env python
import numpy as np
from numpy.polynomial.polynomial import polyfit
import math

nInst=100
currentPos = np.zeros(nInst)

def getMyPosition (prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape 
    rpos = np.zeros(100)
    convergence_values = get_convergence_values(prcSoFar)   
    for i in range(0, nins):
        cnvg = convergence_values[i]
        new_price = prcSoFar[i][-1]
        if new_price < cnvg:
            if currentPos[i] == 0: 
                qty = ((10000 - (10000 % new_price)) / new_price)
                qty = math.floor(qty)
                rpos[i] = qty
            if currentPos[i] < 0:
                qty = currentPos[i]
                qty = math.floor(qty)
                rpos[i] = rpos[i] - qty 
        if new_price > cnvg:
            if currentPos[i] > 0:
                qty = currentPos[i]
                qty = math.floor(qty)
                qty_sll = ((10000 - (10000 % new_price)) / new_price)
                qty_sll = math.floor(qty_sll)
                rpos[i] = -qty_sll - qty
    currentPos += rpos
    return currentPos

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
            tmp_convergence_values.append(pred)
        cnvg = 0
        for val in tmp_convergence_values:
            cnvg += val
        cnvg = cnvg/len(tmp_convergence_values)
        convergence_values.append(cnvg)
    return convergence_values   