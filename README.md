# Personal Economy
> Contains tools for making better investment decisions. 

Overall, two tools are included:
* _Rebalancing_, which gives the user information on the proper amounts to invest in different financial instruments, given a portfolio risk allocation.
* _Dividend dates_, which provides information on the next payout dates and amounts for given stocks.

## Setup (macOS & Linux)
The necessary libraries for this application can be installed in the following way:
* Navigate into the repository directory, i.e. the location of ``requirements.txt``.
* Set up a virtual environment, e.g. via:
```sh
python3 -m venv env
```
* Activate the environment via:
```sh
source env/bin/activate
```
* Install libraries via:
```sh
pip3 install -r requirements.txt
```
The libraries listed in the document are compatible with Python 3.9.12, and were last available for download on 5th April 2022.

## Usage
* Start the application by running ``RUN.sh``, which is an executable Shell script.
* Choose between the tools by clicking the appropriate button.

### Rebalancing
Enter the required information in the input fields. The result will be both a bar chart, comparing the current portfolio with the portfolio after investing the amount at hand, and information (printed in the terminal) on the exact amounts required to invest in the different financial instruments.

### Dividend dates
This tool activates automatically when clicking the button. Given a list of company names, found in ``input/company_urls.txt``, the application returns a table showing the next 10 ex-dividend dates and payment dates for the companies, as well as the forecast payment amount per share.

## Meta
Lars Erik J. Skjegstad - lars_erik_skjegstad@hotmail.com

This repository exists for demonstration purposes only, and thus does not come with a license.
