import tkinter as tk

class Window:
    def __init__(self):
        self.window = tk.Tk()

        self.window.rowconfigure(0, minsize=50, weight=1)
        self.window.columnconfigure([0, 1, 2], minsize=50, weight=1)

        btn_decrease = tk.Button(master=self.window,
                                 text="Dividend dates",
                                 command=self.run_dividend_dates)
        
        btn_decrease.grid(row=0, column=0, sticky="nsew")

        self.lbl_value = tk.Label(master=self.window, text="Choose an option")
        self.lbl_value.grid(row=0, column=1)

        btn_increase = tk.Button(master=self.window,
                                 text="Rebalancing",
                                 command=self.run_rebalancing)
        
        btn_increase.grid(row=0, column=2, sticky="nsew")

        self.window.mainloop()

    # Functions
    def close_window(self):
        self.window.destroy()
    
    def run_dividend_dates(self):
        self.lbl_value["text"] = 'Will run dividend_dates'

        # Run the dividend_dates.py script
        self.close_window()
        from dividends import dividend_dates

    def run_rebalancing(self):
        self.lbl_value["text"] = 'Will run rebalancing'

def run():
    window_obj = Window()



