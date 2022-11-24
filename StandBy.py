import tkinter as tk

class Standby(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)
        self.header = tk.Label(self, text='「人狼シナリオ」', font=('',24))
        self.header.pack()
        self.label = tk.Label(self, text='起動待機中…', font=('',16))
        self.label.pack()