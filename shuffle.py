# .csv 파일을 읽어서 랜덤으로 변경한 후 (lv,훈,음) & (음,훈,lv) 파일 만들기
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


def write_line(level: str, li: list):
    sub_str = '\t\t\t\t\t\t\t\t'.join(li)
    return level + '  ' + sub_str + '\n'
    # TODO: 훈음이 아무리 길어도 정렬해서 출력할 수 있게 하기
    # sub_str = f"{li[0].ljust(10, ' ')} {li[1].rjust(10, ' ')} \n"
    # return level + ' ' + sub_str


def make_question_answer(h_list: list):
    random.shuffle(h_list)
    now = datetime.now()
    fnow = now.strftime('%y%m%d')
    with open(f'{PATH_TEST}/{fnow}_hm.txt', 'w') as f1,\
        open(f'{PATH_TEST}/{fnow}_mh.txt', 'w') as f2:
            for h in h_list:
                lv = h[LEVEL_IDX]
                q = h[HANJA_IDX]
                a = h[HMS_IDX]
                f1.write(write_line(lv, [q, a]))
                f2.write(write_line(lv, [a, q]))
    print(f'{len(h_list)} questions completed.')


if __name__ == '__main__':
    h_list = load_file()
    make_question_answer(h_list)