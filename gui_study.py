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
        click += 1
    else:
        label1.config(text='')
        label2.config(text='-The End-')
        label_cnt.config(text='')
        label_lv.config(text='')


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