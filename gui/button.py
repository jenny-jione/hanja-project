"""
버튼(Button)
클릭했을 때 특정 함수를 실행하고자 사용하는 컴포넌트.
"""

import tkinter as tk

root = tk.Tk()
b1 = tk.Button(root, text='테스트')
b1.pack()

def btn_click(event):
    print('click!')

b1.bind('<Button-1>', btn_click)

root.mainloop()