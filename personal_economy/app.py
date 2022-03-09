import tkinter as tk
from personal_economy.rebalancing import rebalancing

class Window:
    def __init__(self):
        # Initialize window
        self.window = self.initialize_window()

    def initialize_window(self):
        window = tk.Tk()

        window.rowconfigure(0, minsize=50, weight=1)
        window.columnconfigure([0, 1, 2], minsize=50, weight=1)

        # Button
        btn_decrease = tk.Button(master=window,
                                 text="Dividend dates",
                                 command=self.run_dividend_dates)
        
        btn_decrease.grid(row=0, column=0, sticky="nsew")

        # Label
        lbl_value = tk.Label(master=window, text="Choose an option")
        lbl_value.grid(row=0, column=1)

        btn_increase = tk.Button(master=window,
                                 text="Rebalancing",
                                 command=self.run_rebalancing)

        # Button
        btn_increase.grid(row=0, column=2, sticky="nsew")

        return window

    # Functions
    def mainloop(self):
        self.window.mainloop()
    
    def close_window(self):
        self.window.destroy()
    
    def run_dividend_dates(self):
        self.close_window()

        # Run the dividend_dates.py script
        from dividends import dividend_dates

    def run_rebalancing(self):
        self.close_window()

        # Run the dividend_dates.py script
        rebalancing.run()
        
def run():
    # Make window object
    window_obj = Window()
    # Run mainloop
    window_obj.mainloop()



