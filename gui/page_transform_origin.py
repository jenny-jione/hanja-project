import tkinter as tk
from tkinter import font

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        width = 200
        height = 150
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        pos_x = (screen_width - width) // 2
        pos_y = (screen_height - height) // 2
        self.geometry("{}x{}+{}+{}".format(width, height, pos_x, pos_y))
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
        tk.Label(self, text="Start page").pack(side="top", fill="x", pady=5)
        tk.Button(self, text='Reading', font='D2Coding',
                  command=lambda: master.switch_frame(ReadingTest)).pack(side="left", padx=10)
        tk.Button(self, text='Writing', font='D2Coding',
                  command=lambda: master.switch_frame(WritingTest)).pack(side="left", padx=10)

class ReadingTest(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Page one").pack(side="top", fill="x", pady=5)
        tk.Button(self, text='go back to start page', font='D2Coding',
                  command=lambda: master.switch_frame(MainPage)).pack()

class WritingTest(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Page two").pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", font='D2Coding',
                  command=lambda: master.switch_frame(MainPage)).pack()

if __name__ == '__main__':
    app = App()
    app.mainloop()