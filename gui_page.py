import tkinter as tk
# from gui_base import large_font, normal_font, li
import random

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        width = 200
        height = 150
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        pos_x = (screen_width - width) // 2
        pos_y = (screen_height - height) // 2
        self.geometry("{}x{}+{}+{}".format(width, height, pos_x, pos_y))
        self.switch_frame(MainPage)
    
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if hasattr(self, "_frame"):
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill=tk.BOTH, expand=True)

class BasePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)

class MainPage(BasePage):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Start page", font=('Arial', 12)).pack(side="top", fill="x", pady=5)
        tk.Button(self, text='Reading', font='Arial 12',
                  command=lambda: master.switch_frame(ReadingTest)).pack(side="left", padx=10)
        tk.Button(self, text='Writing', font='Arial 12',
                  command=lambda: master.switch_frame(WritingTest)).pack(side="left", padx=10)

class ReadingTest(BasePage):
    def __init__(self, master):
        super().__init__(master)

        ##

        # self.click = 0
        # self.label_han = tk.Label(self, text=" ", anchor="w", font=large_font)
        # self.label_kor = tk.Label(self, text=" ", font=normal_font)
        # self.label_lev = tk.Label(self, text=" ", font=normal_font)
        # self.label_cnt = tk.Label(self, text=" ", font=normal_font)
        # self.label_new = tk.Label(self, text=" ", font=normal_font)
        # self.grid_columnconfigure(0, weight=1)  # Column 0 will expand to center-align elements
        # self.grid_columnconfigure(1, weight=1)  # Column 1 will also expand for label_new
        # self.b_prev = tk.Button(self, text='<',
        #                         command=lambda s=self: s.update_labels('prv'))
        # self.b_next = tk.Button(self, text='>',
        #                         command=lambda s=self: s.update_labels('nxt'))
        # self.label_han.grid(row=0, column=0, columnspan=2)  # Set columnspan to 2 to span both columns
        # self.label_kor.grid(row=1, column=0, columnspan=2)
        # self.label_lev.grid(row=2, column=0, columnspan=2)
        # self.label_cnt.grid(row=3, column=0, sticky="e")  # Use sticky="e" for right-align
        # self.label_new.grid(row=3, column=1, sticky="w")  # Use sticky="w" for left-align
        # self.b_next.grid(row=4, column=1)
        # random.shuffle(li)
        ##
        tk.Label(self, text="Page one", font=('Arial', 12)).pack(side="top", fill="x", pady=5)
        tk.Button(self, text='Go back to start page', font='Arial 12',
                  command=lambda: master.switch_frame(MainPage)).pack()

class WritingTest(BasePage):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Page two", font=('Arial', 12)).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", font='Arial 12',
                  command=lambda: master.switch_frame(MainPage)).pack()

if __name__ == '__main__':
    app = App()
    app.mainloop()
