# 3급 한자의 용례 한자만 크롤링하는 코드 (2025.7.19)

import csv
import re
import requests
from bs4 import BeautifulSoup, Tag
from datetime import datetime
import os

from gui_word_test import ReadingTest

PATTERN = re.compile(r'\(([^)]+)\)')
BASE_URL = 'https://namu.wiki/w/'

# 로그 파일 열기
log_file = open('crawl_log.txt', 'a', encoding='utf-8')

def log(msg):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] {msg}")
    log_file.write(f"[{now}] {msg}\n")
    log_file.flush()  # 버퍼 바로 기록

# 이미 처리한 한자 불러오기
def load_processed_hanja(csv_file):
    processed = set()
    if os.path.exists(csv_file):
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    processed.add(row[0])
    return processed

def get_info(hanja: str):
    url = BASE_URL + hanja
    log(f"Requesting: {url}")
    result = []
    
    # requests를 사용하여 웹 페이지의 소스 코드 가져오기
    response = requests.get(url)
    html_content = response.content

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(html_content, 'html.parser')

    # UBV9xAVx ZxJhBjZZ 추출하다가 id="용례"인 span이 있으면 거기서 멈춤.
    for div in soup.find_all('div', class_='UBV9xAVx ZxJhBjZZ'):
        span = div.find('span', id='용례')
        if span:
            break

    # span 이후에 나오는 모든 형제 요소들 탐색
    for sibling in span.find_parent().next_elements:
        if isinstance(sibling, Tag):
            if sibling.name == 'div' and set(sibling.get('class', [])) == {'LX7a1vUt', '+C30O3Tm'}:
                raw_text = sibling.text.strip()

                # 괄호 안 내용만 캡처 
                # 가객(佳客): 반갑고 귀한 손님가구(佳句): 잘 지은 글귀, 시문 따위의 좋은 글귀
                # 佳客, 佳句, ..
                all_inside = PATTERN.findall(raw_text)
                result = [s for s in all_inside if not re.search(r'[가-힣]', s)]
                break

    return result


if __name__ == '__main__':
    test = ReadingTest()
    hanja_data = test.get_hanja_data()
    hanja_list = [hd[0] for hd in hanja_data]
    
    csv_file = './word_data_nw.csv'
    processed_hanja = load_processed_hanja(csv_file)
    
    with open(csv_file, 'a', encoding='utf-8', newline='') as f:
        wr = csv.writer(f)
        for idx, hanja in enumerate(hanja_list, start=1):
            if hanja in processed_hanja:
                    log(f"[{idx}/{len(hanja_list)}] Skipped: {hanja}")
                    continue
            
            try:
                res = get_info(hanja)
                for word in res:
                    wr.writerow([hanja, word])
                f.flush()
                log(f"[{idx}/{len(hanja_list)}] Saved {hanja} ({len(res)} words)")

            except Exception as e:
                log(f"[{idx}/{len(hanja_list)}] Error: {hanja} - {e}")
