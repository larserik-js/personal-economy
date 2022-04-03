import pandas as pd
from datetime import date, timedelta


# Get today's exchange rates
def scrape_ERs():
    # URL for currency exchange rates
    url = 'https://www.nationalbanken.dk/valutakurser'
    
    print('Getting currency exchange rates...')
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