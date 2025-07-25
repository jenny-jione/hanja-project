# word_test_data.csv 파일의 한자 단어 뜻을 네이버 한자사전에서 크롤링하는 코드 (작성일: 2025.06.30)

import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from logger import Logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = Logger()

RESTART_INTERVAL = 500  # 드라이버 재시작 주기


def load_processed_word(csv_file):
    processed = set()
    if os.path.exists(csv_file):
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    processed.add(row[1])
    return processed


def wait_means(driver, timeout=5):
    """`.mean` 요소가 최소 2개 생길 때까지 기다려 반환"""
    def _has_two_means(drv):
        elems = drv.find_elements(By.CLASS_NAME, "mean")
        return elems if len(elems) >= 2 else False

    return WebDriverWait(driver, timeout).until(_has_two_means)


def get_meaning(word: str, driver: webdriver.Chrome):
    url = f'{URL}={word}'
    driver.get(url)

    try:
        mean_elements = wait_means(driver)

        reading = mean_elements[0].text.strip()
        meaning = mean_elements[1].text.strip()
    except TimeoutException:
        # 로딩 실패/구조 변화/차단 등 예외 처리
        reading, meaning = "", ""
    return reading, meaning, url


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

if __name__ == '__main__':
    file_name = 'level3_words'
    input_file = f'./csv/{file_name}.csv'
    output_file = f'./csv/{file_name}_meaning.csv'

    driver = create_driver()

    with open(input_file, 'r') as f1, open(output_file, 'a', newline='', encoding='utf-8') as f2:
        rdr = csv.reader(f1)
        hanja_word_list = list(rdr)

        processed_word = load_processed_word(output_file)

        wr = csv.writer(f2)

        for i, (hanja, word) in enumerate(hanja_word_list, start=1):
            if word in processed_word:
                continue

            # 일정 주기마다 드라이버 재시작
            if i > 0 and i % RESTART_INTERVAL == 0:
                logger.info(f'{absolute_idx}개 처리 완료 — 크롬 드라이버 재시작 중...')
                driver.quit()
                driver = create_driver()
                logger.info(f'재시작 완료. 계속 진행 중...')

            reading, meaning, url = get_meaning(word, driver)
            row = [hanja, word, reading, meaning, url]
            wr.writerow(row)
            logger.info(f'{i}/{len(hanja_word_list)} {row[1:-1]}')

    driver.quit()