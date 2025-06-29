# 한자 단어 독음 테스트 프로그램 구현 (25.6.24)

from gui_base import *
import random
import time
import csv
from modules.load import load_all_file_with_radical
from collections import defaultdict


QUIZ_COUNT = 10

HANJA_IDX = 0
WORD_IDX = 1
READING_IDX = 2

ROW_HANJA = 0
ROW_KOR = 1
ROW_NOTI = ROW_CLOSING = 2
ROW_INFO = ROW_RESULT = 3
ROW_GRADE = 4
ROW_ENTRY = ROW_TIME = 5
ROW_PROGRESS = 6

class ReadingTest:
    def __init__(self):
        self.cur_idx = 0
        self.ans = 1
        self.label_han = tk.Label(window, text=" ", anchor="w", font=large_font)
        self.label_kor = tk.Label(window, text=" ", font=normal_font)
        self.label_hanja_info = tk.Label(window, text=" ", font=small_font)
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
        self.label_hanja_info.grid(row=ROW_INFO, column=0, columnspan=2)
        self.entry.grid(row=ROW_ENTRY, columnspan=2)
        self.label_index.grid(row=ROW_PROGRESS, column=0, sticky="e")  # Use sticky="e" for right-align
        self.label_total.grid(row=ROW_PROGRESS, column=1, sticky="w")  # Use sticky="w" for left-align

        # 1817개 전체 한자 data
        self.hanja_data = self.get_hanja_data()
        # 1817개 한자 dictionary
        self.hanja_info_dict = self.make_hanja_info_dict()
        self.word_data = self.get_word_test_data()
        self.wrong_count = 0 # 문제 오답 개수

        self.label_han.config(text=self.word_data[0][WORD_IDX])
        self.label_index.config(text=self.cur_idx+1)
        self.label_total.config(text='/ ' + str(QUIZ_COUNT))
        
        self.result = [] # 오답 단어 저장용 리스트 (한 단어 단위)
        self.wrong_result = set() # 오답 한자 저장용 set (한글자 단위)
        self.start_time = time.time()

    # 전체 한자 데이터 리스트 가져오는 함수
    def get_hanja_data(self):
        return load_all_file_with_radical()
    
    # 전체 한자 데이터에서 dictionary 만들기
    def make_hanja_info_dict(self):
        return {row[0]: row[1:] for row in self.hanja_data}

    # 하나의 한자의 여러 용례 중에 하나 뽑아서 문제 set 만들기
    """
    output:
    word_data
        [hanja, 용례 랜덤, extra_info]
        ...
        ['稀', '稀貴', '희귀', '稀', '드물 희', '禾', '12획', '준3급', '3ii', '희']
    """
    def get_word_test_data(self):
        path = './word_test_data.csv'

        # quiz_data = 전체 한자 데이터(self.hanja_data) 중 QUIZ_COUNT개 만큼 뽑은 리스트
        random.shuffle(self.hanja_data)
        quiz_data = self.hanja_data[:QUIZ_COUNT]

        target_h = [q[0] for q in quiz_data]

        # word_test_data.csv에서 해당 한자의 용례 1개 랜덤으로 뽑기
        hanja_word_dict = defaultdict(list)
        with open(path, 'r') as f:
            rdr = csv.reader(f)        
            for row in rdr:
                if row[0] in target_h:
                    hanja_word_dict[row[0]].append(row[1:3])

        word_data = []
        for hanja, h_word_list in hanja_word_dict.items():
            extra_info = self.hanja_info_dict.get(hanja, [])
            word_data.append(([hanja] + random.choice(h_word_list) + list(extra_info)))
        return word_data


    def show_text(self, event):
        self.ans += 1
        # 입력값 변수에 저장
        response = self.entry.get()
        quiz_word, quiz_answer = self.get_data()

        if self.ans == 2:
            # 정답 노출
            self.label_kor.config(text=quiz_answer)
            self.ans = 0
            
            # 채점
            wrong_idx_result = self.check_response(answer=quiz_answer, user_response=response)
            if wrong_idx_result:
                f_str =f'wrong :('
                for idx in wrong_idx_result:
                    self.wrong_result.add(quiz_word[idx])
                data = [quiz_word, quiz_answer]
                self.result.append(data)
                self.wrong_count += 1
            else:
                f_str =f'right! :D'
                
            self.label_noti.config(text=f_str)

            # 단어의 각 한자 훈음 공개 - 武:호반 무 / 士:선비 사
            han_kor = []
            for hanja in quiz_word:
                kor = self.hanja_info_dict[hanja][0]
                han_kor.append(f'{hanja}:{kor}')
            hanja_info_str = ' / '.join(han_kor)
            self.label_hanja_info.config(text=hanja_info_str)


        else:
            self.entry.delete(0, tk.END)
            
            self.update_labels()
            self.label_kor.config(text='')
            self.label_noti.config(text='')
            self.label_hanja_info.config(text='')

    # 입력값 판단
    # answer: csv에 저장된 정답, user_response: 사용자가 입력한 답안
    def check_response(self, answer: str, user_response: str):
        answer = answer.strip()
        resp = user_response.strip()

        if len(resp) < len(answer):
            resp += '_' * (len(answer)-len(resp))
        else:
            resp = resp[:len(answer)]    

        res = list(resp)
        ans = list(answer)

        wrong_idx = []

        for i, (res_ch, ans_ch) in enumerate(zip(res, ans)):
            if res_ch != ans_ch:
                wrong_idx.append(i)
        
        return wrong_idx

    def update_labels(self):
        self.cur_idx += 1
        if self.cur_idx > 0:
            self.entry.grid(row=ROW_ENTRY, columnspan=2)
        if self.cur_idx < QUIZ_COUNT:
            han, _ = self.get_data()
            self.label_han.config(text=han)
            self.label_index.config(text=self.cur_idx+1)
        else:
            self.show_result()
    
    def show_result(self):
        # 라벨, 엔트리 지우기
        self.remove_elements()
        
        # 점수 계산
        total = QUIZ_COUNT
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
        wrong_word = {row[HANJA_IDX] for row in self.result}  # 틀린 단어만 모아둠

        for row in self.word_data:
            word = row[WORD_IDX]
            reading = row[READING_IDX]
            result_str = '❌' if word in wrong_word else '✅'
            ch_result = ''
            for ch in word:
                ch_result += f'{ch}:{self.hanja_info_dict[ch][0]}'
                if ch in self.wrong_result:
                    ch_result += '(X) '
                else:
                    ch_result += '(O) '
            hanja_info_list.append(f"{result_str} {word} / {reading} / {ch_result}")

        hanja_info_text = '\n'.join(hanja_info_list)
        print(hanja_info_text)

        label_hanja_list_title = tk.Label(window, text='[시험 목록]', font=small_font, justify="left")
        label_hanja_list_title.grid(row=ROW_TIME+2, column=0, columnspan=2, sticky="w")

        label_hanja_list = tk.Label(
            window, text=hanja_info_text, font=small_font, justify="left", anchor="w"
        )
        label_hanja_list.grid(row=ROW_TIME+3, column=0, columnspan=2, sticky="w")

       
    # TODO: 창 닫기 버튼 기능 구현

    # TODO: 일부만 맞춘 경우, 정답 처리된 한자는 제외하고 오답 한자만 오답 CSV에 기록하기
    # 예: '巧言'에 대해 사용자가 '_언'을 입력한 경우 (정답: 교언)
    # → [언]은 정답 처리되고, [교]만 오답으로 간주하여 기록
    
    # TODO: word_test_data.csv 내용을 자주 쓰는 단어 중심으로 교체할 것
    # 기존 단어 예: 可,十丈水裏可知一丈人裏不可知,십장수리가지 일장인리불가지
    # 변경 단어 예: 可,可能,가능
    # 뜻도 추가하기.
    # 예: 可,可能,가능,할 수 있거나 될 수 있음.
    
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