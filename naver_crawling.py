# 네이버 한자사전 크롤링 (2023.10.9)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time


if __name__ == "__main__":
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    hanja='托'
    url=f'https://hanja.dict.naver.com/#/search?range=word&query={hanja}&autoConvert=&shouldSearchOpen=false'
    driver.get(url)
    time.sleep(0.3)

    # 전체 / 단어 / 성어
    # 단어 클릭
    radio_group = driver.find_element(By.CLASS_NAME, "radio_group")
    radio_btns = radio_group.find_elements(By.CLASS_NAME, "item")
    word_btn = radio_btns[1]
    word_btn.click()
    time.sleep(0.3)

    # 예시 단어 수집 (예: 검색한자가 托이면 托가 들어간 예시 단어 n개 수집)
    words_div = driver.find_elements(By.CLASS_NAME, "row")
    for word_row in words_div:
        word_div = word_row.find_element(By.CLASS_NAME, "origin")
        word = word_div.find_element(By.TAG_NAME, "a")
        print(word.text)

        mean_div = word_div.find_element(By.CLASS_NAME, "mean")
        mean = mean_div.text
        print(mean)
        print()
    
    # 예시 성어 수집 (예: 검색한자가 托이면 托가 들어간 예시 성어 n개 수집)



    driver.quit()

