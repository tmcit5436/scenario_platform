import site
import pandas as pd
import tkinter as tk
from ChatLog import Chat
from Table import Table
import os

FILE_NAME = 'Datas/scenario1_silent_hanging.xlsx'

class Log:
    # 初期化処理
    def __init__(self):
        self.read_datas()
        self.init_parameter()
        self.init_app()
    # データ関係の関数
    def data_path(self, path: str):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    def read_datas(self):
        self.df_msg = pd.read_excel(self.data_path(FILE_NAME), sheet_name=0, index_col=0)
        self.df_spkr = pd.read_excel(self.data_path(FILE_NAME), sheet_name=1, index_col=0)
        self.df_cond = pd.read_excel(self.data_path(FILE_NAME), sheet_name=2, index_col=0)
    # パラメータの初期化
    def init_parameter(self):
        self.log_id = 0
        self.cond_id = 0
        self.logs:list[tuple] = []   # (name, content)
        # self.msg_replace = [(f'{{{i}}}', row['name']) for i, row in self.df_spkr.iterrows() if row['is_player']]
        # self.is_auto = False
        # self.auto_msg_time = 3
    # アプリの初期化
    def init_app(self):
        self.root = tk.Tk()
        self.chat = Chat(self.root, 300, 400)
        self.chat.grid(row=0, column=0)
        self.init_table()
        self.root.bind('<Return>', lambda e: self.next_cmd())
    # 状況表の初期化
    def init_table(self):
        self.table = Table(self.root)
        players = self.df_spkr[self.df_spkr['is_player']==1]
        self.table.init_values(players['name'], players.index)
        self.table.grid(row=0, column=1, sticky=tk.N)
    # 次のメッセージへ
    def next_cmd(self):
        if self.log_id < len(self.df_msg):
            # dfからデータを取り出す
            spkr_id = self.df_msg.loc[self.log_id,'speaker_id']
            content = self.df_msg.loc[self.log_id,'content']
            cond_id = self.df_msg.loc[self.log_id,'condition_index']
            color = self.df_spkr.loc[spkr_id,'color']
            spkr_name = self.df_spkr.loc[spkr_id,'name']
            # for id, name in self.msg_replace: #
            #     content = content.replace(id, name)
            # ログ、状況表、コラムを更新する
            self.logs.append((spkr_name, content))
            self.chat.send_msg(content, (spkr_name, 'red'), color=color)
            self.update_condition(cond_id)
            # ログIDを1進める
            self.log_id += 1
    # 状況表の更新
    def update_condition(self, id):
        # idの検証
        try:
            id = int(id)
        except ValueError:
            return
        self.table.init_color()
        # 指定されたidの分更新していく
        for i in range(self.cond_id, id+1):
            row = self.df_cond.loc[i]
            self.table.update_value(row['speaker_id'], row['column'], row['cmd'], row['content'])
            # self.table.update_color(str(row["speaker_id"]), 'yellow')
            self.cond_id += 1

if __name__ == '__main__':
    log = Log()
    log.root.mainloop()