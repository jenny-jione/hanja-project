# 부수 추가 version

from gui_base import *
from modules.index import (
    HANJA_IDX, KOR_IDX, LEVEL_IDX, RADICAL_IDX, RADICAL_NAME_IDX,
    STROKE_COUNT, REP_PRON_IDX
    )
import random
import time
import csv
from modules.load import load_file, load_all_file_with_radical
from collections import defaultdict

# li = load_file('./data/seng.csv')
li = load_all_file_with_radical()
random.shuffle(li)
li = li[:50]

ROW_HANJA = 0
ROW_KOR = 1
ROW_NOTI = ROW_CLOSING = 2
ROW_LEVEL = ROW_RESULT = 3
ROW_RADICAL = ROW_GRADE = 4
ROW_ENTRY = ROW_TIME = 5
ROW_PROGRESS = 6

class ReadingTest:
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
        random.shuffle(li)
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
        
        self.hanja_word_dict = self.load_word_example()
        self.label_hanja_list = tk.Label(window, text="", font=small_font, justify="left", anchor="w")
        self.label_hanja_list.grid(row=ROW_TIME+3, column=0, columnspan=2, sticky="w")

        
        self.result = []
        self.start_time = time.time()

    def load_accumulated_mistakes(self):
        path = './data/accumulated_results.csv'
        data = load_file(path)
        mistake_dict = {}
        for row in data[1:]:  # 헤더 제외
            hanja = row[HANJA_IDX]
            mistake = int(row[-1])  # 마지막 컬럼이 누적 오답 횟수
            mistake_dict[hanja] = mistake
        return mistake_dict
    
    def load_word_example(self):
        path = './example_word.csv'
        hanja_word_dict = defaultdict(list)
        target_h = [x[0] for x in li]

        with open(path, 'r') as f:
            rdr = csv.reader(f)        
            for row in rdr:
                if row[0] in target_h and len(row[1])>1:
                    hanja_word_dict[row[0]].append(row[1:3])
        return hanja_word_dict

    def show_text(self, event):
        self.ans += 1
        # 입력값 변수에 저장
        response = self.entry.get()
        han, kor, radical, radical_name, stroke_count, lev, rep_pron = self.get_data()
        
        if self.ans == 2:
            # 정답 노출
            self.label_kor.config(text=kor)
            self.label_lev.config(text=lev)
            self.label_radical.config(text=f'{radical}:{radical_name}')
            self.ans = 0
            
            # 채점
            check_result = self.check_response(answer=kor, user_response=response)
            if check_result:
                f_str =f'right! :D'
            else:
                f_str =f'wrong :('
                data = [han, kor, radical, radical_name, stroke_count, lev, rep_pron]
                self.result.append(data)
            self.label_noti.config(text=f_str)

            print(f'<{han} {kor}>')
            word_example_list = [f'{row[0]} ({row[1]})' for row in self.hanja_word_dict[han]]
            word_example_text = '\n'.join(word_example_list)
            print(word_example_text)
            self.label_hanja_list.config(text=word_example_text)

        else:
            self.entry.delete(0, tk.END)
            
            self.update_labels()
            self.label_kor.config(text='')
            self.label_lev.config(text='')
            self.label_noti.config(text='')
            self.label_radical.config(text='')
            self.label_hanja_list.config(text='')

    # 입력값 판단
    # answer: csv에 저장된 정답, user_response: 사용자가 입력한 답안
    def check_response(self, answer, user_response):
        # Empty value
        if not user_response:
            return False
        
        # 100% 일치
        if user_response == answer:
            return True
        user_response_splited: list = user_response.split('|')
        answer_splited: list = answer.split('|')
        
        # | split 후 개수가 다를 경우 바로 False 반환
        if len(answer_splited) != len(user_response_splited):
            return False
        
        # 음 기준으로 정렬
        answer_splited.sort(key=lambda x:x[-1])
        user_response_splited.sort(key=lambda x:x[-1])
        
        # 완전일치할 경우 바로 True 반환
        if user_response_splited == answer_splited:
            return True
        
        # 완전일치하지 않을 경우 (/가 들어간 경우)
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
            # else:
            #     return False
        
        if '할' in res_h:
            if (ans_h in res_h) and (res_m == ans_m):
                return True

        return False

    def update_labels(self):
        self.cur_idx += 1
        if self.cur_idx > 0:
            self.entry.grid(row=ROW_ENTRY, columnspan=2)
        if self.cur_idx < len(li):
            han, _, _, _, _, _, _ = self.get_data()
            self.label_han.config(text=han)
            self.label_index.config(text=self.cur_idx+1)
        else:
            self.show_result()
    
    def show_result(self):
        # 결과 저장
        # self.save_result()
        # 누적 결과 저장
        self.save_accumulated_results()
        
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

        # 누적 오답 횟수 로드
        mistake_dict = self.load_accumulated_mistakes()

        # 출제된 한자 50개 + 맞음/틀림 여부 표시
        hanja_info_list = []
        wrong_set = {row[HANJA_IDX] for row in self.result}  # 틀린 한자만 모아둠

        for row in li:
            hanja = row[HANJA_IDX]
            kor = row[KOR_IDX]
            mistake_count = mistake_dict.get(hanja, 0)  # 없으면 0회
            result_str = '❌' if hanja in wrong_set else '✅'
            hanja_info_list.append(f"{result_str} {hanja} / {kor} / 누적: {mistake_count}회")

        hanja_info_text = '\n'.join(hanja_info_list)

        label_hanja_list_title = tk.Label(window, text='[이번 시험에 나온 한자 목록]', font=small_font, justify="left")
        label_hanja_list_title.grid(row=ROW_TIME+2, column=0, columnspan=2, sticky="w")

        label_hanja_list = tk.Label(
            window, text=hanja_info_text, font=small_font, justify="left", anchor="w"
        )
        label_hanja_list.grid(row=ROW_TIME+3, column=0, columnspan=2, sticky="w")

        with open('./data/elasped.csv', 'a') as f1:
            wr = csv.writer(f1)
            # total, grade, percent, elasped, minute, second
            wr.writerow([total, grade, percent, elasped, 
                         int(elasped//60), elasped-((int(elasped//60))*60)])
    
    # TODO 창 닫기 버튼
    
    def save_result(self):
        with open('./data/data_today_wrong.csv', 'w') as f:
            wr = csv.writer(f)
            wr.writerow(['hanja', 'kor', 'radical', 'radical_name', 'stroke_count', 'level', 'rep_pron'])
            for data in self.result:
                wr.writerow(data)
    
    # hanja,kor,radical,radical_name,stroke_count,level,rep_pron,mistake
    def save_accumulated_results(self):
        DATA_ACCUMULATED = './data/accumulated_results.csv'
        datas = load_file(DATA_ACCUMULATED)
        MISTAKE_IDX = -1
        # hanja_dict 만들기
        hanja_dict = {}
        for data in datas:
            hanja = data[0]
            mistake = data[MISTAKE_IDX]
            info = data[:] 
            hanja_dict[hanja] = info
        
        new = 0
        old = 0
        for res in self.result:
            res_hanja = res[0]
            res_info = res
            if res_hanja in hanja_dict:
                old += 1
                mistake = int(hanja_dict[res_hanja][-1]) + 1
                hanja_dict[res_hanja] = res_info + [mistake]
            else:
                new += 1
                hanja_dict[res_hanja] = res_info + ['1']
            
        with open(DATA_ACCUMULATED, 'w') as f:
            wr = csv.writer(f)
            wr.writerow(['hanja', 'kor', 'radical', 'radical_name', 
                        'stroke_count', 'level', 'rep_pron', 'mistake'])
            for k, v in hanja_dict.items():
                wr.writerow(v)
        
        print(f'newly added : {new}')
        print(f'increased   : {old}')
    
    def remove_elements(self):
        self.label_han.grid_remove()
        self.entry.grid_forget()
        self.entry.unbind('<Return>')
        self.label_index.grid_remove()
        self.label_total.grid_remove()
    
    def get_data(self):
        kor = li[self.cur_idx][KOR_IDX]
        han = li[self.cur_idx][HANJA_IDX]
        radical = li[self.cur_idx][RADICAL_IDX]
        radical_name = li[self.cur_idx][RADICAL_NAME_IDX]
        stroke_count = li[self.cur_idx][STROKE_COUNT]
        level = li[self.cur_idx][LEVEL_IDX]
        rep_pron = li[self.cur_idx][REP_PRON_IDX]
        return han, kor, radical, radical_name, stroke_count, level, rep_pron


test_base = ReadingTest()
window.mainloop()