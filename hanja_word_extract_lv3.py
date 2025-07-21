# hanja_word_new_processed.csv 에서 
# 두번째 열의 단어의 모든 글자가 3급 한자인 경우만 추출하여 
# 새 파일에 저장하는 코드. (작성일: 2025.7.21)

import csv
from gui_word_test import ReadingTest

input_file = './word_data_new_processed.csv'
output_file = './csv/level3_words.csv'
exclude_file = './csv/excluded_words.csv'

# 3급 한자 단어 목록
test = ReadingTest()
hanja_data = test.get_hanja_data()
hanja_list = [h[0] for h in hanja_data]

with open(input_file, 'r', encoding='utf-8') as f, \
     open(output_file, 'w', encoding='utf-8', newline='') as f2, \
     open(exclude_file, 'w', encoding='utf-8', newline='') as f3:

    rdr = csv.reader(f)
    wr = csv.writer(f2)
    wr_excluded = csv.writer(f3)

    for row in rdr:
        if len(row) < 2:
            print(row, "열이 부족하여 건너뜁니다.")
            continue  # skip rows with insufficient columns
        hanja, word = row[0], row[1]
        
        if any(ch not in hanja_list for ch in word):
            wr_excluded.writerow([hanja, word])
            continue  # skip if any character in word is not in the hanja list
        
        wr.writerow([hanja, word])

print(f"3급 한자 단어 추출 완료. {output_file}에 저장됨.")
# 이 코드는 word_data_new_processed.csv 파일에서 3급 한자 단어만 추출하여 level3_words.csv 파일에 저장합니다.
# 각 단어가 3급 한자에 포함되는지 확인하고, 포함되지 않는 단어는 건너뜁니다.
# 이 코드를 실행하면 level3_words.csv 파일이 생성되며, 이 파일에는 3급 한자 단어만 포함됩니다.
# 이 파일은 이후 다른 작업에 사용될 수 있습니다.