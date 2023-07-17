"""
엔트리(Entry)
텍스트를 입력하거나 보여주고자 사용하는 컴포넌트.
주로 한 줄로 구성된 문자열을 처리할 때 사용하며,
여러 줄의 문자열을 처리하려면 Text 컴포넌트를 사용한다.
"""

import tkinter as tk

root = tk.Tk()
entry = tk.Entry(root)
entry.pack()

entry.insert(0, 'Hello Python')

root.mainloop()