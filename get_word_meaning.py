# word_test_data.csv 파일의 한자 단어 뜻을 네이버 한자사전에서 크롤링하는 코드 (작성일: 2025.06.30)

import csv
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

def get_start_idx(file_path):
    with open(file_path, 'r') as f:
        rdr = csv.reader(f)
        data = list(rdr)
        return len(data)

def wait_means(driver, timeout=5):
    """`.mean` 요소가 최소 2개 생길 때까지 기다려 반환"""
    def _has_two_means(drv):
        elems = drv.find_elements(By.CLASS_NAME, "mean")
        return elems if len(elems) >= 2 else False

    return WebDriverWait(driver, timeout).until(_has_two_means)

def get_meaning(hanja_info: list, driver: webdriver.Chrome):
    # hanja_info: ['家', '家家禮', '가가례']
    url = f'https://hanja.dict.naver.com/#/search?range=word&query={hanja_info[1]}'
    driver.get(url)
    # time.sleep(TIME_SLEEP)
    # class_mean = driver.find_elements(By.CLASS_NAME, "mean")[1]
    # meaning = class_mean.text
    # return hanja_info + [meaning, url]

    try:
        class_mean = wait_means(driver)[1]
        meaning = class_mean.text.strip()
    except TimeoutException:
        # 로딩 실패/구조 변화/차단 등 예외 처리
        meaning = ""
    return hanja_info + [meaning, url]

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

if __name__ == '__main__':
    input_file = './word_test_data.csv'
    output_file = './word_test_data_meaning.csv'

    driver = create_driver()

    with open(input_file, 'r') as f1, open(output_file, 'a', newline='') as f2:
        rdr = csv.reader(f1)
        hanja_word_list = list(rdr)
        start_idx = get_start_idx(output_file)
        print(start_idx)

        wr = csv.writer(f2)

        for i, row in enumerate(hanja_word_list[start_idx:]):
            absolute_idx = start_idx + i

            # 일정 주기마다 드라이버 재시작
            if i > 0 and i % RESTART_INTERVAL == 0:
                logger.info(f'{absolute_idx}개 처리 완료 — 크롬 드라이버 재시작 중...')
                driver.quit()
                driver = create_driver()
                logger.info(f'재시작 완료. 계속 진행 중...')

            data = get_meaning(row, driver)
            wr.writerow(data)
            logger.info(f'{absolute_idx}/{len(hanja_word_list)} {data[1:-1]}')

    driver.quit()