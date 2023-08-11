import csv

def load_all_file():
    with open('./data/data.csv', 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        
        tuple_list = []
        for row in rdr:
            tuple_list.append(tuple(row))
    return tuple_list


def load_today_file():
    with open('./data/data_today_wrong.csv', 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        
        tuple_list = []
        for row in rdr:
            tuple_list.append(tuple(row))
    return tuple_list


def load_file(filename: str):
    with open(filename, 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        
        tuple_list = []
        for row in rdr:
            tuple_list.append(tuple(row))
    return tuple_list


def load_split_file(split_num: int):
    filename_base = './data/review/data_review_split_'
    with open(f'{filename_base}{str(split_num).zfill(2)}.csv', 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        
        tuple_list = []
        for row in rdr:
            tuple_list.append(tuple(row))
    return tuple_list
        

"""
TODO
1. gui에서 범위 선택할 수 있게 하기
    1-1) 혹은 처음에는 더 쉽게, 1번:ㄱ, 2번:ㄴ, 선택
    1-2) 선택한 범위에 맞는 .csv 파일을 가져오기.
2. 한자 검색 기능
3. 현재: 한자, 훈, 음, 급수
    목표: 비슷한 한자, 부수, 단어 예시 등.. 더 보여주기
    근데 이건 크롤링 더 해서 데이터를 쌓아야 할듯!!
"""
