import random
from process_new import HANJA_IDX, HMS_IDX, LEVEL_IDX


def shuffle_list_hanja(h_list: list):
    random.shuffle(h_list)
    for h in h_list:
        lv = h[LEVEL_IDX]
        hanja = h[HANJA_IDX]
        hms = h[HMS_IDX]
        question = lv + ' ' + hanja
        answer = hms