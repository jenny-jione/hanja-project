import tkinter as tk
from tkinter import font
from gui_base import *


from modules.load import load_file
li = load_file()

from modules.shuffle import HANJA_IDX, HMS_IDX, LEVEL_IDX
click = 0
def update_labels():
    global li, click
    if click < len(li):
        hanja = li[click][HANJA_IDX]
        answer = li[click][HMS_IDX]
        level = li[click][LEVEL_IDX]
        label1.config(text=hanja)
        label2.config(text=answer)
        label_cnt.config(text=str(click))
        label_lv.config(text=level)
        label_new.config(text='/ ' + str(len(li)))
        click += 1
    else:
        label1.config(text='')
        label2.config(text='끝! 수고하셨습니다!!')
        label_lv.config(text='')
        label_cnt.config(text='')
        label_new.config(text='')


label1 = tk.Label(window, text=" ", anchor="w", font=large_font)
label2 = tk.Label(window, text=" ", font=normal_font)
label_lv = tk.Label(window, text=" ", font=normal_font)
label_cnt = tk.Label(window, text=" ", font=normal_font)
label_new = tk.Label(window, text=" ", font=normal_font)

b1 = tk.Button(window, text='다음', command=update_labels)

# Set the column and row configurations for center alignment
window.grid_columnconfigure(0, weight=1)  # Column 0 will expand to center-align elements
window.grid_columnconfigure(1, weight=1)  # Column 1 will also expand for label_new

label1.grid(row=0, column=0, columnspan=2)  # Set columnspan to 2 to span both columns
label2.grid(row=1, column=0, columnspan=2)
label_lv.grid(row=2, column=0, columnspan=2)
label_cnt.grid(row=3, column=0, sticky="e")  # Use sticky="e" for right-align
label_new.grid(row=3, column=1, sticky="w")  # Use sticky="w" for left-align
b1.grid(row=4, column=0, columnspan=2)

window.mainloop()