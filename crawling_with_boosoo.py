# 3급 범위의 모든 한자와 훈/음을 가져오는 코드

import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import urllib.parse


def get_urls() -> list:
    load_dotenv()
    base_url = os.getenv('BASE_URL')
    url_list = ['URL_3', 'URL_3II', 'URL_4', 'URL_4II']
    urls = [base_url + os.getenv(url) for url in url_list]
    return urls

# def get_info_5to8(url: str):
def get_info_5to8():
    result = []
    
    load_dotenv()
    url = os.getenv('BASE_URL')
    base_base_url = os.getenv('BASE_BASE_URL')
    response = requests.get(url)
    html_content = response.content
    
    soup = BeautifulSoup(html_content, 'html.parser')

    # 모든 <h3> 태그 추출
    h3_tags = soup.find_all('h3')
    
    nooo = 0
    # h3 태그 다음에 오는 div 태그 추출
    for h3 in h3_tags:
        div = h3.find_next('div')
        # td: 하나의 셀
        td_tags = div.find_all('td')
        for td in td_tags:
            div = td.find('div')
            a = div.find('a')
            href = a.get('href')
            if href:
                link = base_base_url+href
            else:
                link = 'None'
                nooo += 1
                print(div)
            text = div.text.strip()
            if text:
                hanja, hm = text[0], text[1:]
                result.append([hanja, hm, link])
    print(nooo)
    return result
    

def get_info(url: str):
    result = []

    # requests를 사용하여 웹 페이지의 소스 코드 가져오기
    response = requests.get(url)
    html_content = response.content

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(html_content, 'html.parser')

    # 모든 <h3> 태그 추출
    h3_tags = soup.find_all('h3')

    # h3 태그 다음에 오는 div 태그 추출
    for h3 in h3_tags:
        # print(h3.text)
        div = h3.find_next('div')
        # td: 하나의 셀
        td_tags = div.find_all('td')
        for td in td_tags:
            div = td.find('div')
            text = div.text.strip()
            if text:
                hanja, hm = text[0], text[1:]
                result.append([hanja, hm])
    return result


def unicode_to_hangul(unicode_str: str):
    decoded_str = urllib.parse.unquote(unicode_str)
    return decoded_str

# 준3급 -> 3ii, 4급 -> 4
def convert_rank(input_str: str):
    input_str = input_str.strip('급')
    if '준' in input_str:
        input_str = input_str.strip('준') + 'ii'
    return input_str


def save_file(level: str, h_list: list):
    with open(f'./data/txt_wb/h{level}.txt', 'w') as f:
        for line in h_list:
            f.write(' '.join(line) + '\n')
    level__ = level.ljust(3, '_')
    print(f'level {level__}:{len(h_list)} completed.')


if __name__ == '__main__':
    # urls = get_urls()
    # for url in urls:
    #     res = get_info(url)
    #     hangul = unicode_to_hangul(url.split('/')[-1])
    #     print(hangul, len(res))
    #     # level = convert_rank(hangul)
    #     # save_file(level, res)
    
    res = get_info_5to8()
    print(len(res))