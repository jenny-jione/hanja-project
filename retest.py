# 부수 추가 version

from gui_base import *
from modules.index import (
    HANJA_IDX, KOR_IDX, LEVEL_IDX, RADICAL_IDX, RADICAL_NAME_IDX,
    STROKE_COUNT, REP_PRON_IDX
    )
import random
import time
import csv
from modules.load import load_file
#  hanja, kor, radical, radical_name, stroke_count, level, rep_pron, mistake
DATA_ACCUMULATED = './data/accumulated_results.csv'
li = load_file(DATA_ACCUMULATED)
CHUNK = 5
# IDX = 10
# print(f'idx: {IDX}, {IDX*CHUNK}:{(IDX+1)*CHUNK}, total: {len(li)}')
# li = li[IDX*CHUNK:(IDX+1)*CHUNK]
random.shuffle(li)
li_res = li[CHUNK:]
li = li[:CHUNK]
print(len(li_res))
print(len(li))

ROW_HANJA = 0
ROW_KOR = 1
ROW_NOTI = ROW_CLOSING = 2
ROW_LEVEL = ROW_RESULT = 3
ROW_RADICAL = ROW_GRADE = 4
ROW_ENTRY = ROW_TIME = 5
ROW_PROGRESS = 6

class ReTest:
    def __init__(self):
        self.cur_idx = 0
        self.ans = 1
        self.label_han = tk.Label(window, text=" ", anchor="w", font=large_font)
        self.label_kor = tk.Label(window, text=" ", font=normal_font)
        self.label_radical = tk.Label(window, text=" ", font=small_font)
        self.label_lev = tk.Label(window, text=" ", font=small_font)
        self.label_noti = tk.Label(window, text='', font=normal_font)
        self.label_index = tk.Label(window, text=" ", font=small_font)
        self.label_total = tk.Label(window, text=" ", font=small_font)
        window.grid_columnconfigure(0, weight=1)  # Column 0 will expand to center-align elements
        window.grid_columnconfigure(1, weight=1)  # Column 1 will also expand for label_new
        # random.shuffle(li)
        self.entry = tk.Entry(window)
        self.entry.bind('<Return>', self.show_text)
        self.label_han.grid(row=ROW_HANJA, column=0, columnspan=2)  # Set columnspan to 2 to span both columns
        self.label_kor.grid(row=ROW_KOR, column=0, columnspan=2)
        self.label_noti.grid(row=ROW_NOTI, columnspan=2)
        self.label_lev.grid(row=ROW_LEVEL, column=0, columnspan=2)
        self.label_radical.grid(row=ROW_RADICAL, column=0, columnspan=2)
        self.entry.grid(row=ROW_ENTRY, columnspan=2)
        self.label_index.grid(row=ROW_PROGRESS, column=0, sticky="e")  # Use sticky="e" for right-align
        self.label_total.grid(row=ROW_PROGRESS, column=1, sticky="w")  # Use sticky="w" for left-align
        
        self.label_han.config(text=li[0][HANJA_IDX])
        self.label_index.config(text=self.cur_idx+1)
        self.label_total.config(text='/ ' + str(len(li)))
        
        self.good = 0
        self.checkgood = 0
        
        
        self.result = []
        self.start_time = time.time()
    
    def show_text(self, event):
        self.ans += 1
        # 입력값 변수에 저장
        response = self.entry.get()
        
        row = self.get_data()
        kor = row[KOR_IDX]
        radical = row[RADICAL_IDX]
        radical_name = row[RADICAL_NAME_IDX]
        lev = row[LEVEL_IDX]
        mistake = int(row[-1])
        
        if self.ans == 2:
            # 정답 노출
            self.label_kor.config(text=kor)
            self.label_lev.config(text=lev)
            self.label_radical.config(text=f'{radical}:{radical_name}')
            self.ans = 0
            
            # 채점
            check_result = self.check_response(answer=kor, user_response=response)
            # 정답 -> mistake -= 1
            if check_result:
                mistake -= 1
                self.checkgood += 1
                f_str =f'right! :D'
            # 오답 -> mistake += 1
            else:
                mistake += 1
                f_str =f'wrong :('
            data = row[:-1] + [mistake]
            
            # self.entry
            
            if mistake != 0:
                self.result.append(data)
            if mistake == 0:
                self.good += 1

            # 만약 mistake == 0 이면 append하지 않음.
            # self.result.append(data)

            self.label_noti.config(text=f_str)
        else:
            self.entry.delete(0, tk.END)
            
            self.update_labels()
            self.label_kor.config(text='')
            self.label_lev.config(text='')
            self.label_noti.config(text='')
            self.label_radical.config(text='')

    # 입력값 판단
    # answer: csv에 저장된 정답, user_response: 사용자가 입력한 답안
    def check_response(self, answer, user_response):
        # Empty value
        if not user_response:
            return False
        
        # 100% 일치
        if user_response == answer:
            return True
        user_response_splited = user_response.split('|')
        answer_splited = answer.split('|')
        
        # | split 후 개수가 다를 경우 바로 False 반환
        if len(answer_splited) != len(user_response_splited):
            return False
        
        # 정렬 후 일치
        if sorted(user_response_splited) == sorted(answer_splited):
            return True
        
        check = False
        for ans, resp in zip(answer_splited, user_response_splited):
            check = self.check_one(ans=ans, res=resp)
            if not check:
                return False
        return True

    def check_one(self, ans, res):
        # 완전 일치
        if ans == res:
            return True
        
        res_split = res.split()
        # mean+' '+pron 형식이 아닐 경우 바로 False 반환
        if (' ' not in res) or (len(res_split)!=2):
            return False

        # mean, pron split
        ans_h, ans_m = ans.split()
        res_h, res_m = res.split()

        # pron이 틀렸을 때 바로 False 반환
        if ans_m != res_m:
            return False
        
        # 순서 상관 없이 리스트 비교를 위해 / split 후 정렬
        ans_h_sorted = sorted(ans_h.split('/'))
        resp_h_sorted = sorted(res_h.split('/'))
        
        # ans: a/b c
        # res: b/a c
        if (ans_h_sorted == resp_h_sorted) and (ans_m == res_m):
            return True
        
        # ans: a/b c
        # res: (a c) or (b c)
        if len(resp_h_sorted) == 1:
            if (res_h in ans) and (res_m == ans_m):
                return True
            else:
                return False

        return False

    def update_labels(self):
        self.cur_idx += 1
        if self.cur_idx > 0:
            self.entry.grid(row=ROW_ENTRY, columnspan=2)
        if self.cur_idx < len(li):
            row = self.get_data()
            han = row[HANJA_IDX]
            self.label_han.config(text=han)
            self.label_index.config(text=self.cur_idx+1)
        # 마지막에 결과 반환
        else:
            self.show_result()
    
    def show_result(self):
        # 누적 결과 변경
        self.update_accumulated_results()
        
        # 라벨, 엔트리 지우기
        self.remove_elements()
        
        # 점수 계산
        total = len(li)
        # grade = total-len(self.result)
        grade = self.checkgood
        res_txt = f'{grade}개 / {total}개'
        percent = 100*grade//total
        percent_str = f'{percent}%'

        # 라벨 설정 (end, 맞은 개수, 백분율, 걸린 시간)
        label_closing = tk.Label(window, text=closing_remark, font=normal_font)
        label_closing.grid(row=ROW_CLOSING, column=0, columnspan=2)
        label_result = tk.Label(window, text=res_txt, font=normal_font)
        label_result.grid(row=ROW_RESULT, column=0, columnspan=2)
        label_grade = tk.Label(window, text=percent_str, font=normal_font)
        label_grade.grid(row=ROW_GRADE, column=0, columnspan=2)
        elasped = round(time.time() - self.start_time)
        if elasped < 60:
            time_converted = f'{elasped}초'
        else:
            minute = int(elasped//60)
            sec = elasped - (minute*60)
            time_converted = f'{minute}분 {sec}초'
        label_elasped_time = tk.Label(window, text=time_converted, font=normal_font)
        label_elasped_time.grid(row=ROW_TIME, column=0, columnspan=2, rowspan=2)
    
    # hanja, kor, radical, radical_name, stroke_count, level, rep_pron, mistake
    def update_accumulated_results(self):
        with open(DATA_ACCUMULATED, 'w') as f:
            wr = csv.writer(f)
            wr.writerow(['hanja', 'kor', 'radical', 'radical_name', 
                        'stroke_count', 'level', 'rep_pron', 'mistake'])
            for row in self.result:
                wr.writerow(row)
            
            # rest
            for row_res in li_res:
                wr.writerow(row_res)
            
        grade = self.checkgood
        total = len(li)
        percent = 100*grade//total

        print(f'{grade}/{total}, {percent}%')
        print(f'{self.good} :: dobi is free !')
    
    def remove_elements(self):
        self.label_han.grid_remove()
        self.entry.grid_forget()
        self.entry.unbind('<Return>')
        self.label_index.grid_remove()
        self.label_total.grid_remove()
    
    def get_data(self):
        # 8: han, kor, radical, radical_name, stroke_count, level, rep_pron, mistake
        return li[self.cur_idx]


test_base = ReTest()
window.mainloop()