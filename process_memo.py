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


def get_ab_han():
    with open('./memo_ab_sort.csv', 'r') as f:
        rdr = csv.reader(f)
        result = list(rdr)
    return result


def save_sort_file(data: list):
    with open('./memo_ab_sort.csv', 'w') as f:
        wr = csv.writer(f)
        for row in data:
            wr.writerow(row)


# def check_subset(onerow: list, data: list, idx: int):
#     unique = True
#     for j, row in enumerate(data):
#         if set(onerow).issubset(row):
#             unique = False
#     return unique
        

# TODO: ing !!! unique 1, 0, 2 -> true, false, same
def check_subset(onerow: list, data: list, idx: int):
    unique = True
    for j, row in enumerate(data):
        # if onerow == row:
        #     unique = 2
        if set(onerow).issubset(row):
            unique = False
    return unique


def get_unique_list(data: list):
    data_1 = data[:]
    res = []
    result = []
    print(f'before: {len(data)}')
    for i, row in enumerate(data_1):
        unique = check_subset(row, data[:i]+data[i+1:], i)
        if unique:
            res.append(row)
    
    print(f'after : {len(res)}')
    
    # unique
    for r in res:
        if r not in result:
            result.append(r)
    
    print(f'final: {len(result)}')
    
    return result


if __name__ == "__main__":
    # data_ab = get_ab()
    # save_file(data_ab)
    
    unique_list: list = get_unique_list(get_ab_han())
    # save_sort_file(unique_list)
    