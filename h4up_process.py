with open('./data/h4.txt', 'r') as f:
    lines = f.readlines()
    h_list = [line.strip() for line in lines]

result = []
for hm in h_list:
    lst = hm.split(' ', 1)
    lst.insert(0, 'level')
    pair = tuple(lst)
    result.append(pair)

print(result)