import tkinter as tk

class Term(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master, height=198, width=420)
        self.grid_propagate(False)
        self.init_parameter()        
        self.init_text()
        self.init_button()
    def init_parameter(self):
        self.page_now = 0
        self.page_max = 0
        self.headers = []
        self.texts = []
    def init_text(self):
        # new = tk.Label(self, text='new!', fg='yellow')
        # new.grid(row=0, column=0, sticky=tk.N)
        self.header = tk.Label(self, text='「コラム」', font=('',28))
        self.header.grid(row=0, column=0, columnspan=3, sticky=tk.N)
        self.text = tk.Label(self, text='ここにシナリオ内に出てきた\n人狼の用語の説明が書かれます。', font=('',18), anchor=tk.N, justify=tk.CENTER, width=38, height=5)
        self.text.grid(row=1, column=0, columnspan=3)
    def init_button(self):
        self.button_prev = tk.Button(self, text='←', command=lambda: self.add_page(-1))
        self.button_prev.grid(row=2, column=0, sticky=tk.E, pady=10)
        self.button_next = tk.Button(self, text='→', command=lambda: self.add_page(1))
        self.button_next.grid(row=2, column=2, sticky=tk.W, pady=10)
        self.page_label = tk.Label(self, text='0/0')
        self.page_label.grid(row=2, column=1, pady=5)
        self.activate_button()
    # ページ関連
    def add_page(self, diff):
        self.set_page(self.page_now + diff)
    def set_page(self, page_now):
        self.page_now = page_now
        self.header.config(text=f'「{self.headers[self.page_now-1]}」')
        self.text.config(text=self.texts[self.page_now-1])
        self.page_label.config(text=f'{self.page_now}/{self.page_max}')
        self.activate_button()
    def activate_button(self):
        self.prev_stat = tk.DISABLED if self.page_now <= 1 else tk.ACTIVE
        self.next_stat = tk.DISABLED if self.page_now >= self.page_max else tk.ACTIVE
        self.button_prev.config(state=self.prev_stat)
        self.button_next.config(state=self.next_stat)
    # 内容追加
    def insert_content(self, header, text, set_end_page=True):
        self.page_max += 1
        self.headers.append(header)
        self.texts.append(text)
        if set_end_page:
            self.set_page(self.page_max)
        else:
            self.page_label.config(text=f'{self.page_now}/{self.page_max}')
            self.activate_button()

if __name__ == '__main__':
    root = tk.Tk()

    term = Term(root)
    term.grid()

    term.insert_content('CO', 'カミングアウトの略')
    term.insert_content('白', '白は人狼ではないという意味')
    term.insert_content('黒', '黒は人狼であるという意味', False)

    root.mainloop()