from gui_base import *
from modules.shuffle import HANJA_IDX, HMS_IDX, LEVEL_IDX
from modules.refactor import refactor_data
import random
import time
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
        self.start_time = time.time()
    
    def show_text(self, event):
        response = self.entry.get()
        han, kor, lev = self.get_data()
        f_str = f'[{str(self.cur_idx+1)}/{len(li)}] '
        # TODO: 갚을/알릴 보 같은 경우에는 하나만 써도 맞게 하기!
        # TODO: 회복할 복|다시 부 같은 경우에는 둘 다 써야 맞게 하기. 근데 순서는 달라도 됨
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
            self.show_result()
    
    def show_result(self):
        # 결과 저장
        self.save_result()

        # 라벨 지우기
        self.remove_labels()

        # 점수 계산
        total = len(li)
        grade = total-len(self.result)
        res_txt = f'{grade} / {total}개'
        percent = 100*grade//total
        percent_str = f'{percent} / 100점'

        # 라벨 설정 (end, 맞은 개수, 백분율, 걸린 시간)
        label_closing = tk.Label(window, text=closing_remark, font=normal_font)
        label_closing.grid(row=2, column=0, columnspan=2)
        label_result = tk.Label(window, text=res_txt, font=normal_font)
        label_result.grid(row=3, column=0, columnspan=2)
        label_grade = tk.Label(window, text=percent_str, font=normal_font)
        label_grade.grid(row=4, column=0, columnspan=2)
        elasped = time.time() - self.start_time
        elasped_time = f'{elasped:.2f}초'
        label_elasped_time = tk.Label(window, text=elasped_time, font=normal_font)
        label_elasped_time.grid(row=5, column=0, columnspan=2)
    
    # TODO 창 닫기 버튼
    
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
        # TODO: end 보여주기 (closing_remark)
    
    def get_data(self):
        kor = li[self.cur_idx][HMS_IDX]
        han = li[self.cur_idx][HANJA_IDX]
        level_raw = li[self.cur_idx][LEVEL_IDX]
        level = refactor_data(level_raw)
        return han, kor, level


test_base = ReadingTest()
window.mainloop()