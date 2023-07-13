import os
from typing import Tuple, List
import csv


PATH = 'data'
HEADER_ROW = ['level','hanja','rep_h','rep_m','hms(>1)']


def get_filenames(directory):
    txt_files = []
    lvs = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            txt_files.append(filename)
            lv = filename.split('h')[-1].split('.txt')[0]
            lvs.append(lv)
    return lvs


def read_all_txt_files_and_get_info(levels_sorted: list):
    result = []
    for lv in levels_sorted:
        with open(f'./{PATH}/h{lv}.txt', 'r') as f:
            lines = f.readlines()
            h_list = [line.strip() for line in lines]

            if '3' in lv:        
                # h, m is in diffrent line     
                for i in range(0, len(h_list), 2):
                    if i+1 < len(h_list):
                        pair = (lv, h_list[i], h_list[i+1])
                    result.append(pair)
            else:
                for hm in h_list:
                    lst = hm.split(' ', 1)
                    lst.insert(0, lv)
                    pair = tuple(lst)
                    result.append(pair)
    return result


def separate_hm(hm: str) -> Tuple[str, str]:
    tmp = hm.split()
    h_raw, m_raw = tmp[:-1], tmp[-1]
    h = ''.join(h_raw)
    m = m_raw.split('(')[0].split(':')[0]
    return h, m


def get_raw_and_return_each_hm(s: str):
    hms = s.split('|')
    
    result = []
    for i, hm in enumerate(hms):
        if i==0:
            h_rep, m_rep = separate_hm(hm)
            result.append([h_rep, m_rep])
        else:
            h, m = separate_hm(hm)
            result.append([h, m])
    return result


# lv, hanja, rep_h, rep_m, all_hms
def make_tuple(h_list: list) -> List[Tuple]:
    result = []
    for line in h_list:
        lv, hanja, raw_str = line
        hms = get_raw_and_return_each_hm(raw_str)
        rep_h, rep_m = hms[0]
        all_hms_list = []
        for hm in hms:
            hm_combo = ' '.join(hm)
            all_hms_list.append(hm_combo)
            all_hms = '|'.join(all_hms_list)
        result.append((lv, hanja, rep_h, rep_m, all_hms))
    return result


def sort_ganadara(h_tuple_list: List[Tuple]) -> List[Tuple]:
    return sorted(h_tuple_list, key=lambda x: x[3])


def save_file(h_tuple_list: List[Tuple]):
    with open(f'./{PATH}/sorted_improved.csv', 'w') as file:
        wr = csv.writer(file)
        wr.writerow(HEADER_ROW)
        for h in h_tuple_list:
            wr.writerow(h)



if __name__ == '__main__':
    levels = get_filenames(PATH)
    levels_sorted = sorted(levels, reverse=True)
    h_list = read_all_txt_files_and_get_info(levels_sorted)
    h_tuple_list = make_tuple(h_list)
    sorted_h_tuple_list = sort_ganadara(h_tuple_list)
    save_file(sorted_h_tuple_list)
