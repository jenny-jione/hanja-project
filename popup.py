from load import load_file
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
        i = input(question)
        if i == 'q':
            break
        print(answer, '\n')

def shuffle_list_hms(h_list: list):
    random.shuffle(h_list)
    for h in h_list:
        lv = h[LEVEL_IDX]
        hanja = h[HANJA_IDX]
        hms = h[HMS_IDX]
        question = lv + ' ' + hms
        answer = hanja
        i = input(question)
        if i == 'q':
            break
        print(answer, '\n')


if __name__ == '__main__':    
    li = load_file()
    # shuffle_list_hanja(li)
    shuffle_list_hms(li)


