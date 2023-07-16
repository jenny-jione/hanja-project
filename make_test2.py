# .csv 파일을 읽어서 순서만 랜덤으로 변경한 후 새로운 시험 파일로 만드는 코드 (훈 only, 음 only)
import csv
import random
from datetime import datetime
from process_new import HANJA_IDX, HMS_IDX, LEVEL_IDX

PATH_TEST = './data/test'


def load_file():
    with open('./data/data_part.csv', 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        
        tuple_list = []
        for row in rdr:
            tuple_list.append(tuple(row))
    return tuple_list


def write_line(level: str, s: str):
     print()
     return level + ' ' + s + '\n'


def make_question_answer(h_list: list):
    random.shuffle(h_list)
    now = datetime.now()
    fnow = now.strftime('%y%m%d_%H%M%S')
    with open(f'{PATH_TEST}/{fnow}_question.txt', 'w') as f1,\
        open(f'{PATH_TEST}/{fnow}_answer.txt', 'w') as f2:
            for h in h_list:
                lv = h[LEVEL_IDX]
                q = h[HANJA_IDX]
                a = h[HMS_IDX]
                f1.write(write_line(lv, q))
                f2.write(write_line(lv, a))
    print(f'{len(h_list)} questions completed.')


if __name__ == '__main__':
    h_list = load_file()
    make_question_answer(h_list)