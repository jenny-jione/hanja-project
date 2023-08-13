import csv
from crawling_with_boosoo import get_hanja_info
import os
from dotenv import load_dotenv

load_dotenv()
BASE_BASE_URL = os.getenv('BASE_BASE_URL')


radical_dict = {}
with open('./data/data_with_radical.csv', 'r') as f:
    rdr = csv.reader(f)
    next(rdr)
    for rd in rdr:
        radical = rd[2]
        radical_dict.setdefault(radical, 0)
        radical_dict[radical] += 1
    
    print(len(radical_dict))
    
    radicals = list(radical_dict.keys())

with open('./data/radicals.csv', 'a') as f2:
    wr = csv.writer(f2)
    wr.writerow(['hanja', 'kor', 'radical', 
                         'total_num_of_strokes', 
                         'level'])
        
    urls = [(BASE_BASE_URL+'/w/'+rad) for rad in radicals]
    hanja_infos = []
    for i, url in enumerate(urls[140:]):
        hanja_info: list = get_hanja_info(url)
        print(str(i).zfill(3), hanja_info)
        hanja_infos.append(hanja_info)
        wr.writerow(hanja_info)
