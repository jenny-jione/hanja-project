import tkinter as tk
from tkinter import font

WINDOW_WIDTH = 200
WINDOW_HEIGHT = 150
WINDOW_POS_X = 1800
WINDOW_POS_Y = 800

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_POS_X, WINDOW_POS_Y))
        self._frame = None
        self.switch_frame(MainPage)
    
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Start page", 
                 font=('D2Coding')).pack(side="top", fill="x", pady=5)
        tk.Button(self, text='Reading', font='D2Coding',
                  command=lambda: master.switch_frame(ReadingTest)).pack(side="left", padx=10)
        tk.Button(self, text='Writing', font='D2Coding',
                  command=lambda: master.switch_frame(WritingTest)).pack(side="left", padx=10)

from modules.load import load_file_today
from modules.shuffle import HANJA_IDX, HMS_IDX, LEVEL_IDX

class ReadingTest(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Page one", 
                 font=('D2Coding')).pack(side="top", fill="x", pady=5)
        tk.Button(self, text='go back to start page', font='D2Coding',
                  command=lambda: master.switch_frame(MainPage)).pack()

class WritingTest(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Page two", 
                 font=('D2Coding')).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", font='D2Coding',
                  command=lambda: master.switch_frame(MainPage)).pack()

if __name__ == '__main__':
    app = App()
    app.mainloop()