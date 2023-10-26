# memo_ab.txt -> memo_ab.csv 형식 변환해서 저장하는 코드
# memo_ab.txt 형식      memo_ab.csv 형식
# kor1 vs kor2 ..       han1,han2
import csv

with open('./data/data_radicals.csv', 'r') as f:
    rdr = csv.reader(f)
    header = next(rdr)
    # print(header)
    h_dict = {}
    for rd in rdr:
        key = rd[1]
        value = rd
        h_dict.setdefault(key, []).append(value)


def get_ex():
    with open('./memo_ex.txt', 'r') as f:
        lines_ex = f.read().splitlines()

    nxt = input()
    idx = 0
    while(True):
        nxt = input()
        if nxt == 'q' or idx == len(lines_ex):
            break
        kor = lines_ex[idx]
        if h_dict.get(kor):
            print(kor, h_dict[kor])
        idx += 1


def get_h(kor):
    return h_dict.get(kor)


def get_ab():
    result = []
    cnt = 0
    with open('./memo_ab.txt', 'r') as f:
        lines_ab = f.read().splitlines()
        for i, line in enumerate(lines_ab):
            ab = line.split(' vs ')
            data_ab = []
            for kor in ab:
                info = get_h(kor)
                if info:
                    for el in info:
                        data_ab.append(el[0])
                else:
                    cnt += 1
                    print(f'{i+1} {kor}')
            result.append(data_ab)
        print(f'memo_ab len: {len(lines_ab)}')
        print(cnt)
    print(len(result))
    return result


def save_file(data: list):
    with open('./memo_ab.csv', 'w') as f:
        wr = csv.writer(f)
        for row in data:
            wr.writerow(row)
        

if __name__ == "__main__":
    data_ab = get_ab()
    save_file(data_ab)