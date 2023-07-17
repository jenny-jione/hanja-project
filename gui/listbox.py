"""
리스트박스 (ListBox)
블로그 목록처럼 정해진 순서가 있는 여러 개의 데이터를 표시하는 컴포넌트.
END: 리스트박스의 마지막 위치에 새로운 데이터를 추가하는 역할.
리스트 박스를 선택했을 때 특별한 동작을 하도록 하려면 
 -> 이벤트를 구현하면 된다.
컴포넌트에 이벤트를 연결하려면 bind() 함수를 사용한다.
"""

import tkinter as tk

root = tk.Tk()
listbox = tk.Listbox(root)
listbox.pack()

for i in ['one', 'two', 'three', 'four']:
    listbox.insert(tk.END, i)

def event_for_listbox(event):
    print('Hello Event')

listbox.bind('<<ListboxSelect>>', event_for_listbox)

root.mainloop()