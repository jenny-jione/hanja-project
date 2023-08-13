# 3급 범위의 모든 한자와 훈/음을 가져오는 코드
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import csv
import time
import random

load_dotenv()
BASE_BASE_URL = os.getenv('BASE_BASE_URL')


#### 링크 저장을 위한 함수들 ####
def get_urls() -> list:
    load_dotenv()
    base_url = os.getenv('BASE_URL')
    url_list = ['URL_3', 'URL_3II', 'URL_4', 'URL_4II']
    urls = [base_url + '/' + os.getenv(url) for url in url_list]
    urls.insert(0, base_url)
    return urls


# 한자 개별 링크 가져오기
def get_hanja_link(url: str):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    result = []
    # 모든 <h3> 태그 추출
    h3_tags = soup.find_all('h3')

    # h3 태그 다음에 오는 div 태그 추출
    for h3 in h3_tags:
        div = h3.find_next('div')
        # td: 하나의 셀
        td_tags = div.find_all('td')
        for td in td_tags:
            div = td.find('div')
            # a 태그가 2개 이상인 경우
            #  몇번째에 href가 있는지 특정할 수 없으므로
            #  for문 돌면서 확인해야 함
            a_tags = div.find_all('a')
            for a_tag in a_tags:
                href_candidate = a_tag.get('href')
                if not href_candidate:
                    continue
                if '/w' in href_candidate:
                    href = href_candidate
                    break
            link = BASE_BASE_URL + href
            text = div.text.strip()
            if text:
                hanja, kor = text[0], text[2:]
                result.append([hanja, kor, link])
    return result


LINK = './data/link.csv'
# 한자, 훈 음, 링크
def save_link(infos: list):
    with open(LINK, 'r') as f1, open(LINK, 'a') as f2:
        rdr = csv.reader(f1)
        rows_count = len(list(rdr))
        wr = csv.writer(f2)
        if rows_count == 0:
            wr.writerow(['hanja', 'kor', 'link'])
        for info in infos:
            wr.writerow(info)
    print(f'{len(infos)} links were saved.')

##################################################################
##################################################################


### 실제 한자 정보 저장을 위한 함수들 ####
# 한자 개별 페이지에서 한자, 훈, 음, 부수, 획수, 어문회 급수 가져오기
def get_hanja_info(url: str):
    headers = {
        "Cookie": "Grids=searchGrid0#+XLNDeLVrCPqqnqAbPager]bEdSangpyoName]]+A]bSangpumryu]-b-b-bIqSbIbIbAdDuL9JcpPanel+DdistinctCount]DgroupCode]GImageUrl]BcDChulwonNo]GSangpyoName]HeESangpyoEng]FSangpumryu]WeGYusagunCode]QcGChulwonin]kFChulwonNoFormat]9ERegisterNo]FRegisterDate]kEGonggoNo]GLastAppName]Ib7DaeriinvStatusGcETrialInfo]GExpireDate]9++; marksearch_user_id_cookie=haeyul; marksearch_user_password_cookie=13611!; JSESSIONID=F3C92D1C652C68D96BEB2F3FD2802053; locale=ko; OptanonConsent=isIABGlobal=false&datestamp=Thu+Aug+25+2022+13%3A44%3A36+GMT%2B0900+(%ED%95%9C%EA%B5%AD+%ED%91%9C%EC%A4%80%EC%8B%9C)&version=6.31.0&hosts=&consentId=7e961f1a-79e4-4bd9-9733-6322a7839dad&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1&AwaitingReconsent=false&geolocation=KR%3B41; OptanonAlertBoxClosed=2022-08-25T04:44:36.726Z; JSESSIONID=BF39C6D4F146EC8CD2F22793E8A98643",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Authorization": "Basic aGFleXVsOjEzNjExIQ==",
    }
    response = requests.get(url, headers=headers)
    # response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    # ing.. 여기 하는 중 !! 테이블이 여러개 있는 경우 에러난당 으앙
    #  => 이상한게 개발자 모드로 class 이름 확인하면 M0yX6Oub _bbdeec84e8cf6318a1e68d0dbd8b5f97 라고 나오는데,
    #  soup으로 get('class')로 얻어서 보면 wiki-table 이라고 나옴... 이유가 뭘까..? 바뀔 수 있대.. ㄷ
    table_tags = soup.find_all('table')
    for table_tag in table_tags:
        tbody = table_tag.find('tbody')
        tr_tags = tbody.find_all('tr')
        if len(tr_tags) == 11:
            tr_1, tr_2 = tr_tags[1], tr_tags[2]
            td_1_cnt, td_2_cnt = len(tr_1.find_all('td')), len(tr_2.find_all('td'))
            if (td_1_cnt == 4) and (td_2_cnt == 4):
                """
                tr.0 : 한자, 훈, 음
                tr.1 : 부수, 획수
                tr.2 : 어문회 급수
                """
                # tr.0 : 한자, 훈, 음
                tr_0 = tr_tags[0]
                tr0txt = tr_0.text
                hanja, kor = tr0txt[0], tr0txt[1:]

                # tr.1 : 부수, 획수
                tr_1 = tr_tags[1]
                tds = tr_1.find_all('td')
                # 부수 및 나머지 획수
                td_radical = tds[1]
                td_text: str = td_radical.text
                radical, num_of_strokes = td_text.replace(' ', '').split(',')
                # 총 획수
                td_stroke = tds[-1]
                total_num_of_strokes: str = td_stroke.text

                # tr.2 : 어문회 급수
                tr_2 = tr_tags[2]
                td_level = tr_2.find_all('td')[-1]
                level = td_level.text

                return [hanja, kor, radical, total_num_of_strokes, level]


def get_link_from_file():
    with open(LINK, 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        rows = list(rdr)
        result = [row[-1] for row in rows]
        return result


# 크롤링할 때.. 계속 트래픽때문에 막혀서 중간에 끊어져서
#  다음에 다시 할 때 자동으로 어디까지 했는지 확인용
def get_index():
    with open('./data/boosoo.csv', 'r') as f:
        rdr = csv.reader(f)
        rows = list(rdr)
        cnt = len(rows)
        print(len(rows))
        if cnt == 0:
            return 0
        else:
            return cnt - 1


if __name__ == '__main__':
    # urls = get_urls()
    # for url in urls:
    #     print(url)
    #     res = get_hanja_link(url)
    #     save_link(res)

    links: list = get_link_from_file()
    start_index = get_index()

    hanja_infos = []
    with open('./data/boosoo.csv', 'a') as file:
        wr = csv.writer(file)
        if start_index == 0:
            wr.writerow(['hanja', 'kor', 'radical', 
                         'total_num_of_strokes', 
                         'level'])
        for i, link in enumerate(links[start_index:]):
            hanja_info: list = get_hanja_info(link)
            print(str(i+start_index+1).zfill(3), hanja_info)
            hanja_infos.append(hanja_info)
            wr.writerow(hanja_info)
            if (i+start_index+1) % 10 == 0:
                print('break time..')
                sleep_time = round(random.uniform(1, 2), 3)  # moderate
                time.sleep(sleep_time)
