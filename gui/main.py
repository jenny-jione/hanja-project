# tkinter 패키지 import
import tkinter as tk
from time import sleep

# Tk Class 선언으로 window 창 생성
window = tk.Tk()

# 생성할 window 창의 크기 및 초기 위치 설정 매서드: geometry()
window_width = 400
window_height = 200
window_pos_x = 700
window_pos_y = 100

window.geometry("{}x{}+{}+{}".format(window_width, window_height, window_pos_x, window_pos_y))

# 생성한 Window 창의 크기 조절 가능 여부 설정: resizable()
window.resizable(False, False)   # True, False 대신 1, 0을 사용할 수 있음

# 생성한 Window 창의 Title 설정: title()
window.title("Tkinter: Test")

# 생성한 Window 창의 Icon 설정: iconphoto()
# window.iconphoto(False, tk.PhotoImage(file="icon1.png"))

# tk.Label 클래스 선언 및 Button 위젯 생성
label1 = tk.Label(window, text="한자", anchor="w")
label2 = tk.Label(window, text="여긴 답 나옴", bg="skyblue", relief="solid", bd=1)

b1 = tk.Button(window, text='정답')
# 생성한 Label 위젯을 pack() 매서드로 배치
label1.pack()
label2.pack()
b1.pack()

# 생성한 창을 유지하기 위한 코드 작성
window.mainloop()