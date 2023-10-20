# update element_dict to include itself (23.10.20)
import csv

from modules.load import load_file
load_data = load_file('./data/data.csv')
data_list = [data[1] for data in load_data]


if __name__ == "__main__":    
    # element_dict, unique_dict create
    with open('./element.csv', 'r') as f:
        rdr = csv.reader(f)
        header = next(rdr)
        unique_dict = {}
        element_dict = {}
        rows = list(rdr)
        for row in rows:
            h = row[0]
            element = row[1]
            kor = row[-1]
            element_dict.setdefault(h, {})
            element_dict[h].setdefault(element, '')
            element_dict[h][element] = kor
            
            unique_dict.setdefault(element, '')
            unique_dict[element] = kor
    
    for data in data_list:
        itself = unique_dict.get(data)
        if itself:
            element_dict[data][data] = itself
    
    print(header)
    # update element.csv -> element_new.csv (include itself)
    cnt = 0
    with open('./element_new.csv', 'w') as f:
        wr = csv.writer(f)
        wr.writerow(header)
        for k, v in element_dict.items():
            h = k
            for element, kor in v.items():
                wr.writerow([h, element, kor])
                cnt += 1
    
    print(cnt)
