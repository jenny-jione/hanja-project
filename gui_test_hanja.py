import tkinter as tk
from tkinter import font
from gui_base import *
from time import sleep

# window = tk.Tk()
# window_width = 500
# window_height = 200
# window_pos_x = 1000
# window_pos_y = 800
# window.geometry("{}x{}+{}+{}".format(window_width, window_height, window_pos_x, window_pos_y))
# window.resizable(False, False)
# window.title("Tkinter: 한자 3급 합격 기원🍀")


from modules.load import load_file
li = load_file()

from modules.shuffle import HANJA_IDX, HMS_IDX, LEVEL_IDX
import random
random.shuffle(li)

click = 0
cur_idx = 0
def update_labels():
    global li, click, cur_idx
    click += 1
    if click <= len(li)*2:
        if click % 2 == 1:
            cur_idx = (click-1)//2
            label2.config(text='')
        else:
            cur_idx = click//2 - 1
            label2.config(text=li[cur_idx][HMS_IDX])
        label1.config(text=li[cur_idx][HANJA_IDX])
        label_lv.config(text=li[cur_idx][LEVEL_IDX])
        label_cnt.config(text=cur_idx+1)
        label_new.config(text='/ ' + str(len(li)))
    else:
        label1.config(text='')
        label2.config(text='끝! 수고하셨습니다!!')
        label_lv.config(text='')
        label_cnt.config(text='')
        label_new.config(text='')


LABEL1_FONT_SIZE = 200
LABEL2_FONT_SIZE = 50
label1_font = font.Font(size=LABEL1_FONT_SIZE)
label2_font = font.Font(size=LABEL2_FONT_SIZE)
label1 = tk.Label(window, text=" ", anchor="w", font=label1_font)
label2 = tk.Label(window, text=" ", font=label2_font)
label_lv = tk.Label(window, text=" ")
label_cnt = tk.Label(window, text=" ")
label_new = tk.Label(window, text=" ")

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