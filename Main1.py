import tkinter as tk
from ChatLog import Chat
from Table import Table
from Term import Term
from StandBy import Standby
from numpy import int64
import os
import sys

args = sys.argv

if len(args) <= 1:
    FILES = ['excel_data', 'scenario1_silent_hanging', '確定白襲撃']
    FILE_NAME = 'Datas/' + FILES[2] + '.xlsx'
else:
    FILE_NAME = 'Datas/' + args[1] + '.xlsx'

class Log:
    # 初期化処理
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('人狼シナリオ')
        self.standby = Standby(self.root)
        self.standby.grid(row=0, column=0)
    def start_app(self):
        self.root.after(0, self.prepare_app)
        self.root.mainloop()
    def prepare_app(self):
        self.read_datas()
        self.standby.destroy()
        self.init_parameter()
        self.init_app()
    # データ関係の関数
    def data_path(self, path: str):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    def read_datas(self):
        import pandas as pd
        self.df_msg = pd.read_excel(self.data_path(FILE_NAME), sheet_name=0, index_col=0)
        self.df_spkr = pd.read_excel(self.data_path(FILE_NAME), sheet_name=1, index_col=0)
        self.df_cond = pd.read_excel(self.data_path(FILE_NAME), sheet_name=2, index_col=0)
        self.df_term = pd.read_excel(self.data_path(FILE_NAME), sheet_name=3, index_col=0)
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
        self.chat = Chat(self.root, 300, 400)
        self.term = Term(self.root)
        self.chat.grid(row=0, column=0, rowspan=2)
        self.term.grid(row=1, column=1)
        self.init_table()
        self.root.bind('<Return>', lambda e: self.next_cmd())
    # 状況表の初期化
    def init_table(self):
        self.table = Table(self.root)
        players = self.df_spkr[self.df_spkr['is_player']==1]
        self.table.init_values(players['name'], players.index)
        self.table.grid(row=0, column=1, sticky=tk.N)
        # self.table.init_color()
    # 次のメッセージへ
    def next_cmd(self):
        if self.log_id < len(self.df_msg):
            # dfからデータを取り出す
            spkr_id = self.df_msg.loc[self.log_id,'speaker_id']
            content = self.df_msg.loc[self.log_id,'content']
            # spkr_idに応じた処理を行う
            if isinstance(spkr_id, int):
                self.next_msg(spkr_id, content)
            elif isinstance(spkr_id, int64):
                print('^^')
                self.next_msg(int(spkr_id), content)
            elif spkr_id == 'DAY':
                self.chat.center_view(content)
            elif isinstance(spkr_id, float):
                self.next_msg(int(spkr_id), content)
            else:
                print(spkr_id, type(spkr_id))
            # ログIDを1進める
            self.log_id += 1
    def next_msg(self, spkr_id, content):
        cond_id = self.df_msg.loc[self.log_id,'condition_index']
        term_id = self.df_msg.loc[self.log_id,'term_index']
        color = self.df_spkr.loc[spkr_id,'color']
        spkr_name = self.df_spkr.loc[spkr_id,'name']
        sender = self.get_sender(spkr_id, spkr_name, color)
        if 'side' in self.df_spkr.columns:
            side = self.df_spkr.loc[spkr_id,'side']
        else:
            side = 'left'
        # for id, name in self.msg_replace: #content内のidの変換(いらないかも)
        #     content = content.replace(id, name)
        # ログ、状況表、コラムを更新する
        self.logs.append((spkr_name, content))
        self.chat.send_msg(content, sender, side=side, color=color)
        self.update_condition(cond_id)
        self.update_term(term_id)
    def get_sender(self, id, name, color):
        if color != 'white':
            return (name, color, 'black')
        bg = ('white', 'red', 'orange', 'lime', 'green', 'blue', 'dark violet', 'pink', 'violet red', 'goldenrod')
        fg = ['black', 'white', 'black', 'black', 'white', 'white', 'white', 'black', 'white', 'white']
        return (name, bg[id], fg[id])
    # 状況表の更新
    def update_condition(self, id):
        # idの検証
        try:
            id = int(id)
        except ValueError:
            return
        # self.table.init_color()
        # 指定されたidの分更新していく
        for i in range(self.cond_id, id+1):
            row = self.df_cond.loc[i]
            self.table.update_value(row['speaker_id'], row['column'], row['cmd'], row['content'])
            # self.table.update_color(str(row["speaker_id"]), 'yellow')
            self.cond_id += 1
    def update_term(self, id):
        # idの検証
        try:
            id = int(id)
        except ValueError:
            return
        row = self.df_term.loc[id]
        self.term.insert_content(row['term'], row['explanation'])

if __name__ == '__main__':
    log = Log()

    log.start_app()