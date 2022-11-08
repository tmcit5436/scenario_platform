import tkinter as tk

class Chat(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height)
        self.canvas = tk.Canvas(self, width=width, height=height, bg='skyblue', scrollregion=(0,0,0,0))
        self.canvas.grid(row=0, column=0)
        self.init_parameter(width, height)
        self.init_scrollbar()
    # 初期化処理
    def init_parameter(self, width, height):
        self.msg_index = 0
        self.y_diff = 10
        self.width = width
        self.height = height
    def init_scrollbar(self):
        self.bar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.bar.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.bar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.bar.set)
    # メッセージの追加
    def send_msg(self, msg: str, sender=('sender','red'), side='left', color='white'):
        tag = f'msg{self.msg_index}'
        if side == 'right':
            self.send_right_msg(msg, sender, color, tag)
        else:
            self.send_left_msg(msg, sender, color, tag)
        self.msg_index += 1
        self.canvas.config(scrollregion=(0,0,0,self.y_diff))
        self.canvas.yview_moveto(1)
    def send_left_msg(self, msg, sender, color, tag):
        # アイコン
        self.canvas.create_oval(5, self.y_diff, 30, self.y_diff+25, fill='red')
        self.canvas.create_text(17.5, self.y_diff+12.5, text=sender[0][0])
        x_icon = 27
        # 名前
        if not sender is None:
            name_id = self.canvas.create_text(15+x_icon, self.y_diff-3, text=sender[0], font=('',11), fill='black', anchor=tk.NW, tags=tag)
            pos = self.canvas.bbox(name_id)
            self.y_diff += pos[3] - pos[1]
        # メッセージ本文
        text_id = self.canvas.create_text(20+x_icon, self.y_diff, text=msg, fill='black', width=250, anchor=tk.NW, tags=tag)
        pos = [elem+diff for elem, diff in zip(self.canvas.bbox(text_id), (-2,-2,2,2))]
        # 吹き出し
        back_id = self.canvas.create_polygon(
            pos[0], pos[3], pos[2], pos[3], pos[2], pos[1], pos[0]-10, pos[1], pos[0], pos[1]+7, 
            fill=color, width=0, joinstyle=tk.ROUND, tags=tag)
        self.canvas.lower(back_id)
        self.y_diff += pos[3] - pos[1] + 10
    def send_right_msg(self, msg, sender, color, tag):
        # 名前
        if not sender is None:
            name_id = self.canvas.create_text(self.width-12, self.y_diff-3, text=sender[0], font=('',11), fill='black', anchor=tk.NE, tags=tag)
            pos = self.canvas.bbox(name_id)
            self.y_diff += pos[3] - pos[1]
        # メッセージ本文
        text_id = self.canvas.create_text(self.width-17, self.y_diff, text=msg, fill='black', width=250, anchor=tk.NE, tags=tag)
        pos = [elem+diff for elem, diff in zip(self.canvas.bbox(text_id), (-2,-2,2,2))]
        # 吹き出し
        back_id = self.canvas.create_polygon(
            pos[2], pos[3], pos[0], pos[3], pos[0], pos[1], pos[2]+12, pos[1], pos[2], pos[1]+7, 
            fill=color, width=0, joinstyle=tk.ROUND, tags=tag)
        self.canvas.lower(back_id)
        self.y_diff += pos[3] - pos[1] + 10