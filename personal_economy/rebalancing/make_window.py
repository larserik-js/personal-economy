import tkinter as tk

class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.fields = ['Enter person name ("Anna" or "LE")',
                       'Enter amount to invest followed by currency (e.g. 1000 EUR)']
        self.input_strings = []
        self.ents = self.makeform(self.root, self.fields)
    
    def fetch(self, entries):
        for entry in entries:
            #field = entry[0]
            #text  = entry[1].get()
            self.input_strings.append(entry[1].get())
            #print('%s: "%s"' % (field, text))
        self.close_window()
            
    def makeform(self, root, fields):
        entries = []
        for field in fields:
            row = tk.Frame(root)
            lab = tk.Label(row, width=15, text=field, anchor='w')
            ent = tk.Entry(row)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append((field, ent))
        return entries

    def get_input(self):
        self.root.bind('<Return>', (lambda event, e=self.ents: self.fetch(e)))   
        b1 = tk.Button(self.root, text='Show',
                        command=(lambda e=self.ents: fetch(e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
        b2 = tk.Button(self.root, text='Quit', command=self.root.quit)
        b2.pack(side=tk.LEFT, padx=5, pady=5)
        self.root.mainloop()

        return self.input_strings

    def close_window(self):
        self.root.destroy()

