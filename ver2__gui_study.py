import tkinter as tk
from ver2__gui_base import *
from modules.index import HANJA_IDX, KOR_IDX, LEVEL_IDX, RADICAL_IDX, RADICAL_NAME_IDX

ROW_HANJA = 0
ROW_KOR = 1
ROW_LEVEL = 2
ROW_RADICAL = 3
ROW_BUTTON = 4
ROW_PROGRESS = 5

class Study:
    def __init__(self):
        self.click = 0
        self.label_han = tk.Label(window, text=" ", anchor="w", font=large_font)
        self.label_kor = tk.Label(window, text=" ", font=normal_font)
        self.label_radical = tk.Label(window, text=" ", font=small_font)
        self.label_lev = tk.Label(window, text=" ", font=normal_font)
        self.label_progress = tk.Label(window, text=" ", font=normal_font)
        self.label_total = tk.Label(window, text=" ", font=normal_font)
        # Set the column and row configurations for center alignment
        window.grid_columnconfigure(0, weight=1)  # Column 0 will expand to center-align elements
        window.grid_columnconfigure(1, weight=1)  # Column 1 will also expand for label_new
        self.b_prev = tk.Button(window, text='<',
                                command=lambda s=self: s.update_labels('prv'))
        self.button_next = tk.Button(window, text='>',
                                command=lambda s=self: s.update_labels('nxt'))
        self.label_han.grid(row=ROW_HANJA, column=0, columnspan=2)  # Set columnspan to 2 to span both columns
        self.label_kor.grid(row=ROW_KOR, column=0, columnspan=2)
        self.label_lev.grid(row=ROW_LEVEL, column=0, columnspan=2)
        self.label_radical.grid(row=ROW_RADICAL, column=0, columnspan=2)
        self.button_next.grid(row=ROW_BUTTON, column=1)
        self.label_progress.grid(row=ROW_PROGRESS, column=0, sticky="e")  # Use sticky="e" for right-align
        self.label_total.grid(row=ROW_PROGRESS, column=1, sticky="w")  # Use sticky="w" for left-align
        
    def update_labels(self, dir):
        if dir == 'nxt':
            self.click += 1
        else:
            self.click -= 1
        if self.click == 0:
            self.label_han.config(text='')
            self.label_kor.config(text='press >')
            self.label_lev.config(text='')
            self.label_radical.config(text='')
            self.label_progress.config(text='')
            self.label_total.config(text='')
            self.b_prev.grid_forget()
            self.click = 0
        elif self.click <= len(li):
            idx = self.click - 1
            hanja = li[idx][HANJA_IDX]
            kor = li[idx][KOR_IDX]
            level = li[idx][LEVEL_IDX]
            radical = li[idx][RADICAL_IDX]
            radical_name = li[idx][RADICAL_NAME_IDX]
            self.label_han.config(text=hanja)
            self.label_kor.config(text=kor)
            self.label_progress.config(text=str(self.click))
            self.label_lev.config(text=level)
            self.label_radical.config(text=f'{radical}({radical_name})')
            self.label_total.config(text='/ ' + str(len(li)))
            self.b_prev.grid(row=4, column=0)
        elif self.click > len(li):
            self.label_han.config(text='')
            self.label_kor.config(text=closing_remark)
            self.label_lev.config(text='')
            self.label_radical.config(text='')
            self.label_progress.config(text='')
            self.label_total.config(text='')
            self.button_next.grid_forget()
            self.b_prev.grid_forget()

study = Study()
window.mainloop()