# level3_words.csv 에 없는 한자 찾아내기. (2025.7.21)

from hanja_word_process import load_hanja_chars
import csv

# 한자 리스트 불러오기
hanja_list = load_hanja_chars("./csv/hanja.csv")  # ['愛', '安', ...]

csv_file = './csv/level3_words.csv'
output_file = './csv/excluded_hanja.csv'

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    hanjas = set(row[0] for row in reader if row)  # 첫 번째 열의 한자만 추출
    # level3_words = {row[0] for row in reader}

excluded_hanja = [h for h in hanja_list if h not in hanjas]

with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for h in excluded_hanja:
        writer.writerow([h])

print(f"총 {len(hanjas)}개의 한자가 level3_words.csv에 있습니다.")
print(f"총 {len(hanja_list)}개의 한자 중 {len(excluded_hanja)}개가 level3_words.csv에 없습니다.")
print(f"총 {len(excluded_hanja)}개의 한자가 level3_words.csv에 없습니다. {output_file}에 저장되었습니다.")