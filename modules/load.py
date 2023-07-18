import csv

def load_file():
    with open('./data/data_part.csv', 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        
        tuple_list = []
        for row in rdr:
            tuple_list.append(tuple(row))
    return tuple_list