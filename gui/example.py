# tkinter 패키지 import
import tkinter
from time import sleep

# Tk Class 선언으로 window 창 생성
window = tkinter.Tk()

# 생성할 window 창의 크기 및 초기 위치 설정 매서드: geometry()
window_width = 400
window_height = 200
window_pos_x = 700
window_pos_y = 100

window.geometry("{}x{}+{}+{}".format(window_width, window_height, window_pos_x, window_pos_y))

# 생성한 Window 창의 크기 조절 가능 여부 설정: resizable()
window.resizable(False, False)   # True, False 대신 1, 0을 사용할 수 있음

# 생성한 Window 창의 Title 설정: title()
window.title("Tkinter: Label Test by Rosmary")

# 생성한 Window 창의 Icon 설정: iconphoto()
# window.iconphoto(False, tkinter.PhotoImage(file="icon1.png"))

# tkinter.Label 클래스 선언 및 Button 위젯 생성
label_1 = tkinter.Label(window, text="Hello tkinter", anchor="w")
label_2 = tkinter.Label(window, text="Apply relief and background color", bg="skyblue", relief="solid", bd=1)

text_var = "Textvariable 인자값 테스트 및\n다행 처리 테스트"
label_3 = tkinter.Label(window, text=text_var, justify="left", fg="red")

# 생성한 Label 위젯을 pack() 매서드로 배치
label_1.pack()
label_2.pack()
label_3.pack()

# 생성한 창을 유지하기 위한 코드 작성
window.mainloop()