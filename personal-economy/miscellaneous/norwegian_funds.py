# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np

## Current value of "DNB Aktiv 30"
value_DA30 = 25744.

## Current value of "DNB Emerging Markets Indeks A"
value_DEMIA = 5930.

## Current value of "DNB Global Indeks"
value_DGI = 53148.

## Current value of "DNB Norge Indeks"
value_DNI = 5735.

## INSERT value of available investment funds
funds = 25000.

## Total value of all instruments after new investment
total = value_DA30 + value_DEMIA + value_DGI + value_DNI + funds




A = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,1,1,1]])

B = np.array([0.285714*total - value_DA30, (1-0.285714)*0.10*total - value_DEMIA, (1-0.285714)*0.80*total - value_DGI, (1-0.285714)*0.10*total - value_DNI, funds])

C = np.linalg.lstsq(A,B,rcond=None)
print(C)
