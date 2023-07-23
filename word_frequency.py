# 3급 음 초성 통계
import csv

HEADER_ROW = ['level', 'hanja','mean','pron','hms']
PRON_IDX = HEADER_ROW.index('pron')
FILE_PATH = './data/data.csv'


def load_file():
    with open(FILE_PATH, 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        result = list(rdr)
    return result


def get_chosung(char: str):
    # 한글 한 글자의 십진수 유니코드 = [{(초성)×588}+{(중성)×28}+(종성)]+44032
    BASE_CODE = 44032
    CHOSUNG = 588
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    return CHOSUNG_LIST[(ord(char)-BASE_CODE) // CHOSUNG]

def chosung_frequency_check():
    stat = {}
    with open(FILE_PATH, 'r') as f:
        rdr = csv.reader(f)
        next(rdr)
        datas = list(rdr)
        # prons = [data[PRON_IDX] for data in datas]
        for data in datas:
            pron = data[PRON_IDX]
            pron_chosung = get_chosung(pron)
            stat.setdefault(pron_chosung, 0)
            stat[pron_chosung] += 1
    return stat

def pron_frequency_check(li: list):
    stat = {}
    for data in li:
        pron = data[PRON_IDX]
        stat.setdefault(pron, 0)
        stat[pron] += 1
    return stat


if __name__ == '__main__':
    stat_dict = chosung_frequency_check()
    print(stat_dict)
    for key, value in stat_dict.items():
        valuedivten = value // 10
        print(f'{key}: {"-"*valuedivten}')
    
    h_list = load_file()
    pron_stat_dict = pron_frequency_check(h_list)
    pron_stat_dict_sorted = dict(sorted(pron_stat_dict.items(), reverse=True, key=lambda item: item[1]))

    for key, value in pron_stat_dict_sorted.items():
        if value < 5:
            break
        print(f'{key}: {str(value).zfill(2)} {"-"*value}')
