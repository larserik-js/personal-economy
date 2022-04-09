"""Contains specific information on the risk allocation of the different
portfolios.

Variables:
    * RISK_CATEGORIES - a list of all the possible risk categories defined in
      the package.
Functions:
    * get_diversification_dicts - return the specific risk allocation for a
      given input person name.
"""
import sys

import numpy as np


RISK_CATEGORIES = [# High risk
                   'Stocks_ETF',
                   'Dividend_stocks_high',
                   'Private_equity',
                   'Alternative',
                   # Medium risk
                   'Dividend_stocks_medium',
                   'Property',
                   # Low risk
                   'Dividend_stocks_low',
                   'Bonds']

def _values_sum_to_one(diversification_dict):
    diversification_array = np.array(
        [value for value in diversification_dict.values()]
    )

    if diversification_array.sum() == 1:
        return True
    else:
        return False

def get_diversification_dicts(person):

    # Person diversification dictionaries
    if person == 'Person1':
        person_diversification_dict = {# High risk
                                       'Stocks_ETF': 0.66,
                                       'Dividend_stocks_high': 0.03,
                                       'Private_equity': 0.02,
                                       'Alternative': 0.01,
                                       # Medium risk
                                       'Dividend_stocks_medium': 0.10,
                                       'Property': 0.10,
                                       # Low risk
                                       'Dividend_stocks_low': 0.08,
                                       'Bonds': 0.0}

    elif person == 'Person2':
        person_diversification_dict = {# High risk
                                       'Stocks_ETF': 0.67,
                                       'Dividend_stocks_high': 0.0,
                                       'Private_equity': 0.03,
                                       'Alternative': 0.00,
                                       # Medium risk
                                       'Dividend_stocks_medium': 0.10,
                                       'Property': 0.05,
                                       # Low risk
                                       'Dividend_stocks_low': 0.05,
                                       'Bonds': 0.1}
    else:
        print('Got wrong person name in "diversification.py".')
        sys.exit()

    # Stock ETF regional diversification
    regional_diversification_dict = {
        'iShares Core MSCI Emerging Markets IMI UCITS ETF': 0.1,
        'iShares Core MSCI Europe UCITS ETF EUR (Acc)': 0.19,
        'iShares Core MSCI Japan IMI UCITS ETF': 0.07,
        'iShares Core MSCI Pacific ex Japan UCITS ETF': 0.06,
        'iShares Core S&P 500 UCITS ETF': 0.56,
        'iShares MSCI Canada UCITS ETF': 0.02
    }

    # Checks if the diversification values sum to 1        
    if not _values_sum_to_one(person_diversification_dict):
        print('Diversification values do not add up to 100%')
        sys.exit()

     # Checks if regional diversification sums to 100%
    if not _values_sum_to_one(regional_diversification_dict):
        print('Regional diversification does not sum to 100%.')
        sys.exit()

    return person_diversification_dict, regional_diversification_dict