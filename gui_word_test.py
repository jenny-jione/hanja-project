# 한자 단어 독음 테스트 프로그램 구현 (25.6.24)

from gui_base import *
import random
import time
import csv
from modules.load import load_all_file_with_radical
from collections import defaultdict

li = load_all_file_with_radical()
random.shuffle(li)
li = li[:10]

HANJA_IDX = 0
WORD_IDX = 1
READING_IDX = 2

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


        self.word_data = self.get_word_test_data()

        self.label_han.config(text=self.word_data[0][WORD_IDX])
        self.label_index.config(text=self.cur_idx+1)
        self.label_total.config(text='/ ' + str(len(li)))
        
        self.result = []
        self.start_time = time.time()

    # 하나의 한자의 여러 용례 중에 하나 뽑아서 문제 set 만들기
    def get_word_test_data(self):
        path = './word_test_data.csv'
        
        hanja_info_dict = {row[0]: row[1:] for row in li}
        target_h = set(hanja_info_dict.keys())

        hanja_word_dict = defaultdict(list)

        with open(path, 'r') as f:
            rdr = csv.reader(f)        
            for row in rdr:
                if row[0] in target_h:
                    hanja_word_dict[row[0]].append(row[1:3])

        word_data = []
        for hanja, h_word_list in hanja_word_dict.items():
            extra_info = hanja_info_dict.get(hanja, []) 
            word_data.append(([hanja] + random.choice(h_word_list) + list(extra_info)))
        return word_data
        # [hanja, word, kor]

    def show_text(self, event):
        self.ans += 1
        # 입력값 변수에 저장
        response = self.entry.get()
        han, kor = self.get_data()
        
        if self.ans == 2:
            # 정답 노출
            self.label_kor.config(text=kor)
            self.ans = 0
            
            # 채점
            check_result = self.check_response(answer=kor, user_response=response)
            if check_result:
                f_str =f'right! :D'
            else:
                f_str =f'wrong :('
                data = [han, kor]
                self.result.append(data)
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
        if user_response == answer:
            return True
        return False

    def update_labels(self):
        self.cur_idx += 1
        if self.cur_idx > 0:
            self.entry.grid(row=ROW_ENTRY, columnspan=2)
        if self.cur_idx < len(li):
            han, _ = self.get_data()
            self.label_han.config(text=han)
            self.label_index.config(text=self.cur_idx+1)
        else:
            self.show_result()
    
    def show_result(self):
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

        # 출제된 한자 50개 + 맞음/틀림 여부 표시
        hanja_info_list = []
        wrong_set = {row[HANJA_IDX] for row in self.result}  # 틀린 한자만 모아둠
        print(wrong_set)
        for word in self.word_data:
            print(word)

        for row in self.word_data:
            word = row[WORD_IDX]
            reading = row[READING_IDX]
            result_str = '❌' if word in wrong_set else '✅'
            hanja_info_list.append(f"{result_str} {word} / {reading}")

        hanja_info_text = '\n'.join(hanja_info_list)

        label_hanja_list_title = tk.Label(window, text='[시험 목록]', font=small_font, justify="left")
        label_hanja_list_title.grid(row=ROW_TIME+2, column=0, columnspan=2, sticky="w")

        label_hanja_list = tk.Label(
            window, text=hanja_info_text, font=small_font, justify="left", anchor="w"
        )
        label_hanja_list.grid(row=ROW_TIME+3, column=0, columnspan=2, sticky="w")

       
    # TODO 창 닫기 버튼
    # TODO: 
    # 巧言 -> _언 으로 입력했을 경우 (정답: 교언)
    # [교]는 오답처리, [언]은 정답처리 후 오답 한자만 기록하는 기능 만들기
    
    def remove_elements(self):
        self.label_han.grid_remove()
        self.entry.grid_forget()
        self.entry.unbind('<Return>')
        self.label_index.grid_remove()
        self.label_total.grid_remove()
    
    def get_data(self):
        han = self.word_data[self.cur_idx][WORD_IDX]
        kor = self.word_data[self.cur_idx][READING_IDX]
        return han, kor


test_base = ReadingTest()
window.mainloop()