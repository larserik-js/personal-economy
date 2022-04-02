#from locale import currency
import numpy as np
import pandas as pd
from scipy import optimize
import matplotlib.pyplot as plt
import sys

import gui
from diversification import get_diversification_dicts
import scraper

class GetInput:
    # Dictionary of exchange rates
    ER_dict, ER_date = scraper.scrape_ERs()

    # Get person and amount to invest from input
    person, amount, currency = gui.get_input()
        
    # Convert currency to invest to DKK
    amount_DKK = ER_dict[currency] * amount

    # Diversification dictionaries
    diversification_dict, region_diversification_dict = get_diversification_dicts(person)
       

class CalculateInvestments(GetInput):
    def __init__(self):

        # Create the data frame 
        self.df = pd.read_excel('../../input/' + self.person + '.xlsx',
                             header=14)
                
        # Instrument categories
        self.categories = self.df.Category.unique()
        # Number of categories
        self.n_categories = len(self.categories)
        
        # Checks if the number of categories in the .csv file is not higher than in the script
        if self.n_categories > len(self.diversification_dict):
            raise AssertionError('No. of instrument categories in .csv file'\
                                  + ' larger than in Python script.')

        # Total portfolio value
        all_amounts = self.df['Amount'].to_numpy()
        all_ERs = self.get_ERs(self.df['Currency'].to_numpy())
        self.total_value = (all_amounts * all_ERs).sum()


        self.current_distribution_dict = self.get_current_distribution()
        self.current_distribution = np.array([value for value in self.current_distribution_dict.values()])

        self.desired_distribution_dict = self.generate_desired_distribution()
        
        self.desired_distribution = np.array([value * (self.total_value + self.amount_DKK) 
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
            desired_distribution_dict[category] = fraction * (self.total_value + self.amount_DKK) 
        
        return desired_distribution_dict

    def find_investments(self):
        # The function to minimize
        # Global minimum = 0
        # x is the distribution of new investments
        function = lambda x: np.linalg.norm(x - self.distribution_difference)
        
        # The total amount of new investments should equal the available amount
        constraints = {'type': 'eq', 'fun': lambda x: x.sum() - self.amount_DKK}

        # Solve
        sol = optimize.minimize(function, self.distribution_difference, method='SLSQP', 
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
        sol = optimize.minimize(function, distribution_difference, method='SLSQP', 
                       constraints=constraints,
                       bounds=[(0.,None) for _ in range(len(distribution_difference))])
        
        investments = sol['x']

        # The investment dictionary
        stock_ETF_dict = {}
        for i in range(len(self.region_diversification_dict)):
            stock_ETF_dict[list(self.region_diversification_dict.keys())[i]] = investments[i]
            
        return stock_ETF_dict


class Visualize(CalculateInvestments):

    def __init__(self):
        print('At Visualize')

        super().__init__()

        self.plot_distributions()

        self.print_information()

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


if __name__ == '__main__':
    GetInput()

    CalculateInvestments()

    Visualize()
