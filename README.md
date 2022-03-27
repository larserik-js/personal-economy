# Personal Economy
> Contains tools for making better investment decisions. 

Overall, two tools are included:
* _Rebalancing_, which gives the user information on the proper amounts to invest in different financial instruments, given a portfolio risk allocation.
* _Dividend dates_, which provides information on the next payout dates and amounts for given stocks.

## Setup (OS X & Linux)
The necessary libraries for this application can be installed in the following way:
* Navigate into the directory of ``requirements.txt``.
* Set up a virtual environment.
* Install libraries via:
```sh
pip install -r requirements.txt
```

## Usage
* Run the application by double-clicking ``RUN.sh``, which is an executable Shell script.
* Choose between the tools by clicking the appropriate button.

### Rebalancing
Enter the required information in the input fields. The result will be both a bar chart, comparing the current portfolio with the portfolio after investing the amount at hand, and information (printed in the terminal) on the exact amounts required to invest in the different financial instruments.

### Dividend dates
This tool activates automatically when clicking the button. Given a list of company names (pre-written in the code for the purpose of this repository), the application returns a table showing the next 10 ex-dividend dates for the companies, and the forecast payment amount per share.

## Meta
Lars Erik J. Skjegstad - lars_erik_skjegstad@hotmail.com

This project is not open source, and thus does not come with a license.