from gui_base import *
from modules.shuffle import HANJA_IDX, HMS_IDX, LEVEL_IDX
from modules.refactor import refactor_data
import random

from modules.load import load_file__part
li = load_file__part()

class ReadingTest:
    def __init__(self):
        self.cur_idx = 0
        self.label_han = tk.Label(window, text=" ", anchor="w", font=large_font)
        self.label_kor = tk.Label(window, text=" ", font=normal_font)
        self.label_lev = tk.Label(window, text=" ", font=normal_font)
        self.label_cnt = tk.Label(window, text=" ", font=normal_font)
        self.label_new = tk.Label(window, text=" ", font=normal_font)
        window.grid_columnconfigure(0, weight=1)  # Column 0 will expand to center-align elements
        window.grid_columnconfigure(1, weight=1)  # Column 1 will also expand for label_new
        random.shuffle(li)
        self.entry = tk.Entry(window)
        self.entry.bind('<Return>', self.show_text)
        self.label_han.grid(row=0, column=0, columnspan=2)  # Set columnspan to 2 to span both columns
        self.label_kor.grid(row=1, column=0, columnspan=2)
        self.label_lev.grid(row=2, column=0, columnspan=2)
        self.label_cnt.grid(row=3, column=0, sticky="e")  # Use sticky="e" for right-align
        self.label_new.grid(row=3, column=1, sticky="w")  # Use sticky="w" for left-align
        self.label_han.config(text=li[0][HANJA_IDX])
        self.entry.grid(row=4, columnspan=2)
        self.result = []
    
    def show_text(self, event):
        response = self.entry.get()
        han, kor, lev = self.get_data()
        f_str = f'[{str(self.cur_idx+1)}/{len(li)}] '
        if kor == response:
            f_str = f_str + 'right!'
        else:
            f_str = f_str + f'wrong:: {han} {kor}'
            dic = {
                'han': han,
                'kor': kor,
                'lev': lev
            }
            self.result.append(dic)
        print(f_str)
        self.entry.delete(0, tk.END)
        self.update_labels()

    # TODO: 0부터 시작하는게 아니라 idx가 1부터 시작돼서..
    #  맨 첫번째 있는 한자는 아예 건너뛰는 현상 고치기 => 완료!
    def update_labels(self):
        self.cur_idx += 1
        if self.cur_idx > 0:
            self.entry.grid(row=4, columnspan=2)
        if self.cur_idx < len(li):
            han, _, _ = self.get_data()
            self.label_han.config(text=han)
        else:
            for res in self.result:
                print(res)
            print(f'result:{len(li)-len(self.result)}/{len(li)}')
            self.save_result()
            self.remove_labels()
    
    def save_result(self):
        import csv
        with open('./data/data_today_wrong.csv', 'w') as f:
            wr = csv.writer(f)
            wr.writerow(['level', 'hanja', 'mean', 'pron', 'hms'])
            for res in self.result:
                han = res['han']
                kor = res['kor']
                lev = res['lev']
                row = [lev, han, '', '', kor]
                wr.writerow(row)
    
    def remove_labels(self):
        self.label_han.grid_remove()
        self.entry.grid_forget()
    
    def get_data(self):
        kor = li[self.cur_idx][HMS_IDX]
        han = li[self.cur_idx][HANJA_IDX]
        level_raw = li[self.cur_idx][LEVEL_IDX]
        level = refactor_data(level_raw)
        return han, kor, level


test_base = ReadingTest()
window.mainloop()