"""
radicals.csv + data_with_radical.csv 합쳐서 새로 저장하기
hanja,kor,stroke_count,radical,level,level_sort,rep_pron
"""
import csv

# radicals.csv에서 radical_dict 생성
# hanja, kor, radical, total_num_of_strokes, level
radical_dict = {}
with open('./data/radicals.csv', 'r') as f1:
    rdr = csv.reader(f1)
    next(rdr)
    rows = list(rdr)
    for row in rows:
        radical = row[0]
        radical_name = row[1]
        # 구분자 ', ' --> '|' 로 변경
        radical_dict[radical] = radical_name.replace(', ', '|')
    print(len(radical_dict))


# data.csv에서 kor_dict 생성
kor_dict = {}
with open('./data/data.csv', 'r') as f:
    rdr = csv.reader(f)
    next(rdr)
    rows = list(rdr)
    for row in rows:
        hanja = row[1]
        kor = row[-1]
        kor_dict[hanja] = kor

print(len(kor_dict))

    
# data_with_radical.csv에서 한줄씩 읽으며
# hanja, kor, radical, total_num_of_strokes, level, level_sort, sort_key
#   radical_dict에서 radical_name 매칭하기
#   kor_dict에서 kor 매칭하기
# infos: info = hanja, kor, radical, radical_name, stroke_count, level, rep_pron
infos = []
with open('./data/data_with_radical.csv', 'r') as f2:
    rdr2 = csv.reader(f2)
    next(rdr2)
    rows2 = list(rdr2)
    for row in rows2:
        hanja = row[0]
        radical = row[2]
        radical_name = radical_dict[radical]
        kor = kor_dict[hanja]
        # '10획' 처럼 문자열이었기 때문에 '획' 제거한 후 int로 변환하는 과정 필요.
        stroke_count = int(row[3].strip('획'))
        level = row[4]
        rep_pron = row[-1]
        info = [hanja, kor, radical, radical_name, stroke_count, level, rep_pron]
        infos.append(info)


# 정렬
# 1. rep_pron
# 2. stroke_count
from modules.index import HEADER_ROW, REP_PRON_IDX, STROKE_COUNT
infos.sort(key = lambda x: (x[REP_PRON_IDX], x[STROKE_COUNT]))


# 새로운 csv 파일 생성 (컬럼 8개)
# hanja, kor, radical, radical_name, stroke_count, level, rep_pron
with open('./data/data_radicals.csv', 'w') as f3:
    wr = csv.writer(f3)
    wr.writerow(HEADER_ROW)
    for info in infos:
        wr.writerow(info)
