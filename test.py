from modules.load import load_file
from modules.index import *

oldf = load_file('./data/accumulated_results.csv')
newf = load_file('./data/accumulated_results__test.csv')

def make_dict(f: list):
    res_dict = {}
    for row in f[:]:
        hj = row[0]
        miss = row[-1]
        res_dict[hj] = miss
    return res_dict

oldd = make_dict(oldf)
newd = make_dict(newf)

print(len(oldd))
print(len(newd))

# 변동사항
better = 0
worse = 0
for hj, miss in oldd.items():
    search = newd.get(hj)
    if not search:
        print(f'{hj} :: {miss} -> 0')
        better += 1
    else:
        if search > miss:
            print(f'{hj} :: {miss} -> {search} ****')
            worse += 1
        else:
            print(f'{hj} :: {miss} -> {search}')
            better += 1
print(better)
print(worse)