import tkinter as tk
from time import sleep

window = tk.Tk()
window_width = 100
window_height = 120
window_pos_x = 1800
window_pos_y = 1000
window.geometry("{}x{}+{}+{}".format(window_width, window_height, window_pos_x, window_pos_y))
window.resizable(False, False)
window.title("Tkinter: Test")


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
            # label2.config(text=li[cur_idx][HMS_IDX])
            label2.config(text=li[cur_idx][HANJA_IDX])
        # label1.config(text=li[cur_idx][HANJA_IDX])
        label1.config(text=li[cur_idx][HMS_IDX])
        label_lv.config(text=li[cur_idx][LEVEL_IDX])
    else:
        label1.config(text='')
        label2.config(text='End')
        label_lv.config(text='')
        label_cnt.config(text='')


label1 = tk.Label(window, text=" ", anchor="w")
label2 = tk.Label(window, text=" ")
label_lv = tk.Label(window, text=" ")
label_cnt = tk.Label(window, text=" ")

b1 = tk.Button(window, text='btn', command=update_labels)

label1.pack()
label2.pack()
label_lv.pack()
label_cnt.pack()
b1.pack()

window.mainloop()