#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 17:41:36 2019

@author: larserikskjegstad
"""

import numpy as np

## INSERT DKK to EUR exchange rate
exchange_rate = 0.13436776
## INSERT EUR to USD exchange rate
er_USD = 0.15667511

## INSERT current value (EUR) of Mintos account
value_Mintos = 3603.09

##############################################################################
################################# AKTIESPAREKONTO ############################
##############################################################################

## INSERT current value (DKK) of "Aktiesparekonto" (exclusive ETFs and cash)
value_ASK = exchange_rate*0

## INSERT current value (DKK) of "iShares Core MSCI Emerging Markets IMI UCITS ETF"
EM_aktie = exchange_rate*0

## INSERT current value (DKK) of "iShares Core MSCI Europe IMI UCITS ETF Eur (Acc)"
## in "Aktiesparekonto"
europe_aktie = exchange_rate*0

## INSERT current value (DKK) of "iShares Core MSCI Japan IMI UCITS ETF"
## in "Aktiesparekonto"
japan_aktie = exchange_rate*0

## INSERT current value (DKK) of "iShares S&P 500 UCITS ETF"#
## in "Aktiesparekonto"
SP500_aktie = exchange_rate*134128

## INSERT current value (DKK) of "iShares Core MSCI Pacific ex Japan UCITS ETF" 
## in "Aktiesparekonto"
AP_aktie = exchange_rate*2298


##############################################################################
################################# INET USD ###################################
##############################################################################

## INSERT current value (USD) of the INET USD account
value_USD = er_USD*7815.11


##############################################################################
################################# INETEUR ####################################
##############################################################################

## INSERT current value (EUR) of "iShares Core Global Aggregate Bond UCITS ETF"
value_bond = 13629

## INSERT current value (EUR) of "iShares Core MSCI Emerging Markets IMI UCITS ETF"
EM_ineteur = 5763

## INSERT current value (EUR) of "iShares Core MSCI Europe IMI UCITS ETF Eur (Acc)"
europe_ineteur = 11094

## INSERT current value (EUR) of "iShares Core MSCI Japan IMI UCITS ETF"
japan_ineteur = 4055

## INSERT current value (EUR) of "iShares Core MSCI Pacific ex Japan UCITS ETF"
AP_ineteur = 3104

## INSERT current value (EUR) of "iShares S&P 500 UCITS ETF" in InetEUR
SP500_ineteur = 16147

## INSERT current value (EUR) of "iShares MSCI Canada UCITS ETF"
value_canada = 798

## INSERT current value (EUR) of "iShares-S&P Listed Private ETF" in InetEUR
listed_private = 0



## COLLECT VARIABLES
## Total value of "iShares Core MSCI Japan IMI UCITS ETF"
value_EM = EM_ineteur + EM_aktie

## Total value of "iShares Core MSCI Japan IMI UCITS ETF"
value_japan = japan_ineteur + japan_aktie

## Total value of "iShares S&P 500 UCITS ETF"
value_SP500 = SP500_ineteur + SP500_aktie

## Total value of "iShares Core MSCI Europe IMI UCITS ETF Eur (Acc)"
value_europe = europe_ineteur + europe_aktie

## Total value of "iShares Core MSCI Pacific ex Japan UCITS ETF"
value_AP = AP_ineteur + AP_aktie


## CASH AND FUNDS
## INSERT current amount (EUR) of cash in INETEUR account
cash_ineteur = 6712.98
## INSERT value (DKK) of available investment funds
funds = exchange_rate*0


## PROPERTY (DKK)
value_property = exchange_rate*37383.53


## Total value (EUR) of stock ETFs in INETEUR account
value_stocks_ineteur = (value_japan + value_SP500 + value_canada + value_europe 
                        + value_EM + value_AP + listed_private)

## Total value (EUR) of all instruments after new investment
total = (value_ASK + value_USD + value_bond + value_Mintos + value_stocks_ineteur 
         + cash_ineteur + funds + value_property)


## Total share comprised by private equity
share_PE = 0.03


## Total value after investment comprised by stock ETFs, cash and funds
value_rest = (0.80 - share_PE)*total - value_ASK - value_USD


#A = np.array([[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1],[1,1,1,1,1,1]])

#B = np.array([0.2*total - value_bond, 0.07*value_rest - value_japan, 0.58*value_rest - value_SP500, 0.19*value_rest - value_europe, 0.1*value_rest - value_EM, 0.06*value_rest - value_AP, funds + cash_ineteur])

#C = np.linalg.lstsq(A,B,rcond=None)

#final = C[0]

#print("Invest EUR " + str(final[0]) + " in iShares Core Global Aggregate Bond UCITS ETF")
#print("Invest EUR " + str(final[1]) + " in iShares Core MSCI Japan IMI UCITS ETF")
#print("Invest EUR " + str(final[2]) + " in iShares Core S&P 500 UCITS ETF")
#print("Invest EUR " + str(final[3]) + " in iShares Core MSCI Europe IMI UCITS ETF Eur (Acc)")
#print("Invest EUR " + str(final[4]) + " in iShares Core MSCI Emerging Markets IMI UCITS ETF")
#print("Invest EUR " + str(final[5]) + " in iShares Core MSCI Pacific ex Japan UCITS ETF")



from scipy.optimize import minimize

# b = np.array(
#              [
#               0.55*value_rest - value_SP500,
#               0.06*value_rest - value_AP,
#               0.03*value_rest - value_canada,
#               0.19*value_rest - value_europe, 
#               0.07*value_rest - value_japan, 
#               0.1*value_rest - value_EM,
#               share_PE*total - listed_private,
#               0.05*total - value_bond,
#               0.05*total - value_Mintos,
#               0.1*total - value_property
#              ]
#             )

b = np.array(
              [
              0.58*value_rest - value_SP500,
              0.06*value_rest - value_AP,
              0*value_rest - value_canada,
              0.19*value_rest - value_europe, 
              0.07*value_rest - value_japan, 
              0.1*value_rest - value_EM,
              share_PE*total - listed_private,
              0.0*total - value_bond,
              0*total - value_Mintos,
              0*total - value_property
              ]
            )
n = len(b)

a = np.identity(n)


# Ax = b --> x = [1., -2., 3.]

cons = ({'type': 'eq', 'fun': lambda x: x.sum() - (funds + cash_ineteur)})


fun = lambda x: np.linalg.norm(np.dot(a,x)-b)

xo = np.linalg.solve(a,b)

print(xo, b)
#sol = minimize(fun, xo, method='SLSQP', constraints={'type': 'ineq', 'fun': lambda x:  x}, bounds=[(0.,None) for x in range(n)])

sol = minimize(fun, xo, method='SLSQP', constraints=cons, bounds=[(0.,None) for x in range(n)])
#sol = minimize(fun, np.zeros(n), method='L-BFGS-B', bounds=[(0.,None) for x in range(n)])

x = sol['x'] # [2.79149722e-01, 1.02818379e-15, 1.88222298e+00]

print("Invest: {:.2f} EUR in iShares Core S&P 500 UCITS ETF".format(x[0]))
print("Invest: {:.2f} EUR in iShares Core MSCI Pacific ex Japan UCITS ETF".format(x[1]))
print(f"Invest: {x[2]:.2f} EUR in iShares MSCI Canada UCITS ETF")
print("Invest: {:.2f} EUR in iShares Core MSCI Europe IMI UCITS ETF Eur (Acc)".format(x[3]))
print("Invest: {:.2f} EUR in iShares Core MSCI Japan IMI UCITS ETF".format(x[4]))
print("Invest: {:.2f} EUR in iShares Core MSCI Emerging Markets IMI UCITS ETF".format(x[5]))
print(f"Invest: {x[6]:.2f} EUR in iShares-S&P Listed Private ETF")
print("Invest: {:.2f} EUR in iShares Core Global Aggregate Bond UCITS ETF".format(x[7]))
print(f"Invest: {x[8]:.2f} EUR in Mintos")
print(f"Invest: {x[9]:.2f} EUR in property")

print('Total: {:.2f} EUR'.format(x.sum()))

