import pandas as pd
import tkinter as tk
from ChatLog import Chat
import os

FILE_NAME = 'Datas/scenario1_silent_hanging.xlsx'

class Log:
    def __init__(self):
        self.read_datas()
        self.init_parameter()
        self.init_app()
    def data_path(self, path: str):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    def read_datas(self):
        self.df_msg = pd.read_excel(self.data_path(FILE_NAME), sheet_name=0, index_col=0)
        self.df_spkr = pd.read_excel(self.data_path(FILE_NAME), sheet_name=1, index_col=0)
    def init_parameter(self):
        self.log_id = 0
        self.logs:list[tuple] = []   # (name, content)
        self.msg_replace = [(f'{{{i}}}', row['name']) for i, row in self.df_spkr.iterrows() if row['is_player']]
        self.is_auto = False
        self.auto_msg_time = 3
    def init_app(self):
        self.root = tk.Tk()
        self.chat = Chat(self.root, 300, 400)
        self.chat.pack()
        self.root.bind('<Return>', lambda e: self.next_cmd())
    def next_cmd(self):
        if self.log_id < len(self.df_msg):
            # dfからデータを取り出す
            spkr_id = self.df_msg.loc[self.log_id,'speaker_id']
            content = self.df_msg.loc[self.log_id,'content']
            color = self.df_spkr.loc[spkr_id,'color']
            spkr_name = self.df_spkr.loc[spkr_id,'name']
            for id, name in self.msg_replace:
                content = content.replace(id, name)
            # ログへ渡す
            self.logs.append((spkr_name, content))
            self.chat.send_msg(content, (spkr_name, 'red'), color=color)
            # ログIDを1進める
            self.log_id += 1

if __name__ == '__main__':
    log = Log()
    log.root.mainloop()