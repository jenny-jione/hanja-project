from gui_base import *
from modules.shuffle import HANJA_IDX, HMS_IDX, LEVEL_IDX
from modules.refactor import refactor_data
import random
import time
from modules.load import load_file

class ReadingTest:
    def __init__(self, src, dst):
        self.li = load_file(src)
        self.result_file = dst
        self.cur_idx = 0
        self.ans = 1
        self.label_han = tk.Label(window, text=" ", anchor="w", font=large_font)
        self.label_kor = tk.Label(window, text=" ", font=normal_font)
        self.label_lev = tk.Label(window, text=" ", font=normal_font)
        self.label_index = tk.Label(window, text=" ", font=normal_font)
        self.label_total = tk.Label(window, text=" ", font=normal_font)
        window.grid_columnconfigure(0, weight=1)  # Column 0 will expand to center-align elements
        window.grid_columnconfigure(1, weight=1)  # Column 1 will also expand for label_new
        self.entry = tk.Entry(window)
        self.entry.bind('<Return>', self.show_text)
        self.label_han.grid(row=0, column=0, columnspan=2)  # Set columnspan to 2 to span both columns
        self.label_kor.grid(row=1, column=0, columnspan=2)
        self.label_lev.grid(row=2, column=0, columnspan=2)
        self.label_index.grid(row=3, column=0, sticky="e")  # Use sticky="e" for right-align
        self.label_total.grid(row=3, column=1, sticky="w")  # Use sticky="w" for left-align
        self.entry.grid(row=4, columnspan=2)
        
        self.label_han.config(text=self.li[0][HANJA_IDX])
        self.label_index.config(text=self.cur_idx+1)
        self.label_total.config(text='/ ' + str(len(self.li)))
        
        self.label_noti = tk.Label(window, text='', font=normal_font)
        self.label_noti.grid(row=5, columnspan=2)
        
        self.result = []
        self.start_time = time.time()
    
    def show_text(self, event):
        self.ans += 1
        # 입력값 변수에 저장
        response = self.entry.get()
        han, kor, lev = self.get_data()
        
        if self.ans == 2:
            # 정답 노출
            self.label_kor.config(text=kor)
            self.label_lev.config(text=lev)
            self.ans = 0
            
            # 채점
            if kor == response:
                f_str ='right!'
            else:
                f_str =f'wrong :: {kor}'
                dic = {
                    'han': han,
                    'kor': kor,
                    'lev': lev
                }
                self.result.append(dic)
            self.label_noti.config(text=f_str)
        else:
            self.entry.delete(0, tk.END)
            
            self.update_labels()
            self.label_kor.config(text='')
            self.label_lev.config(text='')
            self.label_noti.config(text='')

    def update_labels(self):
        self.cur_idx += 1
        if self.cur_idx > 0:
            self.entry.grid(row=4, columnspan=2)
        if self.cur_idx < len(self.li):
            han, _, _ = self.get_data()
            self.label_han.config(text=han)
            self.label_index.config(text=self.cur_idx+1)
        else:
            self.show_result()
    
    def show_result(self):
        # 결과 저장
        self.save_result()
        
        # 라벨, 엔트리 지우기
        self.remove_elements()
        
        # 점수 계산
        total = len(self.li)
        grade = total-len(self.result)
        res_txt = f'{grade}개 / {total}개'
        percent = 100*grade//total
        percent_str = f'{percent}%'

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
        with open(self.result_file, 'w') as f:
            wr = csv.writer(f)
            wr.writerow(['level', 'hanja', 'mean', 'pron', 'hms'])
            for res in self.result:
                han = res['han']
                kor = res['kor']
                lev = res['lev']
                row = [lev, han, '', '', kor]
                wr.writerow(row)
    
    def remove_elements(self):
        self.label_han.grid_remove()
        self.entry.grid_forget()
        self.entry.unbind('<Return>')
        self.label_index.grid_remove()
        self.label_total.grid_remove()
    
    def get_data(self):
        kor = self.li[self.cur_idx][HMS_IDX]
        han = self.li[self.cur_idx][HANJA_IDX]
        level_raw = self.li[self.cur_idx][LEVEL_IDX]
        level = refactor_data(level_raw)
        return han, kor, level


IDX = '05'
FILE_SRC = f'./data/data_review_split_{IDX}.csv'
FILE_DST = f'./data/data_review_wrong_{IDX}.csv'
test_base = ReadingTest(FILE_SRC, FILE_DST)
window.mainloop()