# 한자 단어 독음 테스트 프로그램 구현 (25.7.30)

# gui_word_test.py 와 다른 점: 
# gui_word_test.py: '한자'를 10개 뽑은 후, 해당 한자에 속한 용례를 랜덤으로 하나씩 뽑는다.
# 이 프로그램: 애초에 '단어' 파일에서 10개를 랜덤으로 뽑는다.

import csv
import os
import random
import time
from collections import OrderedDict
from enum import IntEnum, auto

from gui_base import *
from modules.load import load_all_file_with_radical


QUIZ_COUNT = 10

WORD_IDX = 0
READING_IDX = 1
MEANING_IDX = 2


class QuizScreenRow(IntEnum):
    HANJA    = 0        # 한자 단어
    KOR      = auto()   # 단어 음 (정답)
    NOTI     = auto()   # 정오 표시 -> 마지막엔 closing 문구
    INFO     = auto()   # 단어의 각 한자의 훈/음 표시
    MEANING  = auto()   # 정의
    ENTRY    = auto()   # 입력란
    PROGRESS = auto()   # 진행률 ex. 1/10

class ResultScreenRow(IntEnum):
    CLOSING         = 2
    RESULT          = auto()
    GRADE           = auto()
    TIME            = auto()
    TITLE           = auto()
    RESULT_DETAIL   = auto()
    

