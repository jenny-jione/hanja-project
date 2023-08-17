from gui_base import *
from modules.index import HANJA_IDX, KOR_IDX, LEVEL_IDX, RADICAL_IDX, RADICAL_NAME_IDX
from modules.load import load_all_file
from modules.load import load_all_file_with_radical
# li = load_all_file()
li = load_all_file_with_radical()

MAX_LENGTH = 15

COL_HAN = 0
COL_KOR = 1
COL_LEV = 2
COL_RADICAL = 3


class Search:
    def __init__(self):
        self.cur_idx = 0
        self.ans = 1
        window.grid_columnconfigure(0, weight=1)  # Column 0 will expand to center-align elements
        window.grid_columnconfigure(1, weight=1)  # Column 1 will also expand for label_new
        window.grid_columnconfigure(2, weight=1)  # Column 2 will also expand for label_new
        window.grid_columnconfigure(3, weight=1)  # Column 3 will also expand for label_new
        window.grid_columnconfigure(4, weight=1)  # Column 4 will also expand for label_new
        self.entry = tk.Entry(window)
        self.entry.bind('<Return>', self.search_input)
        
        self.result_labels = []
        self.han_labels = []
        self.kor_labels = []
        self.lev_labels = []
        self.radical_labels = []
        for i in range(MAX_LENGTH):
            label_han = tk.Label(window, font=large_font)
            label_han.grid(row=i, column=COL_HAN)
            label_kor = tk.Label(window, font=normal_font)
            label_kor.grid(row=i, column=COL_KOR, sticky='w')
            label_lev = tk.Label(window, font=small_font)
            label_lev.grid(row=i, column=COL_LEV, sticky='w')
            label_radical = tk.Label(window, font=small_font)
            label_radical.grid(row=i, column=COL_RADICAL, sticky='w')
            self.han_labels.append(label_han)
            self.kor_labels.append(label_kor)
            self.lev_labels.append(label_lev)
            self.radical_labels.append(label_radical)
        self.entry.grid(row=MAX_LENGTH, columnspan=5)
        
        # 검색을 위한 kor(hm) 리스트 생성
        self.kor_list = [row[KOR_IDX] for row in li]
        
        self.result = []
    
    def search_input(self, event):
        self.delete_labels()
        user_input = self.entry.get()
        for idx, data in enumerate(self.kor_list):
            if user_input in data:
                tmp = (
                    li[idx][HANJA_IDX], 
                    li[idx][KOR_IDX], 
                    li[idx][LEVEL_IDX],
                    li[idx][RADICAL_IDX],
                    li[idx][RADICAL_NAME_IDX]
                    )
                self.result.append(tmp)
        print(len(self.result))
        
        length = min(MAX_LENGTH, len(self.result))
        for i in range(length):
            self.han_labels[i].config(text=self.result[i][0])
            self.kor_labels[i].config(text=self.result[i][1])
            self.lev_labels[i].config(text=self.result[i][2])
            radical = f'{self.result[i][3]}({self.result[i][4]})'
            self.radical_labels[i].config(text=radical)
        # entry 입력데이터 지우기
        self.entry.delete(0, tk.END)
        self.result = []
    
    def delete_labels(self):
        for i in range(MAX_LENGTH):
            self.han_labels[i].config(text='')
            self.kor_labels[i].config(text='')
            self.lev_labels[i].config(text='')
            self.radical_labels[i].config(text='')


search = Search()
window.mainloop()