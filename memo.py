import tkinter as tk
from tkinter import font

MAX_LENGTH = 1

def window_geometry():
    window.geometry("{}x{}+{}+{}".format(width, height, pos_x, pos_y))

window = tk.Tk()
width = 100
height = 50
pos_x = 1800
pos_y = 1100
window_title = ' '
window_geometry()
transparent = 0.3
window.wait_visibility(window)
window.wm_attributes("-alpha", transparent)   

window.title(window_title)

class Memo:
    def __init__(self):
        window.grid_columnconfigure(0, weight=1)  # Column 0 will expand to center-align elements
        self.entry = tk.Entry(window)
        self.entry.bind('<Return>', self.enter_input)
        self.label = tk.Label(window)
        self.entry.grid(row=0)
        self.label.grid(row=1)
        self.result = []
    
    def check_input(self, filetype, user_input):
        with open(f'./memo_{filetype}.txt', 'r') as f:
            lines = f.read().splitlines()
            if user_input in lines:
                return True
            else:
                return False
    
    def write_data(self, filetype, user_input):
        with open(f'./memo_{filetype}.txt', 'a') as f:
            f.write(user_input+'\n')
            
    def enter_input(self, event):
        user_input = self.entry.get()
        if 'vs' in user_input:
            input_check = self.check_input('ab', user_input)
            if not input_check:            
                self.write_data('ab', user_input)
                label_str = 'new'
            else:
                label_str = 'exist'
        else:
            input_check = self.check_input('ex', user_input)
            if not input_check:
                self.write_data('ex', user_input)
                label_str = 'new'
            else:
                label_str = 'exist'
        self.label.config(text=label_str)
            
        # entry 입력데이터 지우기
        self.entry.delete(0, tk.END)


search = Memo()
window.mainloop()