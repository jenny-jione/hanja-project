import csv
from modules.load import load_file
from modules.index import HEADER_ROW

data = load_file('./data/accumulated_results.csv')
print(type(data))
print(len(data))

data_sorted = sorted(data, key=lambda x: int(x[-1]), reverse=True)

for row in data_sorted[:20]:
    print(row[0], row[-1])

# hanja,kor,radical,radical_name,stroke_count,level,rep_pron,mistake
