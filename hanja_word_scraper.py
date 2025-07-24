# 3급 한자의 단어 크롤링하는 코드 (2025.7.24)

"""
여기에서도 못 잡아낸 한자: 故,隣,隷,阿,獎,準
(\[2025-07-24 ..:..:..\] \[[0-9]+/1817\] Empty: . \([0-9]+ words\))

[2025-07-24 02:45:00] [130/1817] Empty: 故 (0 words)
[2025-07-24 02:46:09] [435/1817] Empty: 隷 (0 words)
[2025-07-24 02:46:20] [481/1817] Empty: 隣 (0 words)
[2025-07-24 02:48:11] [958/1817] Empty: 阿 (0 words)
[2025-07-24 02:49:19] [1254/1817] Empty: 獎 (0 words)
[2025-07-24 02:49:51] [1398/1817] Empty: 準 (0 words)
"""

import csv
import re
import requests
from bs4 import BeautifulSoup, Tag
from datetime import datetime
import os
import unicodedata


PATTERN = re.compile(r'[一-龥]+')
BASE_URL = 'https://namu.wiki/w/'


# 로그 파일 열기
log_file = open('crawl_log.txt', 'a', encoding='utf-8')


def log(msg):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] {msg}")
    log_file.write(f"[{now}] {msg}\n")
    log_file.flush()  # 버퍼 바로 기록


def load_processed_hanja(csv_file):
    processed = set()
    if os.path.exists(csv_file):
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    processed.add(row[0])
    return processed


def find_content_after_span(soup, keyword: str):
    """span id에 주어진 keywords 중 하나라도 포함되면,
    그 span 이후의 LX7a1vUt +C30O3Tm 클래스를 가진 div의 텍스트를
    정규화 및 한자 추출하여 반환
    """
    for span in soup.find_all('span'):
        span_id = span.get('id', '')
        if keyword in span_id:
            for sibling in span.find_parent().next_elements:
                if isinstance(sibling, Tag):
                    classes = set(sibling.get('class', []))
                    if sibling.name == 'div' and classes == {'LX7a1vUt', '+C30O3Tm'}:
                        raw_text = sibling.text.strip()
                        # ✅ 전처리: 정규화 및 한자 추출
                        normalized = unicodedata.normalize('NFKC', raw_text)
                        result = PATTERN.findall(normalized)
                        return result
    return []


def get_info(hanja: str):
    url = BASE_URL + hanja
    
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    keywords = ['단어', '고사성어', '용례', '용법']
    result = []
    for kw in keywords:
        res = find_content_after_span(soup, kw)
        result.extend(res)
    all_terms = list(set(result))

    # 필터링: hanja가 포함된 단어만 유지
    filtered_terms = [term for term in all_terms if hanja in term and len(term)>1]

    return filtered_terms


if __name__ == '__main__':
    log("크롤링 시작")
    start_time = datetime.now()

    # 크롤링할 한자 목록 가져오기
    # target_file은 사용자가 그때그때 변경할 수 있음.
    # target_file = './csv/test.csv'
    target_file = './csv/hanja.csv'
    # target_file = './csv/excluded_hanja.csv'

    with open(target_file, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        # 첫 번째 열의 한자만 추출
        hanja_list = [row[0] for row in rdr if row]
    
    csv_file = f'./csv/word_data.csv'
    processed_hanja = load_processed_hanja(csv_file)
    hanja_no_words = []
    
    with open(csv_file, 'a', encoding='utf-8', newline='') as f:
        wr = csv.writer(f)
        for idx, hanja in enumerate(hanja_list, start=1):
            if hanja in processed_hanja:
                    log(f"[{idx}/{len(hanja_list)}] Skipped: {hanja}")
                    continue
            try:
                res = get_info(hanja)
                if len(res) == 0:
                    hanja_no_words.append([hanja, 'empty'])
                    log(f"[{idx}/{len(hanja_list)}] Empty: {hanja} ({len(res)} words)")
                else:
                    for word in res:
                        wr.writerow([hanja, word])
                    log(f"[{idx}/{len(hanja_list)}] Saved {hanja} ({len(res)} words)")
                f.flush()

            except Exception as e:
                hanja_no_words.append([hanja, 'error'])
                log(f"[{idx}/{len(hanja_list)}] Error: {hanja} - {e}")

    if hanja_no_words:
        with open('./csv/hanja_no_words.csv', 'a', encoding='utf-8', newline='') as zero_f:
            zero_wr = csv.writer(zero_f)
            for hz in hanja_no_words:
                zero_wr.writerow(hz)

    log(f"단어가 없거나 오류가 발생한 한자 개수: {len(hanja_no_words)}개")
    log(f"걸린 시간: {datetime.now() - start_time}")

    log_file.close()