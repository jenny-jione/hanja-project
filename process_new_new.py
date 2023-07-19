import os
from typing import Tuple, List
import csv


PATH_DATA = './data'
PATH_TXT = './data/txt'
HEADER_ROW = ['level', 'hanja','mean','pron','hms']
HANJA_IDX = HEADER_ROW.index('hanja')
MEAN_IDX = HEADER_ROW.index('mean')
PRON_IDX = HEADER_ROW.index('pron')
HMS_IDX = HEADER_ROW.index('hms')
LEVEL_IDX = HEADER_ROW.index('level')


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
        with open(f'{PATH_TXT}/h{lv}.txt', 'r') as f:
            lines = f.readlines()
            h_list = [line.strip() for line in lines]

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
    # m = m_raw.split('(')[0].split(':')[0].split('[')[0]
    m = m_raw.split('[')[0]
    return h, m


def get_raw_and_return_each_hm(s: str):
    hms = s.split('|')
    
    result = []
    for hm in hms:
        h, m_raw = separate_hm(hm)
        result.append([h, m_raw])
    return result


# lv, hanja, mean, pron, all_hms
def make_tuple(h_list: list) -> List[Tuple]:
    result = []
    for line in h_list:
        lv, hanja, raw_str = line
        hms = get_raw_and_return_each_hm(raw_str)
        mean, pron_raw = hms[0]
        all_hms_list = []
        for hm in hms:
            hm_combo = ' '.join(hm)
            all_hms_list.append(hm_combo)
            all_hms = '|'.join(all_hms_list)
        # result.append((hanja, mean, pron, all_hms, lv))
        # TODO: HEADER_ROW에 따라 자동으로 바뀌게 만들기 => 완료.
        li = ['', '', '', '', '']
        li[HANJA_IDX] = hanja
        li[MEAN_IDX] = mean
        li[PRON_IDX] = pron_raw.split('(')[0].split(':')[0]
        li[HMS_IDX] = all_hms
        li[LEVEL_IDX] = lv.ljust(3, '_')
        result.append(li)
    return result


def sort_ganadara(h_tuple_list: List[Tuple]) -> List[Tuple]:
    return sorted(h_tuple_list, key=lambda x: x[PRON_IDX])


def save_file(h_tuple_list: List[Tuple]):
    with open(f'{PATH_DATA}/data_sound_ver2.csv', 'w') as file:
        wr = csv.writer(file)
        wr.writerow(HEADER_ROW)
        for h in h_tuple_list:
            wr.writerow(h)



if __name__ == '__main__':
    levels = get_filenames(PATH_TXT)
    levels_sorted = sorted(levels, reverse=True)
    h_list = read_all_txt_files_and_get_info(levels_sorted)
    h_tuple_list = make_tuple(h_list)
    sorted_h_tuple_list = sort_ganadara(h_tuple_list)
    save_file(sorted_h_tuple_list)
