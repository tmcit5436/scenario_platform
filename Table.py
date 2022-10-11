import tkinter as tk
from tkinter import ttk

class Table(ttk.Treeview):
    def __init__(self, master: tk.Misc):
        super().__init__(master, show=['headings'])

        self['column'] = ('name', 'alive', 'job', 'skill')

        self.column('#0', width=0, stretch='no')
        self.column('name', anchor=tk.CENTER, width=100)
        self.column('alive', anchor=tk.CENTER, width=50)
        self.column('job', anchor=tk.CENTER, width=60)
        self.column('skill', anchor=tk.W, width=200)

        self.heading('#0', text='')
        self.heading('name', text='名前', anchor=tk.CENTER)
        self.heading('alive', text='生存', anchor=tk.CENTER)
        self.heading('job', text='役職', anchor=tk.CENTER)
        self.heading('skill', text='能力結果', anchor=tk.CENTER)
    def init_values(self, names: list):
        for i, name in enumerate(names):
            self.insert('', 'end', iid=i, values=(name, '', '', ''))

if __name__ == '__main__':
    root = tk.Tk()
    
    tree = Table(root)
    tree.init_values('ABCDE')
    tree.pack()

    root.mainloop()