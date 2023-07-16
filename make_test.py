# 입력한 초성에 해당하는 운을 가진 한자만 시험지 만드는 코드: ㄱ -> 가, 각, 고, ...
import csv
import random
from datetime import datetime
from process_new import HANJA_IDX, HMS_IDX, PRON_IDX

PATH_TEST = './data/test'


def load_file():
    with open('./data/data.csv', 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        
        tuple_list = []
        for row in rdr:
            tuple_list.append(tuple(row))
    return tuple_list

# 주어진 한글 1글자의 초성 얻기
# TODO: 파라미터 validation 검사를 해야 할까?
def get_chosung(char: str):
    BASE_CODE = 44032
    CHOSUNG = 588
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    char_code = ord(char)
    if '가' <= char <= '힣':
        index = (char_code - BASE_CODE) // CHOSUNG
        return CHOSUNG_LIST[index]
    return None
        
# 파라미터로 들어온 초성에 해당하는 모든 데이터 반환 (ex: ㄱ->가, 각, ...)
# TODO: 1. 초성 범위 검색도 가능하게, 2. lv로도 검색 가능하게
def get_h_list(h_list: list, input_char: str = None) -> list:
    # if not chosung:
    #     return h_list
    result = []
    for h in h_list:
        pron = h[PRON_IDX]
        chosung = get_chosung(pron)
        if chosung == input_char:
            result.append(h)
    return result


def make_question_answer(h_list: list, test_char: str):
    random.shuffle(h_list)
    now = datetime.now()
    fnow = now.strftime('%y%m%d_%H%M%S')
    with open(f'{PATH_TEST}/{test_char}_{fnow}_question.txt', 'w') as f1,\
        open(f'{PATH_TEST}/{test_char}_{fnow}_answer.txt', 'w') as f2:
            for h in h_list:
                q = h[HANJA_IDX]
                a = h[HMS_IDX]
                f1.write(q + '\n')
                f2.write(a + '\n')
    print(f'{len(h_list)} questions completed.')


if __name__ == '__main__':
    h_list = load_file()
    test_char = 'ㄱ'
    result = get_h_list(h_list, test_char)
    make_question_answer(result, test_char)