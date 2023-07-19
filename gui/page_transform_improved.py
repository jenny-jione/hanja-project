import tkinter as tk

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
