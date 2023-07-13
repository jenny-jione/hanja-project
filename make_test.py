import csv
import random
from datetime import datetime


def load_file():
    with open('./data/data.csv', 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        
        tuple_list = []
        for row in rdr:
            tuple_list.append(tuple(row))
    return tuple_list

# ㄱ-ㅎ(c) or level(l)
# def make(h_list: list, cs: str = None, ce: str = None, ls: str = None, le: str = None):

def get_chosung(char: str):
    BASE_CODE = 44032
    CHOSUNG = 588
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    char_code = ord(char)
    if '가' <= char <= '힣':
        index = (char_code - BASE_CODE) // CHOSUNG
        return CHOSUNG_LIST[index]
    return None
        

def get_h_list(h_list: list, input_char: str = None) -> list:
    # if not chosung:
    #     return h_list
    result = []
    for h in h_list:
        m = h[3]
        chosung = get_chosung(m)
        if chosung == input_char:
            result.append(h)
    return result


def make_question_answer(h_list: list):
    random.shuffle(h_list)
    now = datetime.now()
    fnow = now.strftime('%y%m%d_%H%M%S')
    
    with open(f'./data/test_{fnow}_question.txt', 'w') as f1,\
        open(f'./data/test_{fnow}_answer.txt', 'w') as f2:
            for h in h_list:
                q = h[1]
                a = h[-1]
                f1.write(q + '\n')
                f2.write(a + '\n')
    print(f'{len(h_list)} questions completed.')


if __name__ == '__main__':
    h_list = load_file()
    result = get_h_list(h_list, 'ㄱ')
    make_question_answer(result)
    
    