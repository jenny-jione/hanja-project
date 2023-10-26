# memo_ab.csv의 각 row를 stroke_count를 기준으로 정렬 후
# memo_ab_sort.csv에 저장하는 코드
import csv

# 전체에서 han, stroke_count만 가져와 dictionary 생성
with open('./data/data_radicals.csv', 'r') as f:
    rdr = csv.reader(f)
    header = next(rdr)
    
    stroke = {}
    for rd in rdr:
        han = rd[0]
        cnt = int(rd[header.index('stroke_count')])
        stroke[han] = cnt
    
    print(len(stroke))

with open('./memo_ab.csv', 'r') as f:
    rdr = csv.reader(f)
    
    lines = []
    for rd in rdr:
        line = []
        for h in rd:
            line.append((h, stroke[h]))
        line_sort = sorted(line, key=lambda x: x[1])
        lines.append(line_sort)

with open('./memo_ab_sort.csv', 'w') as f:
    wr = csv.writer(f)
    
    for line in lines:
        h = [li[0] for li in line]
        wr.writerow(h)