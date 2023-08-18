"""
획수 순서로 정렬한 파일 만들기
 가나다순으로는 뒤에 있지만 앞에 있는 한자에 포함되는 한자가 먼저 나오도록 하기.

1. 획수 (stroke count)
2. 부수 (radical)
3. 음(音) (representative pronunciation)
"""
from modules.load import load_all_file_with_radical
from modules.index import HEADER_ROW, STROKE_COUNT, REP_PRON_IDX, RADICAL_NAME_IDX
import csv

rows = load_all_file_with_radical()

sorted_rows = sorted(rows, key = lambda x: (int(x[STROKE_COUNT]), x[RADICAL_NAME_IDX], x[REP_PRON_IDX]))

with open('./data/data_sorted_by_stroke.csv', 'w') as f:
    wr = csv.writer(f)
    wr.writerow(HEADER_ROW)
    for row in sorted_rows:
        wr.writerow(row)