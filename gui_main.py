import tkinter as tk
from time import sleep

window = tk.Tk()
window_width = 100
window_height = 100
window_pos_x = 1800
window_pos_y = 1000
window.geometry("{}x{}+{}+{}".format(window_width, window_height, window_pos_x, window_pos_y))
window.resizable(False, False)
window.title("Tkinter: Test")


from modules.load import load_file
li = load_file()

from modules.shuffle import HANJA_IDX, HMS_IDX, LEVEL_IDX
import random
cur_idx = 0
random.shuffle(li)
li = li[:5]

def update_labels():
    global li, cur_idx
    if cur_idx < len(li):
        hanja = li[cur_idx][HANJA_IDX]
        answer = li[cur_idx][HMS_IDX]
        # label2_text.set(hanja)
        label1.config(text=hanja)
        label2.config(text=answer)
        cur_idx += 1
    else:
        label1.config(text='')
        label2.config(text='-The End-')

label1 = tk.Label(window, text=" ", anchor="w")
label2 = tk.Label(window, text=" ")
# label2_text = tk.StringVar()
# label2_text.set('a')
# label2 = tk.Label(window, textvariable=label2_text)

b1 = tk.Button(window, text='btn', command=update_labels)

label1.pack()
label2.pack()
b1.pack()

window.mainloop()