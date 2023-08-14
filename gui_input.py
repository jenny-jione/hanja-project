from gui_base import *
from modules.index import HANJA_IDX, HMS_IDX, LEVEL_IDX
from modules.refactor import refactor_data
import random
import time
from modules.load import load_today_file
li = load_today_file()

class ReadingTest:
    def __init__(self):
        self.cur_idx = 0
        self.ans = 1
        self.label_han = tk.Label(window, text=" ", anchor="w", font=large_font)
        self.label_kor = tk.Label(window, text=" ", font=normal_font)
        self.label_lev = tk.Label(window, text=" ", font=normal_font)
        self.label_index = tk.Label(window, text=" ", font=normal_font)
        self.label_total = tk.Label(window, text=" ", font=normal_font)
        window.grid_columnconfigure(0, weight=1)  # Column 0 will expand to center-align elements
        window.grid_columnconfigure(1, weight=1)  # Column 1 will also expand for label_new
        random.shuffle(li)
        self.entry = tk.Entry(window)
        self.entry.bind('<Return>', self.show_text)
        self.label_han.grid(row=0, column=0, columnspan=2)  # Set columnspan to 2 to span both columns
        self.label_kor.grid(row=1, column=0, columnspan=2)
        self.label_lev.grid(row=2, column=0, columnspan=2)
        self.label_index.grid(row=3, column=0, sticky="e")  # Use sticky="e" for right-align
        self.label_total.grid(row=3, column=1, sticky="w")  # Use sticky="w" for left-align
        self.entry.grid(row=4, columnspan=2)
        
        self.label_han.config(text=li[0][HANJA_IDX])
        self.label_index.config(text=self.cur_idx+1)
        self.label_total.config(text='/ ' + str(len(li)))
        
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
            check_result = self.check_response(answer=kor, user_response=response)
            if check_result:
                f_str =f'right! :: {kor}'
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
            # print(f'not valid input :: {res}, {res_split}')
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
            self.entry.grid(row=4, columnspan=2)
        if self.cur_idx < len(li):
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
        total = len(li)
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
        elasped = round(time.time() - self.start_time)
        if elasped < 60:
            time_converted = f'{elasped}초'
        else:
            minute = int(elasped//60)
            sec = elasped - (minute*60)
            time_converted = f'{minute}분 {sec}초'
        label_elasped_time = tk.Label(window, text=time_converted, font=normal_font)
        label_elasped_time.grid(row=5, column=0, columnspan=2, rowspan=2)
    
    # TODO 창 닫기 버튼
    
    def save_result(self):
        import csv
        with open('./data/data_today_wrong.csv', 'w') as f:
        # with open('./data/wrong_collection.csv', 'a') as f:
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
        kor = li[self.cur_idx][HMS_IDX]
        han = li[self.cur_idx][HANJA_IDX]
        level_raw = li[self.cur_idx][LEVEL_IDX]
        level = refactor_data(level_raw)
        return han, kor, level


test_base = ReadingTest()
window.mainloop()