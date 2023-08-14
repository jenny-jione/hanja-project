import csv
import random
from modules.load import load_file
from modules.index import HEADER_ROW

FILE_PATH = './data/data_review.csv'

def split_list(li: list, chunk: int):
    total_count = len(li)
    num = total_count // chunk
    if total_count % chunk != 0:
        num += 1
    for i in range(num):
        start_idx = i*chunk
        end_idx = (i+1)*chunk
        print(f'{start_idx}:{end_idx}')
        sub_li = li[start_idx:end_idx]
        create_sub_file(sub_li, i)


def create_sub_file(li: list, idx: int):
    with open(f'./data/review/data_review_split_{str(idx+1).zfill(2)}.csv', 'w') as f:
        wr = csv.writer(f)
        wr.writerow(HEADER_ROW)
        for row in li:
            wr.writerow(row)


if __name__ == '__main__':
    li = load_file(FILE_PATH)
    random.shuffle(li)
    split_list(li, 100)