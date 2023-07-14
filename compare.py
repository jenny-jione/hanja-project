## 2개의 csv 파일의 내용을 비교하여 동일한지 검사하는 코드.

import csv

def compare_csv(csv_file1, csv_file2):
    with open(csv_file1, 'r') as file1, open(csv_file2, 'r') as file2:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)
        
        for row1, row2 in zip(reader1, reader2):
            if row1 != row2:
                return False
        
        # check if both readers have reached the end of the file
        if any(reader1) or any(reader2):
            return False
    return True

csv_file1 = './data/data2.csv'
csv_file2 = './data/data.csv'

result = compare_csv(csv_file1, csv_file2)

if result:
    print('The two CSV files are identical.')
else:
    print('The two CSV files are not identical.')