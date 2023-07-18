import tkinter as tk

window = tk.Tk()
window_width = 1000
window_height = 400

# Get screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate position for the window to be centered
window_pos_x = (screen_width - window_width) // 2
window_pos_y = (screen_height - window_height) // 2

# window_pos_x = 800
# window_pos_y = 500
window.geometry("{}x{}+{}+{}".format(window_width, window_height, window_pos_x, window_pos_y))
window.resizable(False, False)
window.title("Tkinter: 한자 3급 합격 기원🍀")

# TODO: gui_study.py, gui_test_*.py에서 공통으로 사용하는 부분이 너무 많은데
# 이것들도 다 이 base 파일에 넣을 수 있게 하기!!