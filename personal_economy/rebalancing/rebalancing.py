"""Portfolio rebalancing main script.

This is where all information is gathered, processed, and presented to the user.

Classes:
    * CalculateInvestments - inherits all inputs from the _Input class.
      Calculates and presents the suggestions for investments to the user.
"""
import sys

import numpy as np
import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt

from personal_economy.rebalancing import gui
from personal_economy.rebalancing import scraper
from personal_economy.rebalancing.diversification import (
    RISK_CATEGORIES, get_diversification_dicts)


class _Input:

    def __init__(self):
        # Dictionary of exchange rates
        self.ER_dict, self.ER_date = scraper.scrape_ERs()

        # Get person and amount to invest from input
        self.person, self.amount, self.currency = gui.get_input()

        # Convert currency to invest to DKK
        self.amount_DKK = self.ER_dict[self.currency] * self.amount

        # Diversification dictionaries
        self.diversification_dict, self.region_diversification_dict \
            = get_diversification_dicts(self.person)


class CalculateInvestments(_Input):

    def __init__(self):
        super().__init__()
        # Create the data frame and get relevant risk categories
        self.df, self.categories = self._get_df()

        # Total portfolio value
        self.total_value = self._get_total_value()

        self.current_distribution_dict = self._get_current_distribution()

        self.desired_distribution_dict = self._generate_desired_distribution()

        self.distribution_difference = self._get_distribution_difference()

        self.investments_dict = self._get_investments()

        # Regional diversification of stock ETFs
        self.stock_ETF_investments_dict = self._get_stock_ETF_investments()

        # Visualize
        self._plot_distributions()

        # Print information
        self._print_information()

    def _get_df(self):
        df = pd.read_excel('input/' + self.person + '.xlsx', header=14)
        
        # Instrument categories
        df_categories = df.Category.unique()

        if np.any([risk_category not in RISK_CATEGORIES 
                   for risk_category in df_categories]):
            print('Incorrect risk category in input .xlsx document.')
            sys.exit()

        return df, df_categories

    # Takes an array of currency name strings, and returns an array
    # with exchange rate values
    def _get_ERs(self, ER_strings):
        # Convert strings to ER values
        ER_values = np.array([self.ER_dict[ER] for ER in ER_strings])
        return ER_values

    def _get_total_value(self):
        all_amounts = self.df['Amount'].to_numpy()
        all_ERs = self._get_ERs(self.df['Currency'].to_numpy())
        total_value = (all_amounts * all_ERs).sum()

        return total_value

    # Displays current portfolio distribution
    def _get_current_distribution(self):
        current_distribution_dict = {}

        for category, fraction in self.diversification_dict.items():
            if category in self.categories:
                amounts = self.df.Amount.loc[
                    (self.df.Category == category)
                ].to_numpy()

                # Array of strings
                ERs = self.df.Currency.loc[
                    (self.df.Category == category)
                ].to_numpy()

                # Array of exchange rate values
                ERs = self._get_ERs(ERs)
                
                # Total value
                current_distribution_dict[category] = (amounts * ERs).sum()
            else:
                current_distribution_dict[category] = 0

        return current_distribution_dict

    def _get_distribution_difference(self):
        current_distribution = np.array(
            [value for value in self.current_distribution_dict.values()]
        )

        desired_distribution = np.array(
            [value * (self.total_value + self.amount_DKK) 
                for value in self.diversification_dict.values()]
        )

        return desired_distribution - current_distribution

    # Returns a vector with desired final amounts for each category
    def _generate_desired_distribution(self):
        desired_distribution_dict = {}
                        
        for category, fraction in self.diversification_dict.items():
            desired_distribution_dict[category] = (
                fraction * (self.total_value + self.amount_DKK)
            )
        
        return desired_distribution_dict

    def _solve_for_amounts(self, distribution_difference, available_amount):
        # The function to minimize
        # Global minimum = 0
        # x is the distribution of new investments
        function = lambda x: np.linalg.norm(x - distribution_difference)
        
        # The total amount of new investments should equal the available amount
        constraints = {'type': 'eq', 
                       'fun': lambda x: x.sum() - available_amount}

        # Solve
        sol = optimize.minimize(
            function, distribution_difference, method='SLSQP', 
            constraints=constraints, 
            bounds=[(0.,None) for _ in range(len(distribution_difference))]
        )

        return sol['x']

    def _get_investments(self):
        # # An array of the investments
        investments = self._solve_for_amounts(self.distribution_difference,
                                              self.amount_DKK)

        # The dictionary of investments
        investments_dict = {}
        for i in range(len(self.diversification_dict.keys())):
            investments_dict[
                list(self.diversification_dict.keys())[i]
            ] = investments[i]
        
        return investments_dict

    def _get_stock_ETF_investments(self):

        current_distribution = []
        diversification_fractions = []
        
        for ETF_name, fraction in self.region_diversification_dict.items():
            ER = self.df.Currency.loc[(self.df.Name == ETF_name)].to_numpy()[0]
            current_distribution.append(
                (self.df.Amount.loc[(self.df.Name == ETF_name)].to_numpy()[0]
                    * self.ER_dict[ER])
            )
            diversification_fractions.append(fraction)

        # Convert to Numpy array
        current_distribution = np.array(current_distribution)
        diversification_fractions = np.array(diversification_fractions)

        # Get desired distribution
        total_new_investments = self.investments_dict['Stocks_ETF']
        desired_distribution = (
            current_distribution.sum() + total_new_investments
        ) * diversification_fractions
        distribution_difference = (desired_distribution - current_distribution)
        
        # investments = sol['x']
        investments = self._solve_for_amounts(distribution_difference,
                                              total_new_investments)

        # The investment dictionary
        stock_ETF_dict = {}
        for i in range(len(self.region_diversification_dict)):
            stock_ETF_dict[
                list(self.region_diversification_dict.keys())[i]
            ] = investments[i]
            
        return stock_ETF_dict

    def _plot_distributions(self):
        fig, ax = plt.subplots(figsize=(10,6))
        
        # Portfolio
        ax.bar(self.current_distribution_dict.keys(),
               self.current_distribution_dict.values(), 
               alpha=1, label='Current distribution')
        ax.bar(self.desired_distribution_dict.keys(),
               self.desired_distribution_dict.values(), 
               alpha=0.5, label='Desired distribution')
        
        plt.xticks(rotation=20)
        ax.set_title('Current vs. desired distributions', size=20)
        ax.set_ylabel('DKK', size=14)

        ax.legend(loc='best')
        fig.tight_layout()
        
        plt.show()

    def _print_information(self):
        print('')
        print('###############################################################')
        print(f'############## Rebalancing for {self.person}  ################')
        print('###############################################################')
        print('')
        print(f'Exchange rates (date: {self.ER_date}):')
        
        for key, value in self.ER_dict.items():
            print(f'{key}: {value:.4f}')
        print('')
        
        print('############### CURRENT PORTFOLIO #############################')
        print('')
        
        for category, value in self.current_distribution_dict.items():
            print(f'{category:30s}'
                  + f'{100*value/self.total_value:8.2f}% ({value:.2f} DKK)')
            
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
            print(f'Invest: {amount / self.ER_dict["EUR"]:.2f} EUR '
                  + f'in {ETF_name}')

        print(f'Total: {value_DKK_sum / self.ER_dict["EUR"]:.2f} EUR '
              + f'= {value_DKK_sum:.2f} DKK')
        print('')