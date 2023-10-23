import csv
from modules.load import load_file
from modules.index import HEADER_ROW


def get_grade_stats():
    data = load_file('./data/accumulated_results.csv')
    print(type(data))
    print(len(data))

    data_sorted = sorted(data, key=lambda x: int(x[-1]), reverse=True)

    for row in data_sorted[:20]:
        print(row[0], row[-1])


def get_time_stats():
    with open('./data/elasped.csv', 'r') as f:
        rdr = csv.reader(f)
        header = next(rdr)
        print(header)
        data = []
        for row in rdr:
            avg = int(row[header.index('elasped')]) / int(row[header.index('total')])
            data.append(avg)
        print(data)

if __name__ == "__main__":
    # get_grade_stats()
    get_time_stats()