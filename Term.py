import tkinter as tk

class Term(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master, height=198, width=420)
        self.grid_propagate(False)
        # self.propagate(False)
        self.init_text()
        self.init_button()
    def init_text(self):
        # new = tk.Label(self, text='new!', fg='yellow')
        # new.grid(row=0, column=0, sticky=tk.N)
        header = tk.Label(self, text='「CO」', font=('',28))
        header.grid(row=0, column=0, columnspan=3, sticky=tk.N)
        text = tk.Label(self, text='COは、カミングアウトの略。\n自分の役職をカミングアウトすることを指す。', font=('',18), anchor=tk.N, justify=tk.CENTER, width=38, height=5)
        text.grid(row=1, column=0, columnspan=3)
    def init_button(self):
        button_prev = tk.Button(self, text='←')
        button_prev.grid(row=2, column=0, sticky=tk.E, pady=10)
        button_next = tk.Button(self, text='→')
        button_next.grid(row=2, column=2, sticky=tk.W, pady=10)
        page_label = tk.Label(self, text='１／１')
        page_label.grid(row=2, column=1, pady=5)

if __name__ == '__main__':
    root = tk.Tk()

    term = Term(root)
    term.grid()

    root.mainloop()