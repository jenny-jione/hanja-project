from gui_base import *
from modules.shuffle import HANJA_IDX, HMS_IDX, LEVEL_IDX
from modules.refactor import refactor_data
import random

class ReadingTest:
    def __init__(self):
        self.click = 0
        self.label_han = tk.Label(window, text=" ", anchor="w", font=large_font)
        self.label_kor = tk.Label(window, text=" ", font=normal_font)
        self.label_lev = tk.Label(window, text=" ", font=normal_font)
        self.label_cnt = tk.Label(window, text=" ", font=normal_font)
        self.label_new = tk.Label(window, text=" ", font=normal_font)
        window.grid_columnconfigure(0, weight=1)  # Column 0 will expand to center-align elements
        window.grid_columnconfigure(1, weight=1)  # Column 1 will also expand for label_new
        self.b_prev = tk.Button(window, text='<',
                                command=lambda s=self: s.update_labels('prv'))
        self.b_next = tk.Button(window, text='>',
                                command=lambda s=self: s.update_labels('nxt'))
        self.label_han.grid(row=0, column=0, columnspan=2)  # Set columnspan to 2 to span both columns
        self.label_kor.grid(row=1, column=0, columnspan=2)
        self.label_lev.grid(row=2, column=0, columnspan=2)
        self.label_cnt.grid(row=3, column=0, sticky="e")  # Use sticky="e" for right-align
        self.label_new.grid(row=3, column=1, sticky="w")  # Use sticky="w" for left-align
        self.b_next.grid(row=4, column=1)
        random.shuffle(li)

    def update_labels(self, dir):
        if dir == 'nxt':
            self.click += 1
        else:
            self.click -= 1
        if self.click == 0:
            self.label_han.config(text='')
            self.label_kor.config(text='press >')
            self.label_lev.config(text='')
            self.label_cnt.config(text='')
            self.label_new.config(text='')
            self.b_prev.grid_forget()
            self.click = 0
        elif self.click <= len(li)*2:
            if self.click % 2 == 1:
                idx = (self.click-1)//2
                self.label_kor.config(text='')
            else:
                idx = self.click // 2 - 1
                kor = li[idx][HMS_IDX]
                self.label_kor.config(text=kor)
            han = li[idx][HANJA_IDX]
            self.label_han.config(text=han)
            level_raw = li[idx][LEVEL_IDX]
            level = refactor_data(level_raw)
            self.label_lev.config(text=level)
            self.label_cnt.config(text=idx+1)
            self.label_new.config(text='/ ' + str(len(li)))
            self.b_prev.grid(row=4, column=0)
        elif self.click > len(li):
            self.label_han.config(text='')
            self.label_kor.config(text=closing_remark)
            self.label_lev.config(text='')
            self.label_cnt.config(text='')
            self.label_new.config(text='')
            self.b_next.grid_forget()
            self.b_prev.grid_forget()


test_base = ReadingTest()
window.mainloop()