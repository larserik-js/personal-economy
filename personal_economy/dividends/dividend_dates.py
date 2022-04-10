"""Dividend dates script.

Classes:
    * GetDividendDates - Gets the information by scraping a webpage,
      and processes it into a table.
"""
from datetime import datetime, date
from threading import Thread
import logging
import sys

import pandas as pd
import numpy as np


class GetDividendDates:

    def __init__(self):
        # The keys are the company names
        # The values are the unique part of the URL of the dividend webpage
        self.company_urls = np.loadtxt('input/company_urls.txt', dtype=str, 
                                       delimiter=',')

        # The list of data frames for the companies
        self.df_list = []

        # The table containing the information to be presented
        self.next_dividends = self._make_table()

    # Returns the entire url given a unique string
    def _get_url(self, unique_string):
        initial_string = 'https://www.dividendmax.com/united-states/nyse/'
        final_string = '/dividends'
        return initial_string + unique_string + final_string

    def _transform_df(self, df, company_name):
        # Get last paid dividend amount
        last_dividend = df.loc[df['Status'] == 'Paid']['Decl. amount'].iloc[0]
        
        n_rows = len(df.index)

        # Add a column with the company name
        df['Company name'] = pd.Series([company_name for _ in range(n_rows)])
        # Add a column with the forecast amount
        df['Forecast amount'] = pd.Series([last_dividend for _ in range(n_rows)])
        
        # Specify the relevant column names
        cols = ['Company name', 'Status', 'Ex-div date', 'Pay date',
                'Forecast amount']
        df_transformed = df[cols]
        # Only use data for declared or forecast payments
        # This (among possible others) excludes the 'paid' payments
        condition = (
            (df_transformed['Status'] == 'Forecast') 
            | (df_transformed['Status'] == 'Declared')
        )
        df_transformed = df_transformed.loc[condition]
        
        # Drop the Status column
        df_transformed = df_transformed.drop('Status', axis=1)
        
        return df_transformed

    def _get_df(self, company_name, url):
        try:
            logging.info("Requested..." + url)
            df = pd.read_html(io=url, match='Currency')[0]
        except:
            logging.error(f'Error with check for {url}!')
        else:
            self.df_list.append([df, company_name])

    # Returns all dfs concatenated, using threading
    def _concatenate_dfs(self):
        # The total number of companies
        n_companies = len(self.company_urls)

        threads = [None] * n_companies
        
        # Iterate over companies
        for i in range(n_companies):
            company_name = self.company_urls[i,0]
            unique_string = self.company_urls[i,1]
            # The full, unique company URL
            url = self._get_url(unique_string)
            
            threads[i] = Thread(target=self._get_df, args=(company_name, url))
            threads[i].start()        

        for i in range(n_companies):
            threads[i].join()
        
        # Number of dataframes retrieved
        n_dfs = len(self.df_list)

        retrieved_dfs = [self.df_list[i][0] for i in range(n_dfs)]
        retrieved_companies = [self.df_list[i][1] for i in range(n_dfs)]
        
        for i in range(n_dfs):
            # Get transformed df
            retrieved_dfs[i] = self._transform_df(retrieved_dfs[i], 
                                                  retrieved_companies[i])
            
        # Concatenate all dfs
        if retrieved_dfs:
            df_concatenated = pd.concat(retrieved_dfs, ignore_index=True)
        else:
            print('No information could be scraped. Exiting program.')
            sys.exit()

        return df_concatenated

    def _sort_and_select_next(self, df_concatenated, number):
        # Convert dates to datetime
        df_concatenated['Ex-div date'] = pd.to_datetime(
            df_concatenated['Ex-div date']
        )
        df_concatenated['Pay date'] = pd.to_datetime(df_concatenated['Pay date'])
        
        # Drop ex-div dates from before today
        date_today = datetime.combine(date.today(), datetime.min.time())
        condition = (df_concatenated['Ex-div date'] >= date_today)    
        df_concatenated = df_concatenated.loc[condition]
        
        # Sort rows by ex dividend dates
        df_concatenated = df_concatenated.sort_values(by=['Ex-div date'])
        
        # Format dates
        df_concatenated['Ex-div date'] = df_concatenated['Ex-div date'] \
            .dt.strftime('%d %b %Y')
        df_concatenated['Pay date'] = df_concatenated['Pay date'] \
            .dt.strftime('%d %b %Y')
        
        return df_concatenated.head(number)

    def _format_cents_to_dollars(self, df):
        for i in range(len(df)):
            cent_string = df['Forecast amount'].iloc[i]
            # Amount in cents (float dtype)
            cent_amount = float(cent_string[:-1])
            # Format to dollars
            dollar_amount = 0.01 * cent_amount
            df['Forecast amount'].iloc[i] = f'${dollar_amount:.2f}'
            
        return df

    def _make_table(self):
        # Concatenate all dfs
        df_concatenated = self._concatenate_dfs()
        
        # Sort by date and select display the next 10 payments (by ex-div date)
        next_dividends = self._sort_and_select_next(df_concatenated, 10)
        
        # Format dividend values from cents to dollars
        next_dividends = self._format_cents_to_dollars(next_dividends)

        return next_dividends

    def show_table(self):
        print(self.next_dividends)