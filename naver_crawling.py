# 네이버 한자사전 크롤링 (2023.10.9)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from logger import Logger
import csv
import time

logger = Logger()

from modules.load import load_file
load_data = load_file('./data/data.csv')
hanja_list = [data[1] for data in load_data]
# hanja = hanja_list[400]
TIME_SLEEP = 0.3


def get_start_idx():
    with open('./example_complete.csv', 'r') as f:
        rdr = csv.reader(f)
        data = list(rdr)
        return len(data)


def get_data(hanja: str, driver: webdriver.Chrome):
    url=f'https://hanja.dict.naver.com/#/search?range=word&query={hanja}&autoConvert=&shouldSearchOpen=false'
    driver.get(url)
    time.sleep(TIME_SLEEP)

    # 전체 / 단어 / 성어
    radio_group = driver.find_element(By.CLASS_NAME, "radio_group")
    radio_btns = radio_group.find_elements(By.CLASS_NAME, "item")
    # 단어 클릭
    word_btn = radio_btns[1]
    word_btn.click()
    time.sleep(TIME_SLEEP)

    # 예시 단어 수집 (예: 검색한자가 托이면 托가 들어간 예시 단어 n개 수집)
    words_div = driver.find_elements(By.CLASS_NAME, "row")
    result = []
    for word_row in words_div:
        word_div = word_row.find_element(By.CLASS_NAME, "origin")
        a_tag = word_div.find_element(By.TAG_NAME, "a")
        word = a_tag.text
        link = a_tag.get_attribute('href')
        # print('link:', link)

        kor_div = word_div.find_element(By.CLASS_NAME, "mean")
        kor = kor_div.text
        # print(kor)
        
        # print(hanja, word, kor, link)
        result.append([hanja, word, kor, link])

        # mean_ul = word_row.find_element(By.TAG_NAME, "ul")
        # mean_items = mean_ul.find_elements(By.CLASS_NAME, "mean_item")
        # print(len(mean_items))

        # for mean_item in mean_items:
        #     print(mean_item.text)
        # print()
    return result
    

    # # 예시 성어 수집 (예: 검색한자가 托이면 托가 들어간 예시 성어 n개 수집)
    # idioms_btn = radio_btns[2]
    # idioms_btn.click()
    # time.sleep(0.5)

    # idioms_div = driver.find_elements(By.CLASS_NAME, "row")
    # # print(len(idioms_div))
    # for idiom_row in idioms_div:
    #     origin_div = idiom_row.find_element(By.CLASS_NAME, "origin")
    #     a_tag = origin_div.find_element(By.TAG_NAME, "a")
    #     idiom = a_tag.text
    #     idiom_kor_div = origin_div.find_element(By.CLASS_NAME, "mean")
    #     idiom_kor = idiom_kor_div.text
    #     idiom_mean = idiom_row.find_element(By.CLASS_NAME, "mean_list")

    #     print(idiom, idiom_kor)


if __name__ == "__main__":
    start_idx = get_start_idx()
    print(f'start_idx: {start_idx}')
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # with open('./example_word.csv', 'a') as f1, open('./example_complete.csv', 'a') as f2:
    #     wr = csv.writer(f1)
    #     wr2 = csv.writer(f2)
    #     for i, hanja in enumerate(hanja_list[start_idx:]):
    #         try:
    #             rows = get_data(hanja, driver)
    #             for row in rows:
    #                 wr.writerow(row)
    #             wr2.writerow([hanja])
    #         except Exception as e:
    #             logger.error(f'{start_idx+i}/{len(hanja_list)} {hanja} {e}') 
    #             print('b', i)
    #             i -= 1
    #             print('a', i)
    #         logger.info(f'{start_idx+i}/{len(hanja_list)}')
    
    with open('./example_word.csv', 'a') as f1, open('./example_complete.csv', 'a') as f2:
        wr = csv.writer(f1)
        wr2 = csv.writer(f2)
        for i, hanja in enumerate(hanja_list[start_idx:]):
            rows = get_data(hanja, driver)
            for row in rows:
                wr.writerow(row)
            wr2.writerow([hanja])
            logger.info(f'{start_idx+i}/{len(hanja_list)} {hanja}')
        
    driver.quit()

