import tkinter as tk

root = tk.Tk()
# Label 클래스의 첫 번째 인수로 root 사용 -> root 창에 포함되는 컴포넌트로 생성하겠다는 뜻
label = tk.Label(root, text='Hello World')
# label 객체를 창에 표시하는 역할
label.pack()


# root 창을 이벤트 루프에 들어가도록 함.
# mainloop에 의해 root 창은 종료되지 않고
#  버튼 클릭 등의 이벤트를 수신하거나
#  사용자의 입력을 처리하는 등의 일을 계속 수행할 수 있다.
root.mainloop()