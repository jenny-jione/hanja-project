# 모양자 crawling (23.10.19)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

from modules.load import load_file
load_data = load_file('./data/data.csv')
data_list = [data[1] for data in load_data]


def get_start_idx():
    with open('./element_complete.csv', 'r') as f:
        rdr = csv.reader(f)
        data = list(rdr)
        return len(data)


def get_link(h: str, driver: webdriver.Chrome):
    try:
        url = f'https://hanja.dict.naver.com/#/search?query={h}'
        driver.get(url)
        time.sleep(0.5)
        div_tag = driver.find_element(By.CLASS_NAME, "hanja_word")
        a_tag = div_tag.find_element(By.TAG_NAME, "a")
        link = a_tag.get_attribute('href')
        return link
    except Exception as e:
        print('====')
        print(e)
        print('====')


def get_raw_data(url: str, driver: webdriver.Chrome):
    driver.get(url)
    time.sleep(0.5)
    div_tag = driver.find_element(By.CLASS_NAME, "entry_infos.my_entry_infos")
    info_item = div_tag.find_elements(By.CLASS_NAME, "info_item")[1]
    desc = info_item.find_element(By.CLASS_NAME, "desc")
    text = desc.text
    return text


if __name__ == "__main__":    
    start_idx = get_start_idx()
    print(f'start_idx: {start_idx}')
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    result = []
    with open('./element.csv', 'a') as f1, open('./element_complete.csv', 'a') as f2:
        wr = csv.writer(f1)
        wr2 = csv.writer(f2)
        for i, han in enumerate(data_list[start_idx:]):
            link = get_link(han, driver)
            text = get_raw_data(link, driver)
            
            elements = text.split(' + ')
            print(f'{start_idx+i}/{len(data_list)}')
            for element in elements:
                split_idx = element.index('(')
                h = element[:split_idx]
                k = element[split_idx+1:-1]
                wr.writerow([han, h, k])
            
            wr2.writerow([han])

    driver.quit()