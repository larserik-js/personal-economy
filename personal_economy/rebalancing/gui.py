"""Input widget.

Functions:
    * get_input - initialize widget where the user name, the investment amount,
      and investment currency is input.
"""
import tkinter as tk
from tkinter import ttk


class _App(tk.Tk):

    def __init__(self):
        super().__init__()

        # initialize data
        self.person_names = ['test-person1', 'test-person2']
        self.currencies = ['DKK', 'NOK', 'EUR', 'USD']

        self.person, self.amount, self.currency = '', '', ''

        # set up variable
        self.option_var_person = tk.StringVar(self)
        self.option_var_currency = tk.StringVar(self)

        self.entry_amount = ttk.Entry(self)

        # create widget
        self._create_widget()

    def _create_widget(self):
        self.title('')
        self.geometry("500x150")

        # Padding for widgets using the grid layout
        paddings = {'padx': 5, 'pady': 5}
        
        # Set headline font
        headline_font = ('Helvetica', 12, 'bold')

        # Option menu (input person name)
        option_label_person = ttk.Label(self,  text='Select person name:', 
                                        font = headline_font)
        option_label_person.grid(row=0, column=0, sticky=tk.W, **paddings)
        option_menu_person = ttk.OptionMenu(
            self, self.option_var_person, self.person_names[0],
            *self.person_names, command=None
        )
        option_menu_person.grid(row=0, column=1, sticky=tk.W, **paddings)

        # Input field (investment amount)
        label_amount = ttk.Label(self, text='Enter amount to invest:',
                        font=headline_font)
        label_amount.grid(row=1, column=0)
        self.entry_amount.grid(row=1, column=1)

        # Option menu (currency)
        option_menu_person = ttk.OptionMenu(
            self, self.option_var_currency, self.currencies[0],
            *self.currencies, command=None
        )
        option_menu_person.grid(row=1, column=2, sticky=tk.W, **paddings)

        # OK button
        ok_button = tk.Button(self, text='OK', state=tk.NORMAL, 
                              command=self._get_input)
        ok_button.grid(row=3, column=1)

    def _get_input(self):
        # Get input data
        self.person = self.option_var_person.get()
        self.amount = self.entry_amount.get()
        self.currency = self.option_var_currency.get()

        try:
            float(self.amount)
        except ValueError:
            # Set label to indicate invalid investment amount input
            self.label_invalid = ttk.Label(self, text='Invalid value!')
            self.label_invalid.grid(row=2, column=1)
        # Return amount and destroy widget
        else:
            self.amount = float(self.amount)
            self.destroy()


def get_input():
    widget = _App()
    widget.mainloop()
    
    return widget.person, widget.amount, widget.currency