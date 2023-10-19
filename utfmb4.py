import csv

with open('./element.csv', 'r') as f:
    rdr = csv.reader(f)
    next(rdr)
    for row in rdr:
        u = len(row[1].encode('utf8'))
        if u >= 4:
            print(row, u)