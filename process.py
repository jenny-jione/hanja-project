import os

def get_filenames(directory):
    txt_files = []
    lvs = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            txt_files.append(filename)
            lv = filename.split('h')[-1].split('.txt')[0]
            lvs.append(lv)
    return lvs

PATH = 'data'
levels = get_filenames(PATH)
levels_sorted = sorted(levels, reverse=True)
print(levels_sorted)


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

print(len(result))


from typing import Tuple
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


import csv
with open(f'./{PATH}/total_processed.csv', 'w') as file:
    wr = csv.writer(file)
    wr.writerow(['level','hanja','rep_h','rep_m','hms(>1)'])
    for tu in result:
        lv, hanja, raw_str = tu[0], tu[1], tu[2]
        hms = get_raw_and_return_each_hm(raw_str)
        
        rep = hms[0]
        all_hms = []
        for hm in hms:
            hm_combo = ' '.join(hm)
            all_hms.append(hm_combo)
        
        line = [lv, hanja] + rep + all_hms
        wr.writerow(line)
