# 네이버 한자사전 크롤링 (2023.10.9)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time

from modules.load import load_file
load_data = load_file('./data/data.csv')
hanja_list = [data[1] for data in load_data]
hanja = hanja_list[400]
print(hanja)
# print(len(hanja_list))


if __name__ == "__main__":
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # hanja='托'
    url=f'https://hanja.dict.naver.com/#/search?range=word&query={hanja}&autoConvert=&shouldSearchOpen=false'
    driver.get(url)
    time.sleep(0.3)

    # 전체 / 단어 / 성어
    radio_group = driver.find_element(By.CLASS_NAME, "radio_group")
    radio_btns = radio_group.find_elements(By.CLASS_NAME, "item")
    # 단어 클릭
    word_btn = radio_btns[1]
    word_btn.click()
    time.sleep(0.3)

    # 예시 단어 수집 (예: 검색한자가 托이면 托가 들어간 예시 단어 n개 수집)
    words_div = driver.find_elements(By.CLASS_NAME, "row")
    for word_row in words_div:
        word_div = word_row.find_element(By.CLASS_NAME, "origin")
        word = word_div.find_element(By.TAG_NAME, "a")
        print(word.text)

        kor_div = word_div.find_element(By.CLASS_NAME, "mean")
        kor = kor_div.text
        print(kor)

        mean_ul = word_row.find_element(By.TAG_NAME, "ul")
        mean_items = mean_ul.find_elements(By.CLASS_NAME, "mean_item")
        # print(len(mean_items))

        for mean_item in mean_items:
            print(mean_item.text)
        print()
    
    # 예시 성어 수집 (예: 검색한자가 托이면 托가 들어간 예시 성어 n개 수집)
    idioms_btn = radio_btns[2]
    idioms_btn.click()
    time.sleep(0.5)

    idioms_div = driver.find_elements(By.CLASS_NAME, "row")
    print(len(idioms_div))
    for idiom_row in idioms_div:
        idiom_div = idiom_row.find_element(By.CLASS_NAME, "origin")
        idiom = idiom_div.find_element(By.TAG_NAME, "a")
        idiom_kor = idiom_div.find_element(By.CLASS_NAME, "mean")
        idiom_mean = idiom_row.find_element(By.CLASS_NAME, "mean_list")


        print(idiom.text, ': ', idiom_kor.text)
        print(idiom_mean.text)
        print()



    driver.quit()

