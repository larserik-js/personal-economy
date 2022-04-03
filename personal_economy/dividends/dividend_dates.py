from datetime import datetime, date
from timeit import default_timer as DT
from threading import Thread
import logging

import pandas as pd
import numpy as np


t_init = DT()

# The keys are the company names
# The values are the unique part of the URL of the dividend webpage
company_urls = np.array(
    [['Altria Group Inc.', 'tobacco/altria-group-inc'],
    ['IBM Corp.', 'electronic-and-electrical-equipment/international-business-machines-corp'],
    ['Johnson & Johnson', 'pharmaceuticals-and-biotechnology/johnson-and-johnson'],
    ['Procter & Gamble Co.', 'household-goods/procter-and-gamble-co'],
    ['Realty Income Corp.', 'real-estate-investment-trusts/realty-income-corp'],
    ['Verizon Communications Inc.', 'telecomms/verizon-communications-inc']]
                         )

# The total number of companies
n_companies = len(company_urls)

# The list of data frames for the companies
df_list = []

# Returns the entire url given a unique string
def get_url(unique_string):
    initial_string = 'https://www.dividendmax.com/united-states/nyse/'
    final_string = '/dividends'
    return initial_string + unique_string + final_string

def transform_df(df, company_name):
    # Get last paid dividend amount
    last_dividend = df.loc[df['Status'] == 'Paid']['Decl. amount'].iloc[0]
    
    # Add a column with the company name
    df['Company name'] = pd.Series([company_name for _ in range(len(df.index))])
    df['Forecast amount'] = pd.Series([last_dividend for _ in range(len(df.index))])
    
    # Specify the relevant column names
    cols = ['Company name', 'Status', 'Ex-div date', 'Pay date', 'Forecast amount']
    df_transformed = df[cols]
    # Only use data for delcared or forecast payments
    condition = (df_transformed['Status'] == 'Forecast') | (df_transformed['Status'] == 'Declared')
    df_transformed = df_transformed.loc[condition]
    
    # Drop the Status column
    df_transformed = df_transformed.drop('Status', axis=1)
    
    return df_transformed

def get_df(company_name, url, df_list):
    try:
        logging.info("Requested..." + url)
        df = pd.read_html(io=url, match='Currency')[0]
        df_list.append([df, company_name])
    except:
        logging.error(f'Error with check for {url}!')
    return None

# Returns all dfs concatenated, using threading
def concatenate_dfs():
    
    threads = [None] * n_companies
    
    # Iterate over companies
    for i in range(n_companies):
        company_name, unique_string = company_urls[i,0], company_urls[i,1]
        # The full, unique company URL
        url = get_url(unique_string)
        
        threads[i] = Thread(target=get_df, args=(company_name, url, df_list))
        threads[i].start()        

    for i in range(n_companies):
        threads[i].join()
    
    retrieved_dfs = [df_list[i][0] for i in range(len(df_list))]
    retrieved_companies = [df_list[i][1] for i in range(len(df_list))]
    
    for i in range(len(df_list)):
        # Get transformed df
        retrieved_dfs[i] = transform_df(retrieved_dfs[i], retrieved_companies[i])
        
    # Concatenate all dfs
    df_concatenated = pd.concat(retrieved_dfs, ignore_index=True)

    return df_concatenated

def sort_and_select_next(df_concatenated, number):
    # Convert dates to datetime
    df_concatenated['Ex-div date'] = pd.to_datetime(df_concatenated['Ex-div date'])
    df_concatenated['Pay date'] = pd.to_datetime(df_concatenated['Pay date'])
    
    # Drop ex-div dates from before today
    date_today = datetime.combine(date.today(), datetime.min.time())
    condition = (df_concatenated['Ex-div date'] >= date_today)    
    df_concatenated = df_concatenated.loc[condition]
    
    # Sort rows by ex dividend dates
    df_concatenated = df_concatenated.sort_values(by=['Ex-div date'])
    
    # Format dates
    df_concatenated['Ex-div date'] = df_concatenated['Ex-div date'].dt.strftime('%d %b %Y')
    df_concatenated['Pay date'] = df_concatenated['Pay date'].dt.strftime('%d %b %Y')
    
    return df_concatenated.head(number)

def format_cents_to_dollars(df):
    for i in range(len(df)):
        cent_string = df['Forecast amount'].iloc[i]
        # Amount in cents (float dtype)
        cent_amount = float(cent_string[:-1])
        # Format to dollars
        dollar_amount = 0.01 * cent_amount
        df['Forecast amount'].iloc[i] = f'${dollar_amount:.2f}'
        
    return df 

# Run the script
def run():
    # Concatenate all dfs
    df_concatenated = concatenate_dfs()
      
    # Sort by date and select display the next 10 payments (by ex-div date)
    next_dividends = sort_and_select_next(df_concatenated, 10)
    
    # Format dividend values from cents to dollars
    next_dividends = format_cents_to_dollars(next_dividends)
    
    print(next_dividends)
    
    print(f'Total time: {DT() - t_init:.2f} s')
