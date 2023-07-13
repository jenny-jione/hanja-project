with open('./data/h3.txt', 'r') as f:
    lines = f.readlines()
    h_list = [line.strip() for line in lines]

result = []
for i in range(0, len(h_list), 2):
    if i+1 < len(h_list):
        pair = (3, h_list[i], h_list[i+1])
        result.append(pair)

###
import csv
with open('./data/result.csv', 'w') as f:
    wr = csv.writer(f)
    for res in result:
        wr.writerow(res)