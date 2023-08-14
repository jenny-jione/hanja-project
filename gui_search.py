from gui_base import *
from modules.index import HANJA_IDX, HMS_IDX, LEVEL_IDX
from modules.load import load_all_file
from modules.refactor import refactor_data
li = load_all_file()

MAX_LENGTH = 10

class Search:
    def __init__(self):
        self.cur_idx = 0
        self.ans = 1
        window.grid_columnconfigure(0, weight=1)  # Column 0 will expand to center-align elements
        window.grid_columnconfigure(1, weight=1)  # Column 1 will also expand for label_new
        window.grid_columnconfigure(2, weight=1)  # Column 2 will also expand for label_new
        self.entry = tk.Entry(window)
        self.entry.bind('<Return>', self.search_input)
        
        self.result_labels = []
        self.han_labels = []
        self.kor_labels = []
        self.lev_labels = []
        for i in range(MAX_LENGTH):
            han_label = tk.Label(window, font=large_font)
            han_label.grid(row=i, column=0)
            kor_label = tk.Label(window, font=normal_font)
            kor_label.grid(row=i, column=1)
            lev_label = tk.Label(window, font=normal_font)
            lev_label.grid(row=i, column=2)
            self.han_labels.append(han_label)
            self.kor_labels.append(kor_label)
            self.lev_labels.append(lev_label)
        self.entry.grid(row=MAX_LENGTH, columnspan=3)
        
        # 검색을 위한 hm 리스트 생성
        self.hm_list = [row[HMS_IDX] for row in li]
        
        self.result = []
    
    def search_input(self, event):
        self.delete_labels()
        user_input = self.entry.get()
        for idx, data in enumerate(self.hm_list):
            if user_input in data:
                tmp = (li[idx][HANJA_IDX], 
                       li[idx][HMS_IDX], 
                       refactor_data(li[idx][LEVEL_IDX]))
                self.result.append(tmp)
        print(len(self.result))
        
        length = min(MAX_LENGTH, len(self.result))
        for i in range(length):
            self.han_labels[i].config(text=self.result[i][0])
            self.kor_labels[i].config(text=self.result[i][1])
            self.lev_labels[i].config(text=self.result[i][2])
        # entry 입력데이터 지우기
        self.entry.delete(0, tk.END)
        self.result = []
    
    def delete_labels(self):
        for i in range(MAX_LENGTH):
            self.han_labels[i].config(text='')
            self.kor_labels[i].config(text='')
            self.lev_labels[i].config(text='')


search = Search()
window.mainloop()