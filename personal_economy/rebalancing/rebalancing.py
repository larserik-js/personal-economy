#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 19:25:23 2021

@author: larserikskjegstad
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import pandas as pd
import sys
from datetime import date, timedelta
import os
import sys

path = os.path.dirname(os.path.realpath(__file__)) + '/'
sys.path.append(path)

class Rebalancing:
    def __init__(self, path):
        # Get today's date from input
        #self.today = input("Enter today's date (DD-MM-YYYY): ")

        # Dictionary of exchange rates
        self.ER_dict, self.ER_date = self.scrape_ERs()

        # Get person from input
        self.person = input("Enter person name ('Anna' or 'LE'): ")
        if self.person != 'LE' and self.person != 'Anna':
            print('Person entered is neither Anna nor LE.')
            sys.exit()

        # Get amount to invest from input
        amount_and_currency = input('Enter amount to invest followed by currency (e.g. 1000 EUR): ')
        string_list = amount_and_currency.split(' ')

        # Checks if the value entered can be converted to float
        try:
            float(string_list[0])
        except ValueError:
            print('Amount entered is not a valid value.')
            sys.exit()
            
        # Get the amount to invest from input
        amount_to_invest = float(string_list[0])

        # Checks if the currency entered is supported
        if string_list[1] not in [currency_name for currency_name in self.ER_dict.keys()]:
            print('Currency not supported.')
            sys.exit()
            
        currency_to_invest = string_list[1]

        # Convert currency to invest to DKK
        self.amount_to_invest = self.ER_dict[currency_to_invest] * amount_to_invest

        # Create the data frame    
        self.df = pd.read_excel(path + 'portfolio_' + self.person + '.xlsx',
                             header=14)

        print(self.df)
        
        # Instrument categories
        self.categories = self.df.Category.unique()
        # Number of categories
        self.n_categories = len(self.categories)
        
        # Total portfolio value
        all_amounts = self.df['Amount'].to_numpy()
        all_ERs = self.get_ERs(self.df['Currency'].to_numpy())
        self.total_value = (all_amounts * all_ERs).sum()
        

        # Portfolio diversification
        
        if self.person == 'LE':
            self.diversification_dict = {
                                         # High risk
                                         'Stocks_ETF': 0.66,
                                         'Dividend_stocks_high': 0.03,
                                         'Private_equity': 0.02,
                                         'Alternative': 0.01,
                                         # Medium risk
                                         'Dividend_stocks_medium': 0.10,
                                         'Property': 0.10,
                                         # Low risk
                                         'Dividend_stocks_low': 0.08,
                                         'Bonds': 0.0
                                         }
    
        elif self.person == 'Anna':
        
            self.diversification_dict = {
                                         # High risk
                                         'Stocks_ETF': 0.67,
                                         'Dividend_stocks_high': 0.0,
                                         'Private_equity': 0.03,
                                         'Alternative': 0.00,
                                         # Medium risk
                                         'Dividend_stocks_medium': 0.10,
                                         'Property': 0.05,
                                         # Low risk
                                         'Dividend_stocks_low': 0.05,
                                         'Bonds': 0.1
                                         }
    
        else:
            raise AssertionError('Person entered is neither Anna nor LE.')
        
        # Stock ETF regional diversification
        self.region_diversification_dict = {'iShares Core MSCI Emerging Markets IMI UCITS ETF': 0.1,
                                            'iShares Core MSCI Europe UCITS ETF EUR (Acc)': 0.19,
                                            'iShares Core MSCI Japan IMI UCITS ETF': 0.07,
                                            'iShares Core MSCI Pacific ex Japan UCITS ETF': 0.06,
                                            'iShares Core S&P 500 UCITS ETF': 0.56,
                                            'iShares MSCI Canada UCITS ETF': 0.02}
    
        # Checks if regional diversification sums to 100%
        if np.array([value for value in self.region_diversification_dict.values()]).sum() != 1:
            raise AssertionError('Region diversification does not sum to 100%.')
    
        # Checks if the diversification values sum to 1        
        values = np.array([value for _, value in self.diversification_dict.items()])
    
        if values.sum() != 1:
            raise AssertionError('Diversification values do not add up to 100%')
            
        
        # Checks if the number of categories in the .csv file is not higher than in the script
        if self.n_categories > len(self.diversification_dict):
            raise AssertionError('No. of instrument categories in .csv file'\
                                  + ' larger than in Python script.')
         
                    
        self.current_distribution_dict = self.get_current_distribution()
        self.current_distribution = np.array([value for value in self.current_distribution_dict.values()])

        
        self.desired_distribution_dict = self.generate_desired_distribution()
        
        self.desired_distribution = np.array([value * (self.total_value + self.amount_to_invest) 
                                for value in self.diversification_dict.values()])

        self.distribution_difference = self.desired_distribution - self.current_distribution

        
        # An array of the investments
        self.investments = self.find_investments()

        # The dictionary of investments
        self.investments_dict = {}
        for i in range(len(self.diversification_dict.keys())):
            self.investments_dict[list(self.diversification_dict.keys())[i]] = self.investments[i]

        # Regional diversification of stock ETFs
        self.stock_ETF_investments_dict = self.find_stock_ETF_investments()
        
    # Get today's exchange rates
    def scrape_ERs(self):
        # URL for currency exchange rates
        url = 'https://www.nationalbanken.dk/valutakurser'
    
        ER_df = pd.read_html(url)[0]

        headers = ER_df.columns.values

        # Today's date
        today = date.today()

        # Try to get exchange rates from the last 10 days
        for i in range(10):
            ER_date = today - timedelta(days=i)
            ER_date = ER_date.strftime("%d-%m-%Y")            
            if ER_date in headers:
                # Define exchange rates
                ER_NOK_to_DKK = 0.0001 * (ER_df[ER_date].loc[(ER_df.ISO == 'NOK')]).to_numpy()[0]
                ER_EUR_to_DKK = 0.0001 * (ER_df[ER_date].loc[(ER_df.ISO == 'EUR')]).to_numpy()[0]
                ER_USD_to_DKK = 0.0001 * (ER_df[ER_date].loc[(ER_df.ISO == 'USD')]).to_numpy()[0]
                break

        # If exchange rates cannot be found online, input own values
        if ER_date not in headers:
            print("Online exchange rates not found.")
            ER_NOK_to_DKK = float(input("Enter the value of 1 NOK in DKK (e.g. 0.75): "))
            ER_EUR_to_DKK = float(input("Enter the value of 1 EUR in DKK (e.g. 7.5): "))
            ER_USD_to_DKK = float(input("Enter the value of 1 USD in DKK (e.g. 6.5): "))
        
        # Dictionary containing the currency names strings as keys,
        # and the (current) respective exchange rates as values
        ER_dict = {'DKK': 1, 'NOK': ER_NOK_to_DKK, 'EUR': ER_EUR_to_DKK,
                       'USD': ER_USD_to_DKK}

        return ER_dict, ER_date
    
    # Takes an array of currency name strings, and returns an array
    # with exchange rate values
    def get_ERs(self, ER_strings):
        # Convert strings to ER values
        ER_values = np.array([self.ER_dict[ER] for ER in ER_strings])
        return ER_values
        
    # Displays current portfolio distribution
    def get_current_distribution(self):
        current_distribution_dict = {}

        for category, fraction in self.diversification_dict.items():
            if category in self.categories:
                amounts = (self.df.Amount.loc[(self.df.Category == category)]).to_numpy()
                # Array of strings
                ERs = self.df.Currency.loc[(self.df.Category == category)].to_numpy()
                # Array of exchange rate values
                ERs = self.get_ERs(ERs)
                
                # Total value
                current_distribution_dict[category] = (amounts * ERs).sum()
            else:
                current_distribution_dict[category] = 0

        return current_distribution_dict
        
    # Returns a vector with desired final amounts for each category
    def generate_desired_distribution(self):
        desired_distribution_dict = {}
                        
        for category, fraction in self.diversification_dict.items():
            desired_distribution_dict[category] = fraction * (self.total_value + self.amount_to_invest) 
        
        return desired_distribution_dict
    
    def find_investments(self):
        # The function to minimize
        # Global minimum = 0
        # x is the distribution of new investments
        function = lambda x: np.linalg.norm(x - self.distribution_difference)
        
        # The total amount of new investments should equal the available amount
        constraints = {'type': 'eq', 'fun': lambda x: x.sum() - self.amount_to_invest}

        # Solve
        sol = minimize(function, self.distribution_difference, method='SLSQP', 
                       constraints=constraints,
                       bounds=[(0.,None) for _ in range(len(self.distribution_difference))])
        
        investments = sol['x']
        
        return investments

    def find_stock_ETF_investments(self):

        current_distribution = []
        diversification_fractions = []
        
        for ETF_name, fraction in self.region_diversification_dict.items():
            ER = self.df.Currency.loc[(self.df.Name == ETF_name)].to_numpy()[0]
            current_distribution.append(self.df.Amount.loc[(self.df.Name == ETF_name)].to_numpy()[0] * self.ER_dict[ER])
            diversification_fractions.append(fraction)

        # Convert to Numpy array
        current_distribution = np.array(current_distribution)
        diversification_fractions = np.array(diversification_fractions)

        # Get desired distribution
        total_new_investments = self.investments_dict['Stocks_ETF']
        desired_distribution = (current_distribution.sum() + total_new_investments) * diversification_fractions
        distribution_difference = (desired_distribution - current_distribution)
        
        # The function to minimize
        # Global minimum = 0
        # x is the distribution of new investments
        function = lambda x: np.linalg.norm(x - distribution_difference)
        
        # The total amount of new investments should equal the available amount
        constraints = {'type': 'eq', 'fun': lambda x: x.sum() - total_new_investments}

        # Solve
        sol = minimize(function, distribution_difference, method='SLSQP', 
                       constraints=constraints,
                       bounds=[(0.,None) for _ in range(len(distribution_difference))])
        
        investments = sol['x']

        # The investment dictionary
        stock_ETF_dict = {}
        for i in range(len(self.region_diversification_dict)):
            stock_ETF_dict[list(self.region_diversification_dict.keys())[i]] = investments[i]
            
        return stock_ETF_dict


    def plot_distributions(self):
        fig, ax = plt.subplots(figsize=(10,6))
        
        # Portfolio
        ax.bar(self.current_distribution_dict.keys(), self.current_distribution_dict.values(), 
               alpha=1, label='Current distribution')
        ax.bar(self.desired_distribution_dict.keys(), self.desired_distribution_dict.values(), 
               alpha=0.5, label='Desired distribution')
        
        plt.xticks(rotation=20)
        ax.set_title('Current vs. desired distributions', size=20)
        ax.set_ylabel('DKK', size=14)

        
        ax.legend(loc='best')
        fig.tight_layout()
        
        plt.show()


    def print_information(self):
        print('')
        print('###############################################################')
        print(f'############## Rebalancing for {self.person}  ############################')
        print('###############################################################')
        print('')
        print(f'Exchange rates (date: {self.ER_date}):')
        
        for key, value in self.ER_dict.items():
            print(f'{key}: {value:.4f}')
        print('')
        
        print('############### CURRENT PORTFOLIO #############################')
        print('')
        
        for category, value in self.current_distribution_dict.items():
            print(f'{category:30s}' + f'{100*value/self.total_value:8.2f}% ({value:.2f} DKK)')
            
        print('')
        print(f'Total current portfolio value: {self.total_value:.2f} DKK')
        print('')
        print('###############################################################')
        print('###############################################################')
        print('')

        print('############### NEW INVESTMENTS ###############################')
        print('')
        
        # Print amounts to invest for each portfolio part
        value_DKK_sum = 0
        for category, value in self.investments_dict.items():
            value_DKK_sum += value
            print(f'Invest: {value:.2f} DKK in {category}')

        print(f'Total: {value_DKK_sum:.2f} DKK')
        print('')
        
        # The total amount to invest in stock ETFs
        stock_ETF_investments = self.investments_dict['Stocks_ETF']
        
        # Stocks
        print('Stock ETFs:')
        value_DKK_sum = 0
        for ETF_name, amount in self.stock_ETF_investments_dict.items():
            value_DKK_sum += amount
            print(f'Invest: {amount / self.ER_dict["EUR"]:.2f} EUR in {ETF_name}')

        print(f'Total: {value_DKK_sum / self.ER_dict["EUR"]:.2f} EUR = {value_DKK_sum:.2f} DKK')
        print('')
            
# The simulation
def run(path):
    
    # Create rebalancing object
    rebalancing_obj = Rebalancing(path)
    
    # Print investments
    rebalancing_obj.print_information()

    # Plot distributions
    rebalancing_obj.plot_distributions()
    
# Runs the simulation
run(path)

