"""
boosoo.csv 정렬 -> data_with_radical.csv 생성
boosoo.csv에서 대표 음(rep_pron) 가져오기
정렬
 - 1) rep_pron 기준 오름차순 (가나다순)
 - 2) 획순 기준 오름차순
"""
import csv

# 훈 음 주어지면 정렬을 위한 대표 음(representative pronunciation) 반환
def get_representative_pronunciation(kor: str):
    return kor[-1]

def convert_level(input_str: str):
    input_str = input_str.strip('급')
    if '준' in input_str:
        input_str = input_str.strip('준') + 'ii'
    else:
        input_str += '__'
    return input_str

with open('./data/boosoo.csv', 'r') as f:
    rdr = csv.reader(f)
    next(rdr)
    
    HEADER_ROW = ['hanja','kor','radical','total_num_of_strokes','level']
    HANJA_IDX = HEADER_ROW.index('hanja')
    KOR_IDX = HEADER_ROW.index('kor')
    RADICAL_IDX = HEADER_ROW.index('radical')
    NUM_OF_STROKES_IDX = HEADER_ROW.index('total_num_of_strokes')
    LEVEL_IDX = HEADER_ROW.index('level')

    rows = list(rdr)
    with open('./data/data_with_radical.csv', 'w') as f2:
        wr = csv.writer(f2)
        wr.writerow(['hanja', 'kor', 'radical', 
                     'total_num_of_strokes', 
                     'level', 
                     'level_sort', 'rep_pron'
                     ])
        result = []
        for row in rows:
            hanja = row[HANJA_IDX]
            kor = row[KOR_IDX]
            radical = row[RADICAL_IDX]
            strokes = row[NUM_OF_STROKES_IDX]
            level = row[LEVEL_IDX]
            level_sort = convert_level(level)

            kors_splited = kor.split(',')
            kors = [k.strip() for k in kors_splited]
            rep_pron = get_representative_pronunciation(kors[0])
            new_kor = '|'.join(kors)
            hanja_info = [
                hanja, new_kor, radical,
                strokes,
                level,
                level_sort, rep_pron
            ]
            result.append(hanja_info)

        sorted_result = sorted(result, key = lambda x: (x[-1], x[3]))
        for data in sorted_result:
            wr.writerow(data)
