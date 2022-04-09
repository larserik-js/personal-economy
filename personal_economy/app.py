"""The main application.

Functions:
    * run - initializes a widget, which lets the user decide which of the tools
      to use.
"""
import tkinter as tk

from personal_economy.rebalancing import rebalancing
from personal_economy.dividends import dividend_dates


class _Window:
    
    def __init__(self):
        # Initialize window
        self.window = self._initialize_window()

    def _initialize_window(self):
        window = tk.Tk()
        window.title('Personal economy tools')

        # Do not allow resizing
        window.resizable(height=0, width=0)

        # Configure window geometry
        window.columnconfigure([0, 1, 2], minsize=70)
        window.rowconfigure(0, minsize=60)

        # Button
        btn_div_dates = tk.Button(master=window,
                                 text="Dividend dates",
                                 command=self._run_dividend_dates)
        
        ## Assign place in cell
        btn_div_dates.grid(row=0, column=0, sticky="NSEW")

        # Label
        lbl_value = tk.Label(master=window, text="<-- Choose an option -->")
        lbl_value.grid(row=0, column=1)

        # Button
        btn_rebalancing = tk.Button(master=window,
                                 text="Rebalancing",
                                 command=self._run_rebalancing)

        ## Assign place in cell
        btn_rebalancing.grid(row=0, column=2, sticky="NSEW")

        return window

    # Methods
    def mainloop(self):
        self.window.mainloop()
    
    def _close_window(self):
        self.window.destroy()
    
    def _run_dividend_dates(self):
        self._close_window()

        # Run the dividend_dates.py script
        dividend_dates.run()

    def _run_rebalancing(self):
        self._close_window()

        rebalancing.CalculateInvestments()
        
def run():
    # Make window object
    window_obj = _Window()

    # Run mainloop
    window_obj.mainloop()