class HanjaWordTest:
    def __init__(self):
        self.cur_idx = 0
        self.ans = 1
        self.label_han = tk.Label(window, text=" ", anchor="w", font=large_font)
        self.label_kor = tk.Label(window, text=" ", font=normal_font)
        self.label_hanja_info = tk.Label(window, text=" ", font=normal_font)
        self.label_noti = tk.Label(window, text='', font=small_font)
        self.label_index = tk.Label(window, text=" ", font=small_font)
        self.label_total = tk.Label(window, text=" ", font=small_font)
        window.grid_columnconfigure(0, weight=1)  # Column 0 will expand to center-align elements
        window.grid_columnconfigure(1, weight=1)  # Column 1 will also expand for label_new
        self.entry = tk.Entry(window)
        self.entry.bind('<Return>', self.show_text)
        self.label_han.grid(row=QuizScreenRow.HANJA, column=0, columnspan=2)  # Set columnspan to 2 to span both columns
        self.label_kor.grid(row=QuizScreenRow.KOR, column=0, columnspan=2)
        self.label_noti.grid(row=QuizScreenRow.NOTI, columnspan=2)
        self.label_hanja_info.grid(row=QuizScreenRow.INFO, column=0, columnspan=2)
        
        self.msg_meaning = tk.Message(window, text="", width=480, font=small_font)
        self.msg_meaning.grid(row=QuizScreenRow.MEANING, column=0, columnspan=2, padx=10, pady=5)

        self.entry.grid(row=QuizScreenRow.ENTRY, columnspan=2)
        self.label_index.grid(row=QuizScreenRow.PROGRESS, column=0, sticky="e")  # Use sticky="e" for right-align
        self.label_total.grid(row=QuizScreenRow.PROGRESS, column=1, sticky="w")  # Use sticky="w" for left-align

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
    

    def get_word_test_data(self):
        path = './csv/word_data_5_valid.csv'
        quiz_data = []
        # 加減,가감,더하거나 빼는 일. 또는 그렇게 하여 알맞게 맞추는 일.,https://hanja.dict.naver.com/#/search?range=word&query=加減
        with open(path, 'r', encoding='utf-8') as f:
            rdr = csv.reader(f)
            word_data = list(rdr)

        random.shuffle(word_data)
        quiz_data = word_data[:QUIZ_COUNT]
        return quiz_data

    def show_text(self, event):
        self.ans += 1
        # 입력값 변수에 저장
        response = self.entry.get()
        quiz_word, quiz_answer, quiz_meaning = self.get_data()

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
            self.msg_meaning.config(text=quiz_meaning)

        else:
            self.entry.delete(0, tk.END)
            self.update_labels()
            self.label_kor.config(text='')
            self.label_noti.config(text='')
            self.label_hanja_info.config(text='')
            self.msg_meaning.config(text="")


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
            self.entry.grid(row=QuizScreenRow.ENTRY, columnspan=2)
        if self.cur_idx < QUIZ_COUNT:
            han, _, _ = self.get_data()
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
        label_closing.grid(row=ResultScreenRow.CLOSING, column=0, columnspan=2)
        label_result = tk.Label(window, text=res_txt, font=normal_font)
        label_result.grid(row=ResultScreenRow.RESULT, column=0, columnspan=2)
        label_grade = tk.Label(window, text=percent_str, font=normal_font)
        label_grade.grid(row=ResultScreenRow.GRADE, column=0, columnspan=2)
        elasped = round(time.time() - self.start_time)
        if elasped < 60:
            time_converted = f'{elasped}초'
        else:
            minute = int(elasped//60)
            sec = elasped - (minute*60)
            time_converted = f'{minute}분 {sec}초'
        label_elasped_time = tk.Label(window, text=time_converted, font=normal_font)
        label_elasped_time.grid(row=ResultScreenRow.TIME, column=0, columnspan=2, rowspan=1)

        # 출제된 한자 50개 + 맞음/틀림 여부 표시
        hanja_info_list = []
        wrong_word = {row[WORD_IDX] for row in self.result}  # 틀린 단어만 모아둠

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
        self.save_result(hanja_info_text)

        label_hanja_list_title = tk.Label(window, text='[시험 목록]', font=small_font, justify="left")
        label_hanja_list_title.grid(row=ResultScreenRow.TITLE, column=0, columnspan=2, sticky="w")

        label_hanja_list = tk.Label(window, text=hanja_info_text, font=small_font, justify="left", anchor="w")
        label_hanja_list.grid(row=ResultScreenRow.RESULT_DETAIL, column=0, columnspan=2, sticky="w")


    def update_wrong_hanja_csv(self):
        """
        틀린 한자 정보를 기존 CSV와 병합하여 업데이트한다.
        """
        wrong_hanja_file = './word_test_result_wrong_hanja.csv'
        wrong_hanja_dict = OrderedDict()

        # 1. 기존 데이터 읽기
        if os.path.exists(wrong_hanja_file):
            with open(wrong_hanja_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # 헤더 건너뛰기
                for row in reader:
                    hanja, count = row
                    wrong_hanja_dict[hanja] = int(count)

        # 2. 새로 틀린 한자 병합
        for row in self.word_data:
            word = row[WORD_IDX]
            for ch in word:
                if ch in self.wrong_result:
                    # 이미 있던 한자는 삭제 후 맨 뒤로
                    if ch in wrong_hanja_dict:
                        wrong_hanja_dict[ch] += 1
                        wrong_hanja_dict.move_to_end(ch)
                    else:
                        wrong_hanja_dict[ch] = 1  # 새 항목은 기본값 1로 추가됨

        # 3. 파일 전체 덮어쓰기 (순서 보존)
        with open(wrong_hanja_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['한자', '틀린횟수'])
            for hanja, count in wrong_hanja_dict.items():
                writer.writerow([hanja, count])


    def log_test_result(self, text):
        """
        결과 텍스트를 로그 파일에 남긴다.
        """
        result_log_file = './word_test_result.txt'
        separator = '=' * 30
        cur_time = time.localtime()
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", cur_time)

        with open(result_log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[{formatted_time}]\n{separator}\n{text}\n{separator}\n")


    def save_result(self, text: str):
        """
        틀린 한자를 CSV에 저장하고, 결과 로그를 기록한다.
        """
        self.update_wrong_hanja_csv()
        self.log_test_result(text)
        print("result saved.")

    
    def remove_elements(self):
        self.label_han.grid_remove()
        self.entry.grid_forget()
        self.entry.unbind('<Return>')
        self.label_index.grid_remove()
        self.label_total.grid_remove()
    
    def get_data(self):
        # self.word_data 형식: [한자단어, 한국어발음, 단어뜻, url]
        # self.word_data[] = ['練兵', '연병', '군인(軍人)으로서 전투(戰鬪)에 필요(必要)한 여러 가지 동작(動作)이나 작업(作業) 따위를 훈련(訓鍊)함.', url]
        han = self.word_data[self.cur_idx][WORD_IDX]
        kor = self.word_data[self.cur_idx][READING_IDX]
        meaning = self.word_data[self.cur_idx][MEANING_IDX]
        return han, kor, meaning


if __name__ == '__main__':
    test_base = HanjaWordTest()
    window.mainloop()