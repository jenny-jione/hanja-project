from modules.load import load_file__new
from modules.refactor import refactor_data
# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('-t', '-type', dest='type', action='store')
# args = parser.parse_args()

import random

class Test:
    def __init__(self):
        self.datas = load_file__new()
    
    def study(self):
        for i, data in enumerate(self.datas):
            hanja = data['hanja']
            kor = data['kor']
            lev = refactor_data(data['level'])
            print(f'{str(i+1).zfill(2)} / {len(self.datas)}')
            print(lev)
            print('\t\t', hanja)
            print('\t\t', kor)
            print()
            input()
    
    def read(self):
        grade = 0
        for i, data in enumerate(self.datas):
            hanja = data['hanja']
            kor = data['kor']
            lev = refactor_data(data['level'])
            print(f'[{str(i+1).zfill(2)}/{len(self.datas)}]{lev}')
            print(hanja)
            response = input()
            if response == kor:
                grade += 1
                print('right!')
            else:
                print('wrong!', kor)
            
            print()
        print(f'your grade : {grade}/{len(self.datas)}')
          
    
    # def shuffle(self):
    #     return random.shuffle(self.datas[:])


if __name__ == '__main__':
    test = Test()
    # if args.type == 'study':
    #     test.study()
    study_type = input('study, read, write: \n')
    if study_type == 'study':
        test.study()
    elif study_type == 'read':
        test.read()
    # elif type == 'write':
    #     test.
    else:
        print('invalid input.')