# 크롤링된 한자 데이터 후처리 (2025.7.19)
# word_data_nw.csv -> word_data_nw_processed.csv 
#
# 원본 데이터 예시 (중복 및 포함 관계로 비슷한 단어들이 많음):
# 감격(感激)
# 감격성(感激性)
# 감격적(感激的)
#
# 격동(激動)
# 격동기(激動期)
# 격동적(激動的)
#
# 격려(激勵)
# 격려금(激勵金)
# 격려문(激勵文)
# 격려사(激勵辭)
# 격려전(激勵電)
#
# 원하는 결과:
# 감격(感激)
# 격동(激動)
# 격려(激勵)
#
# => 포함되는 단어는 제거하여 가장 기본 단어만 남김

import csv
from datetime import datetime

log_file = open('crawl_processed_log.txt', 'a', encoding='utf-8')

def log(msg):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] {msg}")

file_name = 'word_data_nw__test'

csv_file = './word_data_nw.csv'
output_file = './word_data_nw_processed.csv'

start_time = datetime.now()
log(f"처리 시작: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

with open(csv_file, 'r', encoding='utf-8') as f, \
     open(output_file, 'w', encoding='utf-8', newline='') as f2:

    rdr = csv.reader(f)
    wr = csv.writer(f2)
    data = list(rdr)

    total = len(data)
    prev_hanja = None
    base_words = set()

    skip_count = 0
    write_count = 0

    for i, (hanja, word) in enumerate(data):
        if hanja != prev_hanja:
            base_words = set()
            prev_hanja = hanja

        # base_words에 포함된 단어가 현재 word에 포함되어 있으면 중복 처리(스킵)
        if any(base_word in word for base_word in base_words):
            skip_count += 1
            continue

        base_words.add(word)
        wr.writerow([hanja, word])
        write_count += 1

end_time = datetime.now()
elapsed = end_time - start_time

log(f"처리 종료: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
log(f"걸린 시간: {elapsed}")
log(f"전체 단어 수: {total}")
log(f"중복 제거된 단어 수: {skip_count}")
log(f"최종 저장된 단어 수: {write_count}")